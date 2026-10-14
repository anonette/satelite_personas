// Live smoke: deno run -A lovable/scripts/smoke_voice.ts  (loads repo .env)
import { handler } from "../edge-functions/voice/lib.ts";

const envText = await Deno.readTextFile(new URL("../../.env", import.meta.url));
for (const line of envText.split(/\r?\n/)) {
  const m = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$/);
  if (m && !line.trim().startsWith("#")) Deno.env.set(m[1], m[2].replace(/^(['"])(.*)\1$/, "$2"));
}
const pass = "smoke-" + crypto.randomUUID();
Deno.env.set("THEATER_PASSCODE", pass);
Deno.env.delete("SUPABASE_URL");
Deno.env.set("LOCAL_CACHE_DIR", await Deno.makeTempDir());

let elCalls = 0;
const realFetch = globalThis.fetch;
globalThis.fetch = ((input: any, init?: any) => {
  const u = typeof input === "string" ? input : input instanceof URL ? input.href : input.url;
  if (u.includes("api.elevenlabs.io")) elCalls++;
  return realFetch(input, init);
}) as typeof fetch;

const out = (await Deno.makeTempDir()) + "/smoke_voice.mp3";
console.log("output:", out);
const call = () => handler(new Request("http://x/", {
  method: "POST",
  headers: { "x-theater-passcode": pass, "content-type": "application/json" },
  body: JSON.stringify({ agentId: "bahai-gardens", text: Deno.env.get("SMOKE_TEXT") ?? "Shalom, I am the greenest terrace in Haifa." }),
}));
let fail = false;
const r1 = await call();
const b1 = new Uint8Array(await r1.arrayBuffer());
await Deno.writeFile(out, b1);
const mp3 = (b1[0] === 0x49 && b1[1] === 0x44 && b1[2] === 0x33) || (b1[0] === 0xff && (b1[1] & 0xe0) === 0xe0);
console.log(`first: status=${r1.status} bytes=${b1.length} mp3header=${mp3} elCalls=${elCalls}`);
if (r1.status !== 200 || b1.length <= 5000 || !mp3 || elCalls !== 1) fail = true;
const r2 = await call();
const b2 = new Uint8Array(await r2.arrayBuffer());
const same = b2.length === b1.length && b2.every((v, i) => v === b1[i]);
console.log(`second: status=${r2.status} identical=${same} elCalls=${elCalls}`);
if (r2.status !== 200 || !same || elCalls !== 1) fail = true;
console.log(fail ? "SMOKE FAIL" : "SMOKE OK");
Deno.exit(fail ? 1 : 0);
