// Live smoke: deno run -A lovable/scripts/smoke_conflict.ts  (loads repo .env)
import { handler as personaHandler } from "../edge-functions/persona/lib.ts";
import { handler as conflictHandler } from "../edge-functions/conflict/lib.ts";

const envText = await Deno.readTextFile(new URL("../../.env", import.meta.url));
for (const line of envText.split(/\r?\n/)) {
  const m = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$/);
  if (m && !line.trim().startsWith("#")) Deno.env.set(m[1], m[2].replace(/^(['"])(.*)\1$/, "$2"));
}
const pass = "smoke-" + crypto.randomUUID();
Deno.env.set("THEATER_PASSCODE", pass);
Deno.env.delete("SUPABASE_URL");
Deno.env.set("LOCAL_CACHE_DIR", await Deno.makeTempDir());

let openaiCalls = 0;
const realFetch = globalThis.fetch;
globalThis.fetch = ((input: any, init?: any) => {
  const u = typeof input === "string" ? input : input instanceof URL ? input.href : input.url;
  if (u.includes("api.openai.com")) openaiCalls++;
  return realFetch(input, init);
}) as typeof fetch;

const hdr = { "x-theater-passcode": pass, "content-type": "application/json" };
const A = "bahai-gardens", B = "haifa-bay-industrial-zone";
let fail = false;

for (const id of [A, B]) {
  const r = await personaHandler(new Request("http://x/", { method: "POST", headers: hdr, body: JSON.stringify({ agentId: id }) }));
  console.log(`persona ${id}: ${r.status}`);
  if (r.status !== 200) fail = true;
  await r.body?.cancel();
}
const conflict = async (a: string, b: string) => {
  const r = await conflictHandler(new Request("http://x/", { method: "POST", headers: hdr, body: JSON.stringify({ agentA: a, agentB: b }) }));
  return { status: r.status, text: await r.text() };
};
let before = openaiCalls;
const first = await conflict(A, B);
console.log(`conflict status=${first.status} openaiCalls+=${openaiCalls - before}`);
const parsed = JSON.parse(first.text);
for (const l of parsed.lines ?? []) console.log(`${l.speaker}: ${l.text}`);
if (first.status !== 200 || openaiCalls - before !== 1 || !(parsed.lines.length >= 2 && parsed.lines.length <= 4)) fail = true;

before = openaiCalls;
const again = await conflict(B, A);
const same = again.text === first.text;
console.log(`reversed re-call: status=${again.status} identical=${same} openaiCalls before=${before} after=${openaiCalls}`);
if (again.status !== 200 || !same || openaiCalls !== before) fail = true;

console.log(fail ? "SMOKE FAIL" : "SMOKE OK");
Deno.exit(fail ? 1 : 0);
