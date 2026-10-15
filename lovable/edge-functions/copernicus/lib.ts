import { checkPasscode } from "../_shared/auth.ts";
import { cacheGet, cacheSet, dailyKey } from "../_shared/cache.ts";
import { cors, json, CORS_HEADERS } from "../_shared/http.ts";
import agentsData from "../../data/agents.json" with { type: "json" };

export interface Agent {
  id: string;
  stats_bbox: number[];
  [k: string]: unknown;
}
export interface SpectralStats {
  ndvi: { mean: number; min: number; max: number };
  bands: { B02: number; B03: number; B04: number; B08: number; B11: number; B12: number };
  indices?: { ndwi: number | null; ndmi: number | null; ndbi: number | null; nbr: number | null; aerosol: number | null };
  interval: { from: string; to: string };
}

const AGENTS = agentsData as unknown as Agent[];
const TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token";
const SH = "https://sh.dataspace.copernicus.eu";
const CRS = "http://www.opengis.net/def/crs/EPSG/0/4326";
const HAIFA_BBOX = [34.95, 32.75, 35.10, 32.85];
const BAND_NAMES = ["B02", "B03", "B04", "B08", "B11", "B12"] as const;

export interface AirQuality {
  no2: number;
  interval: { from: string; to: string };
}

const INDEX_IDS = ["ndwi", "ndmi", "ndbi", "nbr", "aerosol"] as const;

const STATS_EVALSCRIPT = `//VERSION=3
function setup() {
  return {input: [{bands: ["B01", "B02", "B03", "B04", "B08", "B11", "B12", "dataMask"]}],
          output: [{id: "ndvi", bands: 1}, {id: "bands", bands: 6},
                   {id: "ndwi", bands: 1}, {id: "ndmi", bands: 1}, {id: "ndbi", bands: 1},
                   {id: "nbr", bands: 1}, {id: "aerosol", bands: 1}, {id: "dataMask", bands: 1}]};
}
function evaluatePixel(s) {
  let ndvi = (s.B08 - s.B04) / (s.B08 + s.B04);
  return {ndvi: [ndvi], bands: [s.B02, s.B03, s.B04, s.B08, s.B11, s.B12],
          ndwi: [(s.B03 - s.B08) / (s.B03 + s.B08)],
          ndmi: [(s.B08 - s.B11) / (s.B08 + s.B11)],
          ndbi: [(s.B11 - s.B08) / (s.B11 + s.B08)],
          nbr: [(s.B08 - s.B12) / (s.B08 + s.B12)],
          aerosol: [s.B01],
          dataMask: [s.dataMask]};
}`;

const VIS_EVALSCRIPT = `//VERSION=3
function setup() {
  return {input: ["B04", "B08", "dataMask"], output: {bands: 4}};
}
function evaluatePixel(s) {
  let ndvi = (s.B08 - s.B04) / (s.B08 + s.B04);
  let c = ndvi < 0 ? [0.05, 0.2, 0.4] :
          ndvi < 0.2 ? [0.6, 0.5, 0.35] :
          ndvi < 0.4 ? [0.55, 0.7, 0.3] :
          ndvi < 0.6 ? [0.25, 0.6, 0.2] : [0.05, 0.4, 0.1];
  return [c[0], c[1], c[2], s.dataMask];
}`;

const TRUECOLOR_EVALSCRIPT = `//VERSION=3
function setup() {
  return {input: ["B02", "B03", "B04", "dataMask"], output: {bands: 4}};
}
function evaluatePixel(s) {
  return [2.5 * s.B04, 2.5 * s.B03, 2.5 * s.B02, s.dataMask];
}`;

const AIR_EVALSCRIPT = `//VERSION=3
function setup() {
  return {input: [{bands: ["NO2", "dataMask"]}],
          output: [{id: "no2", bands: 1}, {id: "dataMask", bands: 1}]};
}
function evaluatePixel(s) {
  return {no2: [s.NO2], dataMask: [s.dataMask]};
}`;

function iso(d: Date): string {
  return d.toISOString().slice(0, 19) + "Z";
}
function window30(now: Date): { from: string; to: string } {
  return { from: iso(new Date(now.getTime() - 30 * 86400_000)), to: iso(now) };
}

