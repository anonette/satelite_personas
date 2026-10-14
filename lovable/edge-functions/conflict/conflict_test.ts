import { buildConflictPrompt } from "../_shared/prompts.ts";
import { conflictKey, handler, validateConflict, generateConflict } from "./lib.ts";

function eq(a: unknown, b: unknown) { if (a !== b) throw new Error(`expected ${String(b)}, got ${String(a)}`); }
function assert(c: unknown, m = "assertion failed") { if (!c) throw new Error(m); }

const pa = { agent_id: "bahai-gardens", name: "Terraced Tsores", hebrew_name: "גינה", location: "Baha'i Gardens", personality: "greenly smug", monologue: "my NDVI is 0.71!", challenges: [], voice_hint: "v" };
const pb = { agent_id: "haifa-bay-industrial-zone", name: "Captain Diesel-stein", hebrew_name: "קפטן", location: "Haifa Bay", personality: "jobs jobs", monologue: "NDVI 0.12 but we pay salaries", challenges: [], voice_hint: "v" };
const good = { lines: [{ speaker: pa.name, text: "x" }, { speaker: pb.name, text: "y" }] };
const stub = (...contents: string[]) => {
  let n = 0;
  const f = (() => Promise.resolve(new Response(JSON.stringify({ choices: [{ message: { content: contents[Math.min(n++, contents.length - 1)] } }] })))) as unknown as typeof fetch;
  return { f, calls: () => n };
};

Deno.test("conflictKey is order independent", () => {
  eq(conflictKey("a", "b"), conflictKey("b", "a"));
  assert(conflictKey("a", "b").startsWith("conflict:a:b:"));
});

Deno.test("prompt includes names and claims", () => {
  const p = buildConflictPrompt(pa, pb);
  for (const s of [pa.name, pb.name, pa.monologue, pb.monologue, "JSON", "lines", "speaker"]) assert(p.includes(s), s);
});

Deno.test("validateConflict: 2-4 lines, known speakers", () => {
  const names = [pa.name, pb.name];
  assert(validateConflict(good, names));
  assert(!validateConflict({ lines: [good.lines[0]] }, names));
  assert(!validateConflict({ lines: [...good.lines, ...good.lines, good.lines[0]] }, names));
  assert(!validateConflict({ lines: [{ speaker: "Nobody", text: "x" }, good.lines[1]] }, names));
  assert(!validateConflict({ lines: [{ speaker: pa.name, text: "" }, good.lines[1]] }, names));
});

Deno.test("generateConflict: retry then success; double failure throws llm", async () => {
  const s = stub("garbage", JSON.stringify(good));
  eq((await generateConflict(pa, pb, s.f)).lines.length, 2);
  eq(s.calls(), 2);
  const s2 = stub("garbage", "{}");
  let err = "";
  try { await generateConflict(pa, pb, s2.f); } catch (e) { err = (e as Error).message; }
  eq(err, "llm");
  eq(s2.calls(), 2);
});

const req = (body: unknown, pw = "pw") =>
  new Request("http://x/", { method: "POST", headers: { "x-theater-passcode": pw }, body: JSON.stringify(body) });

Deno.test("handler: OPTIONS, auth, bad input", async () => {
  Deno.env.set("THEATER_PASSCODE", "pw");
  eq((await handler(new Request("http://x/", { method: "OPTIONS" }))).status, 204);
  eq((await handler(req({ agentA: "a", agentB: "b" }, "bad"))).status, 401);
  eq((await handler(req({ agentA: "a" }))).status, 400);
  eq((await handler(req({ agentA: "a", agentB: "a" }))).status, 400);
});

Deno.test("handler: 409 when persona missing, cache hit symmetric", async () => {
  const dir = await Deno.makeTempDir();
  Deno.env.set("THEATER_PASSCODE", "pw");
  Deno.env.delete("SUPABASE_URL");
  Deno.env.set("LOCAL_CACHE_DIR", dir);
  const { dailyKey, cacheSet } = await import("../_shared/cache.ts");
  const orig = globalThis.fetch;
  globalThis.fetch = (() => { throw new Error("network!"); }) as typeof fetch;
  try {
    const r = await handler(req({ agentA: pa.agent_id, agentB: pb.agent_id }));
    eq(r.status, 409);
    eq((await r.json()).error, "persona_missing");
    await cacheSet(dailyKey("persona", pa.agent_id), pa);
    eq((await handler(req({ agentA: pa.agent_id, agentB: pb.agent_id }))).status, 409);
    await cacheSet(dailyKey("persona", pb.agent_id), pb);
    await cacheSet(conflictKey(pa.agent_id, pb.agent_id), good);
    for (const [x, y] of [[pa, pb], [pb, pa]]) {
      const ok = await handler(req({ agentA: x.agent_id, agentB: y.agent_id }));
      eq(ok.status, 200);
      eq(JSON.stringify(await ok.json()), JSON.stringify(good));
    }
  } finally {
    globalThis.fetch = orig;
    await Deno.remove(dir, { recursive: true });
  }
});

Deno.test("handler: llm failure -> 502", async () => {
  const dir = await Deno.makeTempDir();
  Deno.env.set("THEATER_PASSCODE", "pw");
  Deno.env.delete("SUPABASE_URL");
  Deno.env.set("LOCAL_CACHE_DIR", dir);
  const { dailyKey, cacheSet } = await import("../_shared/cache.ts");
  await cacheSet(dailyKey("persona", pa.agent_id), pa);
  await cacheSet(dailyKey("persona", pb.agent_id), pb);
  const orig = globalThis.fetch;
  globalThis.fetch = stub("nope").f;
  try {
    const r = await handler(req({ agentA: pa.agent_id, agentB: pb.agent_id }));
    eq(r.status, 502);
    eq((await r.json()).error, "llm");
  } finally {
    globalThis.fetch = orig;
    await Deno.remove(dir, { recursive: true });
  }
});
