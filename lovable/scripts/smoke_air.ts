// Live smoke: deno run -A lovable/scripts/smoke_air.ts  (loads repo .env)
import { getAir, handler } from "../edge-functions/copernicus/lib.ts";

const envText = await Deno.readTextFile(new URL("../../.env", import.meta.url));
for (const line of envText.split(/\r?\n/)) {
  const m = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$/);
  if (m && !line.trim().startsWith("#")) Deno.env.set(m[1], m[2].replace(/^(['"])(.*)\1$/, "$2"));
}
const pass = "smoke-" + crypto.randomUUID();
Deno.env.set("THEATER_PASSCODE", pass);
Deno.env.delete("SUPABASE_URL");
Deno.env.set("LOCAL_CACHE_DIR", await Deno.makeTempDir());

const server = Deno.serve({ port: 0, onListen: () => {} }, handler);
const base = `http://127.0.0.1:${server.addr.port}/`;
const H = { "x-theater-passcode": pass };
let fail = false;

const r = await fetch(`${base}?action=stats&agent=bahai-gardens`, { headers: H });
const body = await r.json();
console.log("stats", r.status, JSON.stringify(body));
const ix = body.indices ?? {};
for (const k of ["ndwi", "ndmi", "ndbi", "nbr"]) {
  if (typeof ix[k] !== "number" || ix[k] < -1 || ix[k] > 1) { fail = true; console.log("  BAD", k); }
}
if (typeof ix.aerosol !== "number" || ix.aerosol < 0 || ix.aerosol > 0.6) { fail = true; console.log("  BAD aerosol"); }

const air = await getAir();
console.log("air", JSON.stringify(air));
if (!air || !(air.no2 > 0)) { fail = true; console.log("  AIR UNAVAILABLE"); }

const o = await fetch(`${base}?action=overlay&kind=truecolor`, { headers: H });
const buf = new Uint8Array(await o.arrayBuffer());
console.log("truecolor overlay:", o.status, buf.length, "bytes");
if (o.status !== 200 || buf.length < 20_000) fail = true;

await server.shutdown();
console.log(fail ? "SMOKE FAIL" : "SMOKE OK");
Deno.exit(fail ? 1 : 0);
