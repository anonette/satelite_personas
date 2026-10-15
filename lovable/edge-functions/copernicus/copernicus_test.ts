import { buildAirRequest, buildOverlayRequest, buildStatsRequest, getAir, getToken, parseStats } from "./lib.ts";
import agents from "../../data/agents.json" with { type: "json" };

function eq(a: unknown, b: unknown) {
  if (JSON.stringify(a) !== JSON.stringify(b)) {
    throw new Error(`expected ${JSON.stringify(b)}, got ${JSON.stringify(a)}`);
  }
}
function assert(c: unknown, m = "assertion failed") {
  if (!c) throw new Error(m);
}

const agent = agents.find((a) => a.id === "bahai-gardens")!;

Deno.test("buildStatsRequest matches spike shape", () => {
  const now = new Date("2026-10-14T12:00:00Z");
  // deno-lint-ignore no-explicit-any
  const r = buildStatsRequest(agent as any, now) as any;
  eq(r.input.bounds.bbox, agent.stats_bbox);
  eq(r.input.bounds.properties.crs, "http://www.opengis.net/def/crs/EPSG/0/4326");
  eq(r.input.data, [{
    type: "sentinel-2-l2a",
    dataFilter: { maxCloudCoverage: 60, mosaickingOrder: "leastCC" },
  }]);
  eq(r.aggregation.aggregationInterval, { of: "P30D" });
  eq(r.aggregation.width, 32);
  eq(r.aggregation.height, 32);
  eq(r.aggregation.timeRange.to, "2026-10-14T12:00:00Z");
  eq(r.aggregation.timeRange.from, "2026-09-14T12:00:00Z");
  const es: string = r.aggregation.evalscript;
  for (const id of ['id: "ndvi"', 'id: "bands"', 'id: "dataMask"', "B11", "B12", "B02"]) {
    assert(es.includes(id), `evalscript missing ${id}`);
  }
});

Deno.test("buildOverlayRequest uses Haifa bbox and PNG", () => {
  // deno-lint-ignore no-explicit-any
  const r = buildOverlayRequest(new Date("2026-10-14T12:00:00Z")) as any;
  eq(r.input.bounds.bbox, [34.95, 32.75, 35.10, 32.85]);
  eq(r.input.data[0].dataFilter.maxCloudCoverage, 60);
  eq(r.input.data[0].dataFilter.mosaickingOrder, "leastCC");
  eq(r.input.data[0].dataFilter.timeRange.from, "2026-09-14T12:00:00Z");
  eq(r.output.responses[0].format.type, "image/png");
  assert(r.evalscript.includes("0.05, 0.2, 0.4"));
});

const sample = {
  data: [{
    interval: { from: "2026-09-14T00:00:00Z", to: "2026-10-14T00:00:00Z" },
    outputs: {
      ndvi: { bands: { B0: { stats: { min: -0.1, max: 0.8, mean: 0.42, stDev: 0.1, sampleCount: 9, noDataCount: 0 } } } },
      bands: {
        bands: Object.fromEntries(
          [0.02, 0.04, 0.05, 0.3, 0.2, 0.1].map((m, i) => [`B${i}`, { stats: { mean: m, min: 0, max: 1 } }]),
        ),
      },
    },
  }],
};

Deno.test("parseStats extracts ndvi and bands", () => {
  const s = parseStats(sample)!;
  eq(s.ndvi, { mean: 0.42, min: -0.1, max: 0.8 });
  eq(s.bands, { B02: 0.02, B03: 0.04, B04: 0.05, B08: 0.3, B11: 0.2, B12: 0.1 });
  eq(s.interval, { from: "2026-09-14T00:00:00Z", to: "2026-10-14T00:00:00Z" });
});

Deno.test("parseStats returns null on empty/NaN data", () => {
  eq(parseStats({ data: [] }), null);
  eq(parseStats({}), null);
  const bad = structuredClone(sample);
  // deno-lint-ignore no-explicit-any
  (bad.data[0].outputs.ndvi.bands.B0.stats as any).mean = "NaN";
  eq(parseStats(bad), null);
});

