// Live smoke: deno run -A lovable/scripts/smoke_copernicus.ts  (loads repo .env)
import { handler } from "../edge-functions/copernicus/lib.ts";

const envText = await Deno.readTextFile(new URL("../../.env", import.meta.url));
for (const line of envText.split(/\r?\n/)) {
  const m = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$/);
  if (m && !line.trim().startsWith("#")) {
    Deno.env.set(m[1], m[2].replace(/^(['"])(.*)\1$/, "$2"));
  }
}
const pass = "smoke-" + crypto.randomUUID();
Deno.env.set("THEATER_PASSCODE", pass);
Deno.env.delete("SUPABASE_URL");
Deno.env.set("LOCAL_CACHE_DIR", await Deno.makeTempDir());

const server = Deno.serve({ port: 0, onListen: () => {} }, handler);
const base = `http://127.0.0.1:${server.addr.port}/`;
const H = { "x-theater-passcode": pass };
let fail = false;

for (const [id, ok] of [
  ["bahai-gardens", (m: number) => m >= 0.3 && m <= 0.6],
  ["haifa-bay-industrial-zone", (m: number) => m < 0.1],
] as const) {
  const r = await fetch(`${base}?action=stats&agent=${id}`, { headers: H });
  const body = await r.json();
  console.log(id, r.status, JSON.stringify(body));
  if (r.status !== 200 || !ok(body.ndvi?.mean)) { fail = true; console.log("  UNEXPECTED"); }
}
const noPass = await fetch(`${base}?action=overlay`);
console.log("overlay without passcode:", noPass.status);
await noPass.body?.cancel();
for (const label of ["miss", "cache hit"]) {
  const r = await fetch(`${base}?action=overlay`, { headers: H });
  const buf = new Uint8Array(await r.arrayBuffer());
  const png = buf[1] === 0x50 && buf[2] === 0x4e && buf[3] === 0x47;
  console.log(`overlay ${label}:`, r.status, r.headers.get("content-type"), buf.length, "bytes, png:", png);
  if (r.status !== 200 || buf.length < 20_000 || !png) fail = true;
}
await server.shutdown();
console.log(fail ? "SMOKE FAIL" : "SMOKE OK");
Deno.exit(fail ? 1 : 0);
