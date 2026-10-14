import { voiceFor } from "../_shared/voices.ts";
import { handler, voiceKey } from "./lib.ts";

function eq(a: unknown, b: unknown) { if (a !== b) throw new Error(`expected ${String(b)}, got ${String(a)}`); }
function assert(c: unknown, m = "assertion failed") { if (!c) throw new Error(m); }

const TYPES = ["industrial", "beach", "park", "academic", "cultural_religious", "cultural_residential", "residential", "commercial", "religious", "transportation"];

Deno.test("voiceFor total over types + unknown", () => {
  for (const t of TYPES) assert(/^[A-Za-z0-9]{20}$/.test(voiceFor(t)), t);
  assert(/^[A-Za-z0-9]{20}$/.test(voiceFor("nonsense")));
  assert(/^[A-Za-z0-9]{20}$/.test(voiceFor("toString")));
});

Deno.test("voiceKey stable and text-sensitive", async () => {
  const a = await voiceKey("bahai-gardens", "shalom");
  eq(a, await voiceKey("bahai-gardens", "shalom"));
  assert(a !== await voiceKey("bahai-gardens", "shalom!"));
  assert(a.startsWith("voice:bahai-gardens:"));
});

function req(body: unknown, pass = "pw") {
  return new Request("http://x/", { method: "POST", headers: { "x-theater-passcode": pass, "content-type": "application/json" }, body: JSON.stringify(body) });
}

Deno.test("handler: caches, 400s, auth, OPTIONS", async () => {
  Deno.env.set("THEATER_PASSCODE", "pw");
  Deno.env.set("ELEVENLABS_API_KEY", "k");
  Deno.env.delete("SUPABASE_URL");
  Deno.env.set("LOCAL_CACHE_DIR", await Deno.makeTempDir());
  let calls = 0, url = "";
  const audio = new Uint8Array([0x49, 0x44, 0x33, 1, 2, 3]);
  const orig = globalThis.fetch;
  globalThis.fetch = ((i: any) => { calls++; url = String(i); return Promise.resolve(new Response(audio)); }) as typeof fetch;
  try {
    const r1 = await handler(req({ agentId: "bahai-gardens", text: "shalom" }));
    eq(r1.status, 200);
    eq(r1.headers.get("content-type"), "audio/mpeg");
    eq((await r1.arrayBuffer()).byteLength, 6);
    eq(calls, 1);
    assert(url.includes("api.elevenlabs.io/v1/text-to-speech/"));
    const r2 = await handler(req({ agentId: "bahai-gardens", text: "shalom" }));
    eq(r2.status, 200);
    eq((await r2.arrayBuffer()).byteLength, 6);
    eq(calls, 1);
    eq((await handler(req({ agentId: "nope", text: "x" }))).status, 400);
    eq((await handler(req({ agentId: "bahai-gardens", text: "  " }))).status, 400);
    eq((await handler(req({ agentId: "bahai-gardens", text: "x" }, "bad"))).status, 401);
    eq((await handler(new Request("http://x/", { method: "OPTIONS" }))).status, 204);
    eq(calls, 1);
  } finally {
    globalThis.fetch = orig;
  }
});
