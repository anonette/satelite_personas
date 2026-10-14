import { checkPasscode } from "../_shared/auth.ts";
import { cacheGetBytes, cacheSetBytes, dailyKey } from "../_shared/cache.ts";
import { CORS_HEADERS, cors, json } from "../_shared/http.ts";
import { voiceFor } from "../_shared/voices.ts";
import agentsData from "../../data/agents.json" with { type: "json" };

const AGENTS = agentsData as unknown as { id: string; type: string }[];

export async function sha256hex(text: string): Promise<string> {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return Array.from(new Uint8Array(buf), (b) => b.toString(16).padStart(2, "0")).join("");
}

export async function voiceKey(agentId: string, text: string): Promise<string> {
  return dailyKey("voice", agentId, (await sha256hex(text)).slice(0, 16));
}

function audio(bytes: Uint8Array): Response {
  return new Response(bytes as BodyInit, { headers: { ...CORS_HEADERS, "Content-Type": "audio/mpeg" } });
}

export async function handler(req: Request): Promise<Response> {
  const pre = cors(req);
  if (pre) return pre;
  const denied = checkPasscode(req);
  if (denied) return denied;
  if (req.method !== "POST") return json({ error: "method" }, 405);
  let agentId = "", text = "";
  try {
    const b = await req.json();
    agentId = String(b?.agentId ?? "");
    text = typeof b?.text === "string" ? b.text : "";
  } catch { /* fall through to 400 */ }
  const agent = AGENTS.find((a) => a.id === agentId);
  if (!agent) return json({ error: "unknown_agent" }, 400);
  if (!text.trim()) return json({ error: "empty_text" }, 400);
  if (text.length > 1500) return json({ error: "text_too_long" }, 400);
  const key = await voiceKey(agentId, text);
  const hit = await cacheGetBytes(key);
  if (hit) return audio(hit);
  try {
    const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceFor(agent.type)}`, {
      method: "POST",
      headers: {
        "xi-api-key": Deno.env.get("ELEVENLABS_API_KEY") ?? "",
        "Content-Type": "application/json",
        Accept: "audio/mpeg",
      },
      body: JSON.stringify({ text, model_id: "eleven_multilingual_v2" }),
    });
    if (!res.ok) { await res.body?.cancel(); return json({ error: "upstream", status: res.status }, 502); }
    const bytes = new Uint8Array(await res.arrayBuffer());
    if (!bytes.length) return json({ error: "upstream" }, 502);
    await cacheSetBytes(key, bytes);
    return audio(bytes);
  } catch {
    return json({ error: "upstream" }, 502);
  }
}