export function buildStatsRequest(agent: Agent, now = new Date()): object {
  return {
    input: {
      bounds: { bbox: agent.stats_bbox, properties: { crs: CRS } },
      data: [{
        type: "sentinel-2-l2a",
        dataFilter: { maxCloudCoverage: 60, mosaickingOrder: "leastCC" },
      }],
    },
    aggregation: {
      timeRange: window30(now),
      aggregationInterval: { of: "P30D" },
      width: 32,
      height: 32,
      evalscript: STATS_EVALSCRIPT,
    },
  };
}

export function buildAirRequest(now = new Date()): object {
  return {
    input: {
      bounds: { bbox: HAIFA_BBOX, properties: { crs: CRS } },
      data: [{ type: "sentinel-5p-l2", dataFilter: {} }],
    },
    aggregation: {
      timeRange: { from: iso(new Date(now.getTime() - 5 * 86400_000)), to: iso(now) },
      aggregationInterval: { of: "P5D" },
      width: 16,
      height: 16,
      evalscript: AIR_EVALSCRIPT,
    },
  };
}

export function buildOverlayRequest(now = new Date(), kind = "ndvi"): object {
  return {
    input: {
      bounds: { bbox: HAIFA_BBOX, properties: { crs: CRS } },
      data: [{
        type: "sentinel-2-l2a",
        dataFilter: { timeRange: window30(now), maxCloudCoverage: 60, mosaickingOrder: "leastCC" },
      }],
    },
    output: { width: 640, height: 500, responses: [{ identifier: "default", format: { type: "image/png" } }] },
    evalscript: kind === "truecolor" ? TRUECOLOR_EVALSCRIPT : VIS_EVALSCRIPT,
  };
}

// deno-lint-ignore no-explicit-any
export function parseStats(resp: any): SpectralStats | null {
  const d = resp?.data?.[0];
  if (!d) return null;
  const n = d.outputs?.ndvi?.bands?.B0?.stats;
  const b = d.outputs?.bands?.bands;
  if (!n || !b) return null;
  const num = (v: unknown) => (typeof v === "number" && Number.isFinite(v) ? v : null);
  const ndvi = { mean: num(n.mean), min: num(n.min), max: num(n.max) };
  if (ndvi.mean === null || ndvi.min === null || ndvi.max === null) return null;
  const bands: Record<string, number> = {};
  for (let i = 0; i < BAND_NAMES.length; i++) {
    const m = num(b[`B${i}`]?.stats?.mean);
    if (m === null) return null;
    bands[BAND_NAMES[i]] = m;
  }
  const indices: Record<string, number | null> = {};
  for (const id of INDEX_IDS) indices[id] = num(d.outputs?.[id]?.bands?.B0?.stats?.mean);
  return {
    ndvi: ndvi as SpectralStats["ndvi"],
    bands: bands as SpectralStats["bands"],
    indices: indices as SpectralStats["indices"],
    interval: { from: d.interval?.from, to: d.interval?.to },
  };
}

let tokenCache: { token: string; expires: number } | null = null;

export async function getToken(fetchFn: typeof fetch = fetch): Promise<string> {
  if (tokenCache && Date.now() < tokenCache.expires - 60_000) return tokenCache.token;
  const res = await fetchFn(TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "client_credentials",
      client_id: (Deno.env.get("CDSE_CLIENT_ID") ?? "").trim(),
      client_secret: (Deno.env.get("CDSE_CLIENT_SECRET") ?? "").trim(),
    }).toString(),
  });
  if (!res.ok) throw new Error(`token HTTP ${res.status}`);
  const j = await res.json();
  if (typeof j?.access_token !== "string" || !j.access_token) throw new Error("token missing access_token");
  tokenCache = { token: j.access_token, expires: Date.now() + (j.expires_in ?? 600) * 1000 };
  return j.access_token;
}

function b64encode(bytes: Uint8Array): string {
  let s = "";
  for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(s);
}
function b64decode(s: string): Uint8Array {
  return Uint8Array.from(atob(s), (c) => c.charCodeAt(0));
}

