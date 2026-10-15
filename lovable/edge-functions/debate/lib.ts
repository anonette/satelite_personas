import { checkPasscode } from "../_shared/auth.ts";
import { cacheGet, cacheSet, dailyKey } from "../_shared/cache.ts";
import { cors, json } from "../_shared/http.ts";
import { buildDebatePrompt, type Persona } from "../_shared/prompts.ts";
import { callJSON, ensurePersona } from "../persona/lib.ts";
import { type Agent, type AirQuality, getAir } from "../copernicus/lib.ts";
import agentsData from "../../data/agents.json" with { type: "json" };

const AGENTS = agentsData as unknown as Agent[];
const MIN_CAST = 4;

export interface DebateLine { speaker: string; text: string }
export interface Debate { date: string; cast: string[]; lines: DebateLine[] }

function seedOf(s: string): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}

function mulberry32(a: number): () => number {
  return () => {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Deterministic seeded shuffle of ids; the full order is also the replacement queue. */
export function shuffleForDate(dateStr: string, ids: string[]): string[] {
  const rnd = mulberry32(seedOf(dateStr));
  const a = [...new Set(ids)];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rnd() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/** Cast of 4-6 distinct ids, fixed per date. */
export function castForDate(dateStr: string, ids: string[]): string[] {
  const size = Math.min(4 + (seedOf(dateStr) % 3), new Set(ids).size);
  return shuffleForDate(dateStr, ids).slice(0, size);
}

export function validateDebate(raw: unknown, castNames: string[]): { lines: DebateLine[] } | null {
  const lines = (raw as { lines?: unknown })?.lines;
  if (!Array.isArray(lines) || lines.length < 8 || lines.length > 12) return null;
  const out: DebateLine[] = [];
  for (const l of lines) {
    const speaker = (l as Record<string, unknown>)?.speaker, text = (l as Record<string, unknown>)?.text;
    if (typeof speaker !== "string" || !castNames.includes(speaker)) return null;
    if (typeof text !== "string" || !text.trim()) return null;
    out.push({ speaker, text });
  }
  return { lines: out };
}

export function generateDebate(personas: Persona[], air: AirQuality | null, fetchFn: typeof fetch = fetch): Promise<{ lines: DebateLine[] }> {
  const names = personas.map((p) => p.name);
  return callJSON(buildDebatePrompt(personas, air), (raw) => validateDebate(raw, names), fetchFn);
}

export interface Deps {
  ensure: (agent: Agent) => Promise<Persona | null>;
  air: () => Promise<AirQuality | null>;
  generate: (personas: Persona[], air: AirQuality | null) => Promise<{ lines: DebateLine[] }>;
}

const realDeps: Deps = { ensure: ensurePersona, air: () => getAir(), generate: (p, a) => generateDebate(p, a) };

export function makeHandler(deps: Deps = realDeps, ids: string[] = AGENTS.map((a) => a.id)) {
  return async (req: Request): Promise<Response> => {
    const pre = cors(req);
    if (pre) return pre;
    const denied = checkPasscode(req);
    if (denied) return denied;
    if (req.method !== "POST") return json({ error: "method" }, 405);
    const date = new Date().toISOString().slice(0, 10);
    const key = dailyKey("debate");
    const hit = await cacheGet(key);
    if (hit) return json(hit);

    const order = shuffleForDate(date, ids);
    const size = castForDate(date, ids).length;
    const personas: Persona[] = [];
    try {
      for (const id of order) {
        if (personas.length >= size) break;
        const agent = AGENTS.find((a) => a.id === id);
        if (!agent) continue;
        const p = await deps.ensure(agent);
        if (p) personas.push(p);
      }
    } catch (e) {
      const m = String((e as Error).message ?? e);
      if (m.startsWith("upstream:")) return json({ error: "upstream", message: m.slice(9) }, 502);
      return json({ error: "llm" }, 502);
    }
    if (personas.length < MIN_CAST) return json({ error: "no_data" }, 503);
    try {
      const { lines } = await deps.generate(personas, await deps.air());
      const result: Debate = { date, cast: personas.map((p) => p.agent_id), lines };
      await cacheSet(key, result);
      return json(result);
    } catch {
      return json({ error: "llm" }, 502);
    }
  };
}

export const handler = makeHandler();
