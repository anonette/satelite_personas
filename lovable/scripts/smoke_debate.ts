// Live smoke: deno run -A lovable/scripts/smoke_debate.ts  (loads repo .env)
import { handler } from "../edge-functions/debate/lib.ts";

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

const call = async () => {
  const r = await handler(new Request("http://x/", { method: "POST", headers: { "x-theater-passcode": pass } }));
  return { status: r.status, text: await r.text() };
};
let fail = false;
let before = openaiCalls;
const first = await call();
console.log(`status=${first.status} openaiCalls+=${openaiCalls - before}`);
const d = JSON.parse(first.text);
console.log(`date=${d.date}\ncast=${JSON.stringify(d.cast)}`);
for (const l of d.lines ?? []) console.log(`${l.speaker}: ${l.text}`);
if (first.status !== 200 || !(d.lines.length >= 8 && d.lines.length <= 12) || d.cast.length < 4) fail = true;

before = openaiCalls;
const again = await call();
console.log(`repeat: status=${again.status} identical=${again.text === first.text} openaiCalls before=${before} after=${openaiCalls}`);
if (again.status !== 200 || again.text !== first.text || openaiCalls !== before) fail = true;
console.log(fail ? "SMOKE FAIL" : "SMOKE OK");
Deno.exit(fail ? 1 : 0);