export async function handler(req: Request): Promise<Response> {
  const pre = cors(req);
  if (pre) return pre;
  const denied = checkPasscode(req);
  if (denied) return denied;
  const url = new URL(req.url);
  const action = url.searchParams.get("action");
  try {
    if (action === "stats") {
      const id = url.searchParams.get("agent") ?? "";
      const agent = AGENTS.find((a) => a.id === id);
      if (!agent) return json({ error: "unknown_agent" }, 400);
      const key = dailyKey("stats", id);
      const hit = await cacheGet(key);
      if (hit) return json(hit);
      const token = await getToken();
      const res = await fetch(`${SH}/api/v1/statistics`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        body: JSON.stringify(buildStatsRequest(agent)),
      });
      if (!res.ok) {
        await res.body?.cancel();
        return json({ error: "upstream", status: res.status }, 502);
      }
      const stats = parseStats(await res.json());
      if (!stats) return json({ error: "no_data" }, 503);
      await cacheSet(key, stats);
      return json(stats);
    }
    if (action === "air") {
      const air = await getAir();
      return air ? json(air) : json({ error: "no_data" }, 503);
    }
    if (action === "overlay") {
      const kind = url.searchParams.get("kind") === "truecolor" ? "truecolor" : "ndvi";
      const key = kind === "truecolor" ? dailyKey("overlay", "truecolor") : dailyKey("overlay");
      const png = (b: Uint8Array) =>
        new Response(b as unknown as BodyInit, { headers: { ...CORS_HEADERS, "Content-Type": "image/png" } });
      const hit = await cacheGet(key);
      if (typeof hit === "string") return png(b64decode(hit));
      const token = await getToken();
      const res = await fetch(`${SH}/api/v1/process`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json", Accept: "image/png" },
        body: JSON.stringify(buildOverlayRequest(new Date(), kind)),
      });
      if (!res.ok) {
        await res.body?.cancel();
        return json({ error: "upstream", status: res.status }, 502);
      }
      const bytes = new Uint8Array(await res.arrayBuffer());
      await cacheSet(key, b64encode(bytes));
      return png(bytes);
    }
    return json({ error: "bad_action" }, 400);
  } catch (e) {
    return json({ error: "upstream", message: String((e as Error).message ?? e) }, 502);
  }
}

/** Daily-cached spectral stats for an agent, fetched directly (no HTTP hop). Null when no data. Throws on upstream failure. */
export async function getStats(agent: Agent, fetchFn: typeof fetch = fetch): Promise<SpectralStats | null> {
  const key = dailyKey("stats", agent.id);
  const hit = await cacheGet(key);
  if (hit) return hit as SpectralStats;
  const token = await getToken(fetchFn);
  const res = await fetchFn(`${SH}/api/v1/statistics`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify(buildStatsRequest(agent)),
  });
  if (!res.ok) {
    await res.body?.cancel();
    throw new Error(`stats upstream ${res.status}`);
  }
  const stats = parseStats(await res.json());
  if (stats) await cacheSet(key, stats);
  return stats;
}

// deno-lint-ignore no-explicit-any
export function parseAir(resp: any): AirQuality | null {
  const d = resp?.data?.[0];
  const m = d?.outputs?.no2?.bands?.B0?.stats?.mean;
  if (typeof m !== "number" || !Number.isFinite(m)) return null;
  return { no2: m, interval: { from: d.interval?.from, to: d.interval?.to } };
}

/** Daily-cached Sentinel-5P NO2 mean over Haifa. Null on any failure; never throws. */
export async function getAir(fetchFn: typeof fetch = fetch): Promise<AirQuality | null> {
  try {
    const key = dailyKey("air");
    const hit = await cacheGet(key);
    if (hit) return hit as AirQuality;
    const token = await getToken(fetchFn);
    const res = await fetchFn(`${SH}/api/v1/statistics`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify(buildAirRequest()),
    });
    if (!res.ok) {
      const t = await res.text().catch(() => "");
      console.error(`getAir upstream ${res.status}: ${t.slice(0, 300)}`);
      return null;
    }
    const air = parseAir(await res.json());
    if (air) await cacheSet(key, air);
    return air;
  } catch (e) {
    console.error("getAir failed:", (e as Error).message ?? e);
    return null;
  }
}
