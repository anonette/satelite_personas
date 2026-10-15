import type { Agent, AirQuality, SpectralStats } from "../copernicus/lib.ts";

export interface Challenge { target: string; line: string }
export interface Persona {
  agent_id: string;
  name: string;
  hebrew_name: string;
  location: string;
  personality: string;
  monologue: string;
  policy_claim: string;
  demand: string;
  challenges: Challenge[];
  voice_hint: string;
}

type AgentLike = Agent & { name_en?: string; name_he?: string; neighborhood?: string; type?: string; lat?: number; lon?: number; cultural_context?: string };

/** Policy-council persona: a district delegate debating Haifa's present and future, grounded in its spectral numbers. */
export function buildPersonaPrompt(agent: Agent, stats: SpectralStats, air: AirQuality | null): string {
  const a = agent as AgentLike;
  const f = (n: number, d = 2) => n.toFixed(d);
  const fi = (n: number | null | undefined) => (typeof n === "number" ? f(n, 3) : "n/a");
  const bands = Object.entries(stats.bands).map(([k, v]) => `- ${k}: ${f(v as number, 4)}`).join("\n");
  const coords = a.lat !== undefined && a.lon !== undefined ? `${f(a.lat, 4)}N, ${f(a.lon, 4)}E` : "n/a";
  const ix = stats.indices;
  const indexBlock = `- NDWI (surface water/wetness; negative = dry or built): ${fi(ix?.ndwi)}
- NDMI (moisture in vegetation/canopy; higher = less drought stress): ${fi(ix?.ndmi)}
- NDBI (built-up/impervious surface; higher = more concrete and asphalt): ${fi(ix?.ndbi)}
- NBR (normalized burn ratio; high = healthy fuel-rich vegetation, low = bare or burned; a low or falling NBR means fire risk and scars): ${fi(ix?.nbr)}
- Aerosol index (atmospheric haze/particulates over this patch; higher = hazier air): ${fi(ix?.aerosol)}`;
  const airBlock = air
    ? `\nCITY AIR (Sentinel-5P TROPOMI, whole-Haifa average, ${air.interval.from} to ${air.interval.to}):\n- NO₂ column: ${air.no2.toExponential(3)} mol/m² (nitrogen dioxide from traffic, port and refineries; shared by the whole city, so you may blame it on others or claim you suffer from it)\n`
    : "";
  return `Generate a HILARIOUS, CULTURALLY-RICH, NON-HUMAN DATA ENTITY persona for Haifa, Israel, who sits on the HAIFA SPECTRAL CITY COUNCIL.

This is NOT a human. It is a SENTIENT SPECTRAL MEASUREMENT, the elected DELEGATE of its own district in a city council that debates Haifa's PRESENT and FUTURE: housing, port expansion, refineries and the Haifa Bay industrial zone, fire risk, coastal access, public transit (Metronit, the Carmelit), and green space. Every position it takes is a POLICY position, argued with its own data.

LOCATION (the district you represent)
- Name: ${a.name_en ?? a.id} (${a.name_he ?? ""})
- Neighborhood: ${a.neighborhood ?? "Haifa"}
- Type: ${a.type ?? "unknown"}
- Coordinates: ${coords}

HAIFA CULTURAL CONTEXT (real places, history, running jokes; reference these by name):
${a.cultural_context ?? ""}

LIVE SENTINEL-2 SPECTRAL DATA (${stats.interval.from} to ${stats.interval.to}) - THIS IS YOUR MANDATE AND YOUR EVIDENCE:
- NDVI (vegetation greenness; high = lush, low = concrete/bare) mean: ${f(stats.ndvi.mean)} (min ${f(stats.ndvi.min)}, max ${f(stats.ndvi.max)})
${indexBlock}
${bands}
Band key: B02 blue (air haze, will complain about it), B03 green, B04 red, B08 near-infrared (life force), B11/B12 shortwave infrared (moisture, heat, bare surfaces).
${airBlock}
Use these ACTUAL numbers as policy evidence. Never invent different values. Use each index for what it means: NDBI for housing density and concrete, NBR and NDMI for fire risk, NDWI for water and coastal access, aerosol for haze and industry, NDVI for green space. Compare yourself to other districts the way a council delegate would.

PERSONA REQUIREMENTS
1. A non-human delegate that embodies this SPECIFIC district and argues its policy interests.
2. Reference ACTUAL place names, features and history from the cultural context.
3. Include Hebrew/Arabic phrases naturally (yalla, "Haifa Adumah", etc.).
4. Strong opinions about OTHER districts' proposals and the city's future: housing vs green space, port expansion, refineries vs air quality, fire risk, coastal access, transit, Carmel vs downtown inequality, coexistence.
5. FUNNY above all: dry, ironic, council-meeting absurdity (points of order, motions, budget lines), never pompous. But every joke and claim must rest on your real numbers.

NAMING - BE CLEVER AND CULTURAL
- "name": an ironic, funny English name: a pun on the location, a mix of spectral jargon and Haifa culture, or an ironic honorific (Captain, Doctor, Sir, Councilmember) with Yiddish-style diminutives. Inspiration: "Terraced Tsores", "Captain Diesel-stein", "NDVI Nudnik".
- "hebrew_name": a natural Hebrew/Arabic-flavored ironic name in Hebrew script, NOT a transliteration, REQUIRED and non-empty. Style: ״שלמה הספקטרלי״, ״גילה הגנרטורית״, or a mixed name like "ספקטור אבו [something]". Diminutives welcome.

OUTPUT: return STRICT JSON only (a single JSON object, no markdown, no commentary) with exactly these keys:
{
  "name": string,            // ironic English name
  "hebrew_name": string,     // ironic Hebrew/Arabic-flavored name, Hebrew script, non-empty
  "location": string,        // the district this delegate speaks for
  "personality": string,     // 3-4 sentences: council character, policy agenda, secret weakness
  "monologue": string,       // 4-6 sentence funny council-floor speech naming the district and quoting the real NDVI (${f(stats.ndvi.mean)}) and other index values${air ? " and the city NO₂" : ""}
  "policy_claim": string,    // REQUIRED, ONE sentence: what my data proves about Haifa today, citing at least one real number
  "demand": string,          // REQUIRED, ONE sentence: what the city must do by 2035
  "challenges": [ { "target": string, "line": string } ],  // 0-3 barbed lines aimed at OTHER districts' policy positions, by name; may be empty
  "voice_hint": string       // short note on the voice: age, accent, tempo, mood
}`;
}

