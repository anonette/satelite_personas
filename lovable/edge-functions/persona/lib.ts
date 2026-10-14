import { checkPasscode } from "../_shared/auth.ts";
import { cacheGet, cacheSet, dailyKey } from "../_shared/cache.ts";
import { cors, json } from "../_shared/http.ts";
import { buildPersonaPrompt, type Challenge, type Persona } from "../_shared/prompts.ts";
import { type Agent, getStats } from "../copernicus/lib.ts";
import agentsData from "../../data/agents.json" with { type: "json" };

export type { Persona };
const AGENTS = agentsData as unknown as Agent[];

type LLMPersona = Omit<Persona, "agent_id">;

function str(v: unknown): string | null {
  return typeof v === "string" && v.trim() ? v : null;
}

/** Returns a valid persona (without agent_id) or null if malformed. */
export function validatePersona(raw: unknown): LLMPersona | null {
  if (!raw || typeof raw !== "object") return null;
  const o = raw as Record<string, unknown>;
  const name = str(o.name), hebrew_name = str(o.hebrew_name), location = str(o.location);
  const personality = str(o.personality), monologue = str(o.monologue), voice_hint = str(o.voice_hint);
  if (!name || !hebrew_name || !location || !personality || !monologue || !voice_hint) return null;
  const challenges: Challenge[] = [];
  if (o.challenges !== undefined) {
    if (!Array.isArray(o.challenges)) return null;
    for (const c of o.challenges) {
      const t = str((c as Record<string, unknown>)?.target), l = str((c as Record<string, unknown>)?.line);
      if (!t || !l) return null;
      challenges.push({ target: t, line: l });
    }
  }
  return { name, hebrew_name, location, personality, monologue, challenges, voice_hint };
}

async function attempt<T>(prompt: string, fetchFn: typeof fetch, validate: (raw: unknown) => T | null): Promise<T | null> {
  try {
    const res = await fetchFn("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${Deno.env.get("OPENAI_API_KEY") ?? ""}`,
      },
      body: JSON.stringify({
        model: Deno.env.get("OPENAI_MODEL") || "gpt-5-mini",
        response_format: { type: "json_object" },
        messages: [{ role: "user", content: prompt }],
      }),
    });
    if (!res.ok) { await res.body?.cancel(); return null; }
    const body = await res.json();
    const content = body?.choices?.[0]?.message?.content;
    if (typeof content !== "string") return null;
    return validate(JSON.parse(content));
  } catch {
    return null;
  }
}

/** One call plus one retry on malformed output; throws Error("llm") if both fail. */
export async function callJSON<T>(prompt: string, validate: (raw: unknown) => T | null, fetchFn: typeof fetch = fetch): Promise<T> {
  for (let i = 0; i < 2; i++) {
    const p = await attempt(prompt, fetchFn, validate);
    if (p) return p;
  }
  throw new Error("llm");
}

export function callLLM(prompt: string, fetchFn: typeof fetch = fetch): Promise<LLMPersona> {
  return callJSON(prompt, validatePersona, fetchFn);
}

export async function handler(req: Request): Promise<Response> {
  const pre = cors(req);
  if (pre) return pre;
  const denied = checkPasscode(req);
  if (denied) return denied;
  if (req.method !== "POST") return json({ error: "method" }, 405);
  let agentId = new URL(req.url).searchParams.get("agent") ?? "";
  if (!agentId) {
    try { agentId = String((await req.json())?.agentId ?? ""); } catch { /* ignore */ }
  }
  const agent = AGENTS.find((a) => a.id === agentId);
  if (!agent) return json({ error: "unknown_agent" }, 400);
  const key = dailyKey("persona", agentId);
  const hit = await cacheGet(key);
  if (hit) return json(hit);
  let stats;
  try {
    stats = await getStats(agent);
  } catch (e) {
    return json({ error: "upstream", message: String((e as Error).message ?? e) }, 502);
  }
  if (!stats) return json({ error: "no_data" }, 503);
  try {
    const persona: Persona = { agent_id: agentId, ...(await callLLM(buildPersonaPrompt(agent, stats))) };
    await cacheSet(key, persona);
    return json(persona);
  } catch {
    return json({ error: "llm" }, 502);
  }
}
