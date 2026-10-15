import { buildDebatePrompt } from "../_shared/prompts.ts";
import { castForDate, generateDebate, makeHandler, validateDebate } from "./lib.ts";

function eq(a: unknown, b: unknown) { if (a !== b) throw new Error(`expected ${String(b)}, got ${String(a)}`); }
function assert(c: unknown, m = "assertion failed") { if (!c) throw new Error(m); }

const IDS = Array.from({ length: 16 }, (_, i) => `a${i}`);
const mk = (id: string) => ({ agent_id: id, name: "N-" + id, hebrew_name: "ה", location: "L" + id, personality: "p", monologue: "NDVI 0.5", challenges: [], voice_hint: "v", policy_claim: "PC-" + id, demand: "D-" + id });
const names = ["N-a", "N-b", "N-c", "N-d"];
const lines = (n: number, sp = names) => ({ lines: Array.from({ length: n }, (_, i) => ({ speaker: sp[i % sp.length], text: "t" + i })) });

Deno.test("castForDate: deterministic, 4-6, no dups, dates differ", () => {
  const sizes = new Set<number>();
  let differ = false;
  for (let d = 1; d <= 30; d++) {
    const ds = `2026-10-${String(d).padStart(2, "0")}`;
    const c = castForDate(ds, IDS);
    eq(JSON.stringify(c), JSON.stringify(castForDate(ds, IDS)));
    assert(c.length >= 4 && c.length <= 6);
    eq(new Set(c).size, c.length);
    sizes.add(c.length);
    if (JSON.stringify(c) !== JSON.stringify(castForDate("2026-10-01", IDS))) differ = true;
  }
  assert(differ);
  assert(sizes.size > 1);
});

Deno.test("validateDebate: 8-12 lines, speakers in cast, non-empty text", () => {
  assert(validateDebate(lines(8), names));
  assert(validateDebate(lines(12), names));
  assert(!validateDebate(lines(7), names));
  assert(!validateDebate(lines(13), names));
  assert(!validateDebate(lines(8, ["Nobody"]), names));
  const bad = lines(8); bad.lines[3].text = " ";
  assert(!validateDebate(bad, names));
});

Deno.test("buildDebatePrompt: names, claims, NO2 only when air", () => {
  const ps = ["a", "b", "c", "d"].map((s) => ({ ...mk(s), name: "N-" + s }));
  const air = { no2: 3.2e-5, interval: { from: "x", to: "y" } };
  const p = buildDebatePrompt(ps, air as never);
  for (const s of ["N-a", "PC-a", "D-d", "NO₂", "3.200e-5", "8 to 12", "JSON"]) assert(p.includes(s), s);
  assert(!buildDebatePrompt(ps, null).includes("CITY AIR"));
});

Deno.test("generateDebate: retry then success, double failure throws llm", async () => {
  let n = 0;
  const f = (() => Promise.resolve(new Response(JSON.stringify({ choices: [{ message: { content: n++ === 0 ? "garbage" : JSON.stringify(lines(9)) } }] })))) as unknown as typeof fetch;
  const ps = names.map((s) => ({ ...mk("x"), name: s }));
  eq((await generateDebate(ps, null, f)).lines.length, 9);
  eq(n, 2);
  const bad = (() => Promise.resolve(new Response("{}", { status: 500 }))) as unknown as typeof fetch;
  let err = "";
  try { await generateDebate(ps, null, bad); } catch (e) { err = (e as Error).message; }
  eq(err, "llm");
});

const req = (method = "POST", pw = "pw") => new Request("http://x/", { method, headers: { "x-theater-passcode": pw } });

Deno.test("handler: OPTIONS, auth, method", async () => {
  Deno.env.set("THEATER_PASSCODE", "pw");
  const h = makeHandler();
  eq((await h(new Request("http://x/", { method: "OPTIONS" }))).status, 204);
  eq((await h(req("POST", "bad"))).status, 401);
  eq((await h(req("GET"))).status, 405);
});

Deno.test("handler: cache hit short-circuits; <4 with data -> 503; success caches", async () => {
  const dir = await Deno.makeTempDir();
  Deno.env.set("THEATER_PASSCODE", "pw");
  Deno.env.delete("SUPABASE_URL");
  Deno.env.set("LOCAL_CACHE_DIR", dir);
  let ensures = 0, gens = 0;
  const base = {
    ensure: (a: { id: string }) => { ensures++; return Promise.resolve(mk(a.id)); },
    air: () => Promise.resolve(null),
    generate: (ps: { name: string }[]) => { gens++; return Promise.resolve(lines(9, ps.map((p) => p.name))); },
  };
  // only 3 agents with data
  const few = makeHandler({ ...base, ensure: (a: { id: string }) => Promise.resolve(a.id === "x" ? null : mk(a.id)) } as never, ["a0", "a1", "a2", "x"]);
  eq((await few(req())).status, 503);
  eq(gens, 0);
  // success with real agent ids
  const agents = (await import("../../data/agents.json", { with: { type: "json" } })).default as { id: string }[];
  const ids = agents.map((a) => a.id);
  const h = makeHandler(base as never, ids);
  const r = await h(req());
  eq(r.status, 200);
  const body = await r.json();
  assert(body.cast.length >= 4 && body.cast.length <= 6);
  assert(/^\d{4}-\d{2}-\d{2}$/.test(body.date));
  eq(gens, 1);
  const e1 = ensures;
  const r2 = await h(req());
  eq(JSON.stringify(await r2.json()), JSON.stringify(body));
  eq(gens, 1); eq(ensures, e1);
  // replacement: first agent in order has no data, still 200
  await Deno.remove(dir, { recursive: true });
  const dropped: string[] = [];
  const h3 = makeHandler({ ...base, ensure: (a: { id: string }) => { if (dropped.length === 0) { dropped.push(a.id); return Promise.resolve(null); } return Promise.resolve(mk(a.id)); } } as never, ids);
  const r3 = await h3(req());
  eq(r3.status, 200);
  assert(!(await r3.json()).cast.includes(dropped[0]));
});
