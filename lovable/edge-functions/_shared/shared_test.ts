import { checkPasscode } from "./auth.ts";
import { cacheGet, cacheSet, dailyKey } from "./cache.ts";
import { cors, json } from "./http.ts";

function assert(c: unknown, m = "assertion failed") {
  if (!c) throw new Error(m);
}
function eq(a: unknown, b: unknown) {
  if (a !== b) throw new Error(`expected ${String(b)}, got ${String(a)}`);
}
const req = (h?: string, method = "GET") =>
  new Request("http://x/", { method, headers: h === undefined ? {} : { "x-theater-passcode": h } });

Deno.test("passcode match", () => {
  Deno.env.set("THEATER_PASSCODE", "sesame");
  eq(checkPasscode(req("sesame")), null);
});

Deno.test("passcode mismatch and missing header", async () => {
  Deno.env.set("THEATER_PASSCODE", "sesame");
  for (const r of [req("nope"), req()]) {
    const res = checkPasscode(r)!;
    eq(res.status, 401);
    eq(await res.text(), '{"error":"passcode"}');
    eq(res.headers.get("access-control-allow-origin"), "*");
  }
});

Deno.test("passcode missing env rejects", () => {
  Deno.env.delete("THEATER_PASSCODE");
  eq(checkPasscode(req(""))?.status, 401);
  eq(checkPasscode(req("anything"))?.status, 401);
});

Deno.test("dailyKey ends with UTC date", () => {
  const k = dailyKey("persona", "haifa-port");
  eq(k, `persona:haifa-port:${new Date().toISOString().slice(0, 10)}`);
});

Deno.test("file cache round-trip", async () => {
  const dir = await Deno.makeTempDir();
  Deno.env.delete("SUPABASE_URL");
  Deno.env.delete("SUPABASE_SERVICE_ROLE_KEY");
  Deno.env.set("LOCAL_CACHE_DIR", dir);
  eq(await cacheGet("a:b/c:2026-01-01"), null);
  await cacheSet("a:b/c:2026-01-01", { x: [1, 2] });
  const v = await cacheGet("a:b/c:2026-01-01") as { x: number[] };
  eq(JSON.stringify(v), '{"x":[1,2]}');
  await Deno.remove(dir, { recursive: true });
});

Deno.test("unwritable cache dir is a miss, not a throw", async () => {
  const f = await Deno.makeTempFile();
  Deno.env.delete("SUPABASE_URL");
  Deno.env.set("LOCAL_CACHE_DIR", `${f}/sub`); // parent is a file
  eq(await cacheGet("k"), null);
  await cacheSet("k", 1);
  eq(await cacheGet("k"), null);
  await Deno.remove(f);
});

Deno.test("supabase backend error is a miss", async () => {
  Deno.env.set("SUPABASE_URL", "http://127.0.0.1:1");
  Deno.env.set("SUPABASE_SERVICE_ROLE_KEY", "k");
  eq(await cacheGet("k"), null);
  await cacheSet("k", 1);
  Deno.env.delete("SUPABASE_URL");
  Deno.env.delete("SUPABASE_SERVICE_ROLE_KEY");
});

Deno.test("http helpers", async () => {
  const r = json({ a: 1 }, 201);
  eq(r.status, 201);
  eq(r.headers.get("content-type"), "application/json");
  eq(r.headers.get("access-control-allow-origin"), "*");
  eq(await r.text(), '{"a":1}');
  const o = cors(req(undefined, "OPTIONS"))!;
  eq(o.status, 204);
  assert(o.headers.get("access-control-allow-headers")!.includes("x-theater-passcode"));
  assert(o.headers.get("access-control-allow-headers")!.includes("content-type"));
  eq(cors(req()), null);
});