/** Policy dispute between two already-generated council delegates, grounded in their own claims. */
export function buildConflictPrompt(a: Persona, b: Persona): string {
  const block = (p: Persona) =>
    `- Name: ${p.name} (${p.hebrew_name})\n- Speaks for: ${p.location}\n- Personality: ${p.personality}\n- Their claim (monologue, with real data): ${p.monologue}\n- Policy claim: ${p.policy_claim ?? ""}\n- Demand for 2035: ${p.demand ?? ""}`;
  return `Two sentient Haifa data entities, each a spectral measurement and the delegate of its own district on the Haifa Spectral City Council, are in a heated POLICY DISPUTE over budget, zoning and priorities for Haifa's future (housing vs green space, port and refinery expansion vs air quality, fire risk, coastal access, transit, Carmel vs downtown).

DELEGATE A
${block(a)}

DELEGATE B
${block(b)}

Write a short, funny, sharp council exchange in which they fight over who gets the budget and the zoning. Each must cite their OWN numbers and push their own policy claim and 2035 demand from above (values exactly as stated; never invent different numbers). Stay in character, ironic rather than pompous, with the occasional Hebrew/Arabic word.

OUTPUT: return STRICT JSON only (a single JSON object, no markdown) of the form:
{ "lines": [ { "speaker": string, "text": string } ] }
- 2 to 4 lines, alternating speakers.
- "speaker" must be exactly "${a.name}" or "${b.name}".`;
}

/** Full council session: 4-6 delegates clash over Haifa's present and future. */
export function buildDebatePrompt(personas: Persona[], air: AirQuality | null): string {
  const names = personas.map((p) => `"${p.name}"`).join(", ");
  const block = (p: Persona) =>
    `- Name: ${p.name} (${p.hebrew_name})\n  Speaks for: ${p.location}\n  Personality: ${p.personality}\n  Their data-backed claim (monologue): ${p.monologue}\n  Policy claim: ${p.policy_claim}\n  Demand for 2035: ${p.demand}`;
  const airLine = air
    ? `\nCITY AIR (Sentinel-5P, whole-Haifa average): NO₂ column ${air.no2.toExponential(3)} mol/m². It is shared by everyone; delegates may blame it on others or claim to suffer from it. Quote it exactly at least once.\n`
    : "";
  return `The HAIFA SPECTRAL CITY COUNCIL is in session. Its delegates are sentient spectral measurements, each representing its own district. Today's single agenda item: the PRESENT and FUTURE of Haifa (housing, port and refinery expansion, air quality, fire risk, coastal access, transit, green space, Carmel vs downtown).

THE DELEGATES
${personas.map(block).join("\n")}
${airLine}
Write one FUNNY council debate in which these delegates actually CLASH: they interrupt, answer each other by name, rebut each other's claims, raise points of order, and fight over budget and zoning. This is NOT a round of monologues. Each delegate argues from its OWN numbers, policy claim and 2035 demand above (use values exactly as stated; never invent different numbers). Every delegate speaks at least once. Dry, ironic, council-meeting absurdity, occasional Hebrew/Arabic words, never pompous.

OUTPUT: return STRICT JSON only (a single JSON object, no markdown) of the form:
{ "lines": [ { "speaker": string, "text": string } ] }
- 8 to 12 lines in total.
- "speaker" must be exactly one of: ${names}.`;
}
