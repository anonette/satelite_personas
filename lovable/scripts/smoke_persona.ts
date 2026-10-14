// Live smoke: deno run -A lovable/scripts/smoke_persona.ts  (loads repo .env)
import { handler } from "../edge-functions/persona/lib.ts";

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

// Count OpenAI calls by wrapping fetch.
let openaiCalls = 0;
const realFetch = globalThis.fetch;
globalThis.fetch = ((input: any, init?: any) => {
  const u = typeof input === "string" ? input : input instanceof URL ? input.href : input.url;
  if (u.includes("api.openai.com")) openaiCalls++;
  return realFetch(input, init);
}) as typeof fetch;

const server = Deno.serve({ port: 0, onListen: () => {} }, handler);
const base = `http://127.0.0.1:${server.addr.port}/`;
const call = async (id: string) => {
  const r = await realFetch(base, {
    method: "POST",
    headers: { "x-theater-passcode": pass, "content-type": "application/json" },
    body: JSON.stringify({ agentId: id }),
  });
  return { status: r.status, text: await r.text() };
};

let fail = false;
const out: Record<string, string> = {};
for (const id of ["bahai-gardens", "haifa-bay-industrial-zone"]) {
  const before = openaiCalls;
  const r = await call(id);
  console.log(`== ${id} status=${r.status} openaiCalls+=${openaiCalls - before}`);
  console.log(JSON.stringify(JSON.parse(r.text), null, 2));
  const p = JSON.parse(r.text);
  if (r.status !== 200 || !p.hebrew_name || !/[֐-׿]/.test(p.hebrew_name)) { fail = true; console.log("  UNEXPECTED"); }
  out[id] = r.text;
}
if (out["bahai-gardens"] === out["haifa-bay-industrial-zone"]) fail = true;

const before = openaiCalls;
const again = await call("bahai-gardens");
const identical = again.text === out["bahai-gardens"];
console.log(`cache re-call: status=${again.status} identical=${identical} openaiCalls before=${before} after=${openaiCalls}`);
if (!identical || openaiCalls !== before) fail = true;

await server.shutdown();
console.log(fail ? "SMOKE FAIL" : "SMOKE OK");
Deno.exit(fail ? 1 : 0);
