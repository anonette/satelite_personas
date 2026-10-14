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
  interval: { from: string; to: string };
}

const AGENTS = agentsData as unknown as Agent[];
const TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token";
const SH = "https://sh.dataspace.copernicus.eu";
const CRS = "http://www.opengis.net/def/crs/EPSG/0/4326";
const HAIFA_BBOX = [34.95, 32.75, 35.10, 32.85];
const BAND_NAMES = ["B02", "B03", "B04", "B08", "B11", "B12"] as const;

const STATS_EVALSCRIPT = `//VERSION=3
function setup() {
  return {input: [{bands: ["B02", "B03", "B04", "B08", "B11", "B12", "dataMask"]}],
          output: [{id: "ndvi", bands: 1}, {id: "bands", bands: 6}, {id: "dataMask", bands: 1}]};
}
function evaluatePixel(s) {
  let ndvi = (s.B08 - s.B04) / (s.B08 + s.B04);
  return {ndvi: [ndvi], bands: [s.B02, s.B03, s.B04, s.B08, s.B11, s.B12], dataMask: [s.dataMask]};
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

export function buildOverlayRequest(now = new Date()): object {
  return {
    input: {
      bounds: { bbox: HAIFA_BBOX, properties: { crs: CRS } },
      data: [{
        type: "sentinel-2-l2a",
        dataFilter: { timeRange: window30(now), maxCloudCoverage: 60, mosaickingOrder: "leastCC" },
      }],
    },
    output: { width: 640, height: 500, responses: [{ identifier: "default", format: { type: "image/png" } }] },
    evalscript: VIS_EVALSCRIPT,
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
  return {
    ndvi: ndvi as SpectralStats["ndvi"],
    bands: bands as SpectralStats["bands"],
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
    if (action === "overlay") {
      const key = dailyKey("overlay");
      const png = (b: Uint8Array) =>
        new Response(b as unknown as BodyInit, { headers: { ...CORS_HEADERS, "Content-Type": "image/png" } });
      const hit = await cacheGet(key);
      if (typeof hit === "string") return png(b64decode(hit));
      const token = await getToken();
      const res = await fetch(`${SH}/api/v1/process`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json", Accept: "image/png" },
        body: JSON.stringify(buildOverlayRequest()),
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
