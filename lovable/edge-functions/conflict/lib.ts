import { checkPasscode } from "../_shared/auth.ts";
import { cacheGet, cacheSet, dailyKey } from "../_shared/cache.ts";
import { cors, json } from "../_shared/http.ts";
import { buildConflictPrompt, type Persona } from "../_shared/prompts.ts";
import { callJSON } from "../persona/lib.ts";

export interface ConflictLine { speaker: string; text: string }
export interface Conflict { lines: ConflictLine[] }

/** Order-independent: (A,B) and (B,A) share one entry. */
export function conflictKey(a: string, b: string): string {
  const [x, y] = [a, b].sort();
  return dailyKey("conflict", x, y);
}

export function validateConflict(raw: unknown, speakers: string[]): Conflict | null {
  const lines = (raw as { lines?: unknown })?.lines;
  if (!Array.isArray(lines) || lines.length < 2 || lines.length > 4) return null;
  const out: ConflictLine[] = [];
  for (const l of lines) {
    const speaker = (l as Record<string, unknown>)?.speaker, text = (l as Record<string, unknown>)?.text;
    if (typeof speaker !== "string" || !speakers.includes(speaker)) return null;
    if (typeof text !== "string" || !text.trim()) return null;
    out.push({ speaker, text });
  }
  return { lines: out };
}

/** One call plus one retry; throws Error("llm") if both fail. */
export function generateConflict(a: Persona, b: Persona, fetchFn: typeof fetch = fetch): Promise<Conflict> {
  return callJSON(buildConflictPrompt(a, b), (raw) => validateConflict(raw, [a.name, b.name]), fetchFn);
}

export async function handler(req: Request): Promise<Response> {
  const pre = cors(req);
  if (pre) return pre;
  const denied = checkPasscode(req);
  if (denied) return denied;
  if (req.method !== "POST") return json({ error: "method" }, 405);
  let agentA = "", agentB = "";
  try {
    const body = await req.json();
    agentA = String(body?.agentA ?? "");
    agentB = String(body?.agentB ?? "");
  } catch { /* ignore */ }
  if (!agentA || !agentB || agentA === agentB) return json({ error: "bad_request" }, 400);
  const key = conflictKey(agentA, agentB);
  const hit = await cacheGet(key);
  if (hit) return json(hit);
  const [pa, pb] = await Promise.all([
    cacheGet(dailyKey("persona", agentA)),
    cacheGet(dailyKey("persona", agentB)),
  ]) as [Persona | null, Persona | null];
  if (!pa || !pb) return json({ error: "persona_missing" }, 409);
  try {
    const result = await generateConflict(pa, pb);
    await cacheSet(key, result);
    return json(result);
  } catch {
    return json({ error: "llm" }, 502);
  }
}