Deno.test("getToken posts client credentials and caches", async () => {
  Deno.env.set("CDSE_CLIENT_ID", "cid");
  Deno.env.set("CDSE_CLIENT_SECRET", "sec");
  let calls = 0;
  let body = "";
  const f = ((_u: string, init: RequestInit) => {
    calls++;
    body = String(init.body);
    return Promise.resolve(new Response(JSON.stringify({ access_token: "tok" + calls, expires_in: 600 })));
  }) as unknown as typeof fetch;
  // A 200 without access_token must throw and must not be cached.
  const bad = (() => Promise.resolve(new Response("{}"))) as unknown as typeof fetch;
  let threw = false;
  try { await getToken(bad); } catch { threw = true; }
  assert(threw);
  const t1 = await getToken(f);
  const t2 = await getToken(f);
  eq(t1, "tok1");
  eq(t2, "tok1");
  eq(calls, 1);
  assert(body.includes("grant_type=client_credentials") && body.includes("client_id=cid") && body.includes("client_secret=sec"));
});

Deno.test("evalscript outputs the five extra indices and B01", () => {
  // deno-lint-ignore no-explicit-any
  const es: string = (buildStatsRequest(agent as any) as any).aggregation.evalscript;
  for (const id of ["ndwi", "ndmi", "ndbi", "nbr", "aerosol"]) {
    assert(es.includes(`id: "${id}"`), `evalscript missing ${id}`);
  }
  assert(es.includes('"B01"'));
});

Deno.test("buildOverlayRequest truecolor variant", () => {
  // deno-lint-ignore no-explicit-any
  const r = buildOverlayRequest(new Date("2026-10-14T12:00:00Z"), "truecolor") as any;
  assert(r.evalscript.includes("2.5"));
  assert(r.evalscript.includes("B02") && !r.evalscript.includes("0.05, 0.2, 0.4"));
  eq(r.input.bounds.bbox, [34.95, 32.75, 35.10, 32.85]);
});

function withIdx(extra: Record<string, number>) {
  const c = structuredClone(sample);
  for (const [k, v] of Object.entries(extra)) {
    // deno-lint-ignore no-explicit-any
    (c.data[0].outputs as any)[k] = { bands: { B0: { stats: { mean: v } } } };
  }
  return c;
}

Deno.test("parseStats maps indices and keeps old fields identical", () => {
  const old = parseStats(sample)!;
  const s = parseStats(withIdx({ ndwi: -0.3, ndmi: 0.1, ndbi: -0.1, nbr: 0.2, aerosol: 0.12 }))!;
  eq(s.indices, { ndwi: -0.3, ndmi: 0.1, ndbi: -0.1, nbr: 0.2, aerosol: 0.12 });
  eq(s.ndvi, old.ndvi);
  eq(s.bands, old.bands);
  eq(s.interval, old.interval);
});

const s5p = {
  data: [{
    interval: { from: "2026-10-10T00:00:00Z", to: "2026-10-15T00:00:00Z" },
    outputs: { no2: { bands: { B0: { stats: { mean: 0.00012, min: 0, max: 1 } } } } },
  }],
};

Deno.test("buildAirRequest targets sentinel-5p NO2", () => {
  // deno-lint-ignore no-explicit-any
  const r = buildAirRequest(new Date("2026-10-15T00:00:00Z")) as any;
  eq(r.input.data[0].type, "sentinel-5p-l2");
  eq(r.aggregation.aggregationInterval, { of: "P5D" });
  eq(r.aggregation.timeRange.from, "2026-10-10T00:00:00Z");
  assert(r.aggregation.evalscript.includes("NO2"));
});

function airFetch(airStatus: number) {
  return ((u: string) => {
    if (String(u).includes("token")) return Promise.resolve(new Response(JSON.stringify({ access_token: "t", expires_in: 600 })));
    return Promise.resolve(new Response(airStatus === 200 ? JSON.stringify(s5p) : "boom", { status: airStatus }));
  }) as unknown as typeof fetch;
}

Deno.test("getAir parses S5P response", async () => {
  Deno.env.delete("SUPABASE_URL");
  Deno.env.delete("LOCAL_CACHE_DIR");
  const a = await getAir(airFetch(200));
  eq(a, { no2: 0.00012, interval: { from: "2026-10-10T00:00:00Z", to: "2026-10-15T00:00:00Z" } });
});

Deno.test("getAir returns null on 500", async () => {
  Deno.env.delete("SUPABASE_URL");
  Deno.env.delete("LOCAL_CACHE_DIR");
  eq(await getAir(airFetch(500)), null);
});
