import type { Agent, SpectralStats } from "../copernicus/lib.ts";

export interface Challenge { target: string; line: string }
export interface Persona {
  agent_id: string;
  name: string;
  hebrew_name: string;
  location: string;
  personality: string;
  monologue: string;
  challenges: Challenge[];
  voice_hint: string;
}

type AgentLike = Agent & { name_en?: string; name_he?: string; neighborhood?: string; type?: string; lat?: number; lon?: number; cultural_context?: string };

/** Ported from core/haifa/haifa_persona_generator.py, with a strict-JSON output contract. */
export function buildPersonaPrompt(agent: Agent, stats: SpectralStats): string {
  const a = agent as AgentLike;
  const f = (n: number, d = 2) => n.toFixed(d);
  const bands = Object.entries(stats.bands).map(([k, v]) => `- ${k}: ${f(v as number, 4)}`).join("\n");
  const coords = a.lat !== undefined && a.lon !== undefined ? `${f(a.lat, 4)}N, ${f(a.lon, 4)}E` : "n/a";
  return `Generate a HILARIOUS, CULTURALLY-RICH, NON-HUMAN DATA ENTITY persona for Haifa, Israel.

This is NOT a human. It is a SENTIENT SPECTRAL MEASUREMENT that has absorbed Haifa's culture and is an opinionated environmental activist for its own patch of the city.

LOCATION
- Name: ${a.name_en ?? a.id} (${a.name_he ?? ""})
- Neighborhood: ${a.neighborhood ?? "Haifa"}
- Type: ${a.type ?? "unknown"}
- Coordinates: ${coords}

HAIFA CULTURAL CONTEXT (real places, history, running jokes; reference these by name):
${a.cultural_context ?? ""}

LIVE SENTINEL-2 SPECTRAL DATA (${stats.interval.from} to ${stats.interval.to}) - THIS IS THEIR IDENTITY:
- NDVI mean: ${f(stats.ndvi.mean)} (min ${f(stats.ndvi.min)}, max ${f(stats.ndvi.max)})
${bands}
Band key: B02 blue (air haze, will complain about it), B03 green, B04 red, B08 near-infrared (life force), B11/B12 shortwave infrared (moisture, heat, bare surfaces).
Use these ACTUAL numbers as proof of superiority or inferiority. Never invent different values. High NDVI looks down on low NDVI (concrete); low NDVI blames someone else.

PERSONA REQUIREMENTS
1. A non-human entity that embodies this SPECIFIC location.
2. Reference ACTUAL place names, features and history from the cultural context.
3. Include Hebrew/Arabic phrases naturally (yalla, "Haifa Adumah", etc.).
4. Strong opinions about other Haifa locations. Competing environmental priorities: air quality vs jobs, tourism vs local life, gentrification, Carmel vs downtown elevation inequality, coexistence, development vs preservation.
5. DRAMATIC, OPINIONATED, slightly ABSURD, but IRONIC rather than pompous.

NAMING - BE CLEVER AND CULTURAL
- "name": an ironic, funny English name: a pun on the location, a mix of spectral jargon and Haifa culture, or an ironic honorific (Captain, Doctor, Sir) with Yiddish-style diminutives. Inspiration: "Terraced Tsores", "Captain Diesel-stein", "NDVI Nudnik".
- "hebrew_name": a natural Hebrew/Arabic-flavored ironic name in Hebrew script, NOT a transliteration, REQUIRED and non-empty. Style: ״שלמה הספקטרלי״, ״גילה הגנרטורית״, or a mixed name like "ספקטור אבו [something]". Diminutives welcome.

OUTPUT: return STRICT JSON only (a single JSON object, no markdown, no commentary) with exactly these keys:
{
  "name": string,            // ironic English name
  "hebrew_name": string,     // ironic Hebrew/Arabic-flavored name, Hebrew script, non-empty
  "location": string,        // the place this persona speaks for
  "personality": string,     // 3-4 sentences: activist character, agenda, secret weakness
  "monologue": string,       // 4-6 sentence passionate rant naming the location and quoting the real NDVI (${f(stats.ndvi.mean)}) and band values
  "challenges": [ { "target": string, "line": string } ],  // 0-3 barbed lines aimed at OTHER Haifa places by name; may be empty
  "voice_hint": string       // short note on the voice: age, accent, tempo, mood
}`;
}

/** Argument between two already-generated personas, grounded in their own claims. */
export function buildConflictPrompt(a: Persona, b: Persona): string {
  const block = (p: Persona) =>
    `- Name: ${p.name} (${p.hebrew_name})\n- Speaks for: ${p.location}\n- Personality: ${p.personality}\n- Their claim (monologue, with real data): ${p.monologue}`;
  return `Two sentient Haifa data entities, each a spectral measurement of its own patch of the city, are having a heated argument about competing environmental priorities (air quality vs jobs, green space vs development, Carmel vs downtown, etc.).

ENTITY A
${block(a)}

ENTITY B
${block(b)}

Write a short, funny, sharp exchange in which they argue their competing environmental priorities. Each must reference their REAL data and places from the claims above (NDVI and band values as stated; never invent different numbers). Stay in character, ironic rather than pompous, with the occasional Hebrew/Arabic word.

OUTPUT: return STRICT JSON only (a single JSON object, no markdown) of the form:
{ "lines": [ { "speaker": string, "text": string } ] }
- 2 to 4 lines, alternating speakers.
- "speaker" must be exactly "${a.name}" or "${b.name}".`;
}
