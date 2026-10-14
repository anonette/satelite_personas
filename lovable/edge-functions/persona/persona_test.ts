import { buildPersonaPrompt } from "../_shared/prompts.ts";
import { callLLM, handler } from "./lib.ts";
import agents from "../../data/agents.json" with { type: "json" };

function eq(a: unknown, b: unknown) {
  if (a !== b) throw new Error(`expected ${String(b)}, got ${String(a)}`);
}
function assert(c: unknown, m = "assertion failed") { if (!c) throw new Error(m); }

const agent = agents[0] as any;
const stats = {
  ndvi: { mean: 0.4567, min: 0.1, max: 0.8 },
  bands: { B02: 0.05, B03: 0.08, B04: 0.07, B08: 0.3, B11: 0.2, B12: 0.1 },
  interval: { from: "2026-09-14T00:00:00Z", to: "2026-10-14T00:00:00Z" },
};
const good = {
  name: "Terraced Tsores", hebrew_name: "גינה אבו ספקטרלי", location: "Baha'i Gardens",
  personality: "p", monologue: "m", challenges: [{ target: "Haifa Port", line: "x" }], voice_hint: "v",
};
const stub = (...contents: string[]) => {
  let n = 0;
  const f = (() => Promise.resolve(new Response(JSON.stringify({ choices: [{ message: { content: contents[Math.min(n++, contents.length - 1)] } }] })))) as unknown as typeof fetch;
  return { f, calls: () => n };
};

Deno.test("prompt has Hebrew name, NDVI 2dp, JSON", () => {
  const p = buildPersonaPrompt(agent, stats);
  assert(p.includes(agent.name_he));
  assert(p.includes("0.46"));
  assert(p.includes("JSON"));
  assert(p.includes("hebrew_name") && p.includes("voice_hint") && p.includes("challenges"));
});

Deno.test("callLLM: malformed twice rejects with llm", async () => {
  const s = stub("not json", "{bad");
  let err = "";
  try { await callLLM("p", s.f); } catch (e) { err = (e as Error).message; }
  eq(err, "llm");
  eq(s.calls(), 2);
});

Deno.test("callLLM: valid resolves, Hebrew survives round trip", async () => {
  const p = await callLLM("p", stub(JSON.stringify(good)).f);
  assert(p.hebrew_name.length > 0);
  eq(JSON.parse(JSON.stringify(p)).hebrew_name, good.hebrew_name);
});

Deno.test("callLLM: empty hebrew_name retries then succeeds", async () => {
  const s = stub(JSON.stringify({ ...good, hebrew_name: "" }), JSON.stringify(good));
  const p = await callLLM("p", s.f);
  eq(p.hebrew_name, good.hebrew_name);
  eq(s.calls(), 2);
});

Deno.test("callLLM: missing hebrew_name twice rejects; empty challenges ok", async () => {
  const { hebrew_name: _h, ...noHe } = good;
  let err = "";
  try { await callLLM("p", stub(JSON.stringify(noHe)).f); } catch (e) { err = (e as Error).message; }
  eq(err, "llm");
  const p = await callLLM("p", stub(JSON.stringify({ ...good, challenges: [] })).f);
  eq(p.challenges.length, 0);
});

Deno.test("handler: auth, OPTIONS, unknown agent", async () => {
  Deno.env.set("THEATER_PASSCODE", "pw");
  eq((await handler(new Request("http://x/", { method: "OPTIONS" }))).status, 204);
  eq((await handler(new Request("http://x/?agent=a", { method: "POST" }))).status, 401);
  const r = await handler(new Request("http://x/?agent=nope", { method: "POST", headers: { "x-theater-passcode": "pw" } }));
  eq(r.status, 400);
});

Deno.test("handler: cached persona served without any network", async () => {
  const dir = await Deno.makeTempDir();
  Deno.env.set("THEATER_PASSCODE", "pw");
  Deno.env.delete("SUPABASE_URL");
  Deno.env.set("LOCAL_CACHE_DIR", dir);
  const { dailyKey, cacheSet } = await import("../_shared/cache.ts");
  const cached = { agent_id: agent.id, ...good };
  await cacheSet(dailyKey("persona", agent.id), cached);
  const orig = globalThis.fetch;
  globalThis.fetch = (() => { throw new Error("network!"); }) as typeof fetch;
  try {
    const r = await handler(new Request("http://x/", { method: "POST", headers: { "x-theater-passcode": "pw" }, body: JSON.stringify({ agentId: agent.id }) }));
    eq(r.status, 200);
    eq(JSON.stringify(await r.json()), JSON.stringify(cached));
  } finally {
    globalThis.fetch = orig;
    await Deno.remove(dir, { recursive: true });
  }
});
