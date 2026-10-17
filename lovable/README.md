# Haifa Spectral City Council

A spectral theater. Sixteen places in Haifa (the port, the Baha'i Gardens, the Technion, the Carmelit, the cement factory at Nesher, and eleven more) are each given a voice. The voice is not a person. It is a satellite measurement, and it speaks in the first person, in a council chamber, about housing, refineries, fire risk, coastal access and the city's future.

The delegates get their opinions from live Copernicus data. Each one reads the numbers for its own patch of ground, then argues from them, usually with more confidence than the numbers deserve.

This folder is the "Lovable package": five Supabase edge functions, the agent list, and the prompts that put the frontend on top. If you are a colleague, a curator or a future contributor, this file explains what the data is, what each index means, and how the prompts keep the jokes tied to the measurements.

> Contains modified Copernicus Sentinel data (2026).

---

## The data

**Sentinel-2 L2A** is an optical satellite pair with 13 bands at 10 to 60 m resolution. It revisits Haifa every 2 to 5 days. For each of the 16 agents we request statistics over a small bounding box (`stats_bbox` in `data/agents.json`). The request uses a 30-day window with `mosaickingOrder: "leastCC"`, so it picks the least cloudy pixels, and `maxCloudCoverage: 60`. Haifa is sunny, but "no data today" is a real outcome, so the window is deliberately wide. The result is cached once per day.

**Sentinel-5P** (TROPOMI) measures atmospheric gases. We use the nitrogen dioxide (NO₂) column. Its pixels are about 5.5 km, so it cannot tell the port from the Carmel. We take one city-wide mean over the last 5 days. That is why every delegate shares the same NO₂ number and gets to blame it on someone else.

The same Sentinel-2 mosaic also feeds the map overlay: an NDVI colour ramp, or a true-colour image.

## The indices

An index is a ratio of two bands, which cancels out most of the lighting and leaves the contrast between them. The formulas below are copied from the evalscript in `edge-functions/copernicus/lib.ts`, the code that runs on the Copernicus servers.

### NDVI: vegetation

```js
let ndvi = (s.B08 - s.B04) / (s.B08 + s.B04);
```

Healthy leaves absorb red light (B04) for photosynthesis and reflect near-infrared (B08) strongly. Concrete, bare soil and water do not. NDVI therefore runs from negative (water) through near zero (concrete, rock) to about 0.6 and above (dense canopy).
*Dramatically:* the greenness delegate. Gan HaEm talks about it constantly. The port asks not to be quoted.

### NDWI: surface water and wetness

```js
ndwi: [(s.B03 - s.B08) / (s.B03 + s.B08)],
```

Water reflects green (B03) and swallows near-infrared (B08). Positive values mean water or very wet surfaces. Negative values mean dry ground, vegetation or buildings.
*Dramatically:* the coast delegates (Bat Galim, Dado Beach) argue for coastal access. Inland delegates mostly have to concede a negative number.

### NDMI: moisture in vegetation

```js
ndmi: [(s.B08 - s.B11) / (s.B08 + s.B11)],
```

Shortwave infrared (B11) is absorbed by leaf water, so the contrast with near-infrared tracks how much water the canopy holds. Higher means less drought stress. Low values over a green patch mean the plants look fine but are thirsty.
*Dramatically:* the dry-canopy delegate makes the fire-risk case, calmly, in a very small voice.

### NDBI: built-up surface

```js
ndbi: [(s.B11 - s.B08) / (s.B11 + s.B08)],
```

This is NDMI with the terms swapped. Bare and built surfaces reflect shortwave infrared (B11) more than they reflect near-infrared, while vegetation does the opposite. Higher NDBI means more concrete, asphalt and roofs.
*Dramatically:* the housing-density and zoning argument. High-NDBI delegates are told they are the problem, and say they are the solution.

### NBR: burn ratio

```js
nbr: [(s.B08 - s.B12) / (s.B08 + s.B12)],
```

Near-infrared (B08) is high in healthy, fuel-rich vegetation. Longer shortwave infrared (B12) rises on burned or bare ground. A high NBR means healthy fuel-rich vegetation. A low or falling NBR means bare or burned ground, and so scars and fire risk.
*Dramatically:* Mount Carmel still carries the 2010 fire. The Carmel National Park delegate has not forgotten and does not intend to let anyone else forget.

### B01 aerosol: atmospheric haze

```js
aerosol: [s.B01],
```

This one is not a ratio. B01 is the 60 m "coastal aerosol" band, in the deep blue and violet. It is very sensitive to particles in the air. We pass the raw reflectance through. Higher means hazier air over that patch, whether from dust, smoke or industry.
*Dramatically:* the Haifa Bay Industrial Zone and the port are suspiciously hazy and suspiciously unbothered.

### NO₂: nitrogen dioxide column

```js
return {no2: [s.NO2], dataMask: [s.dataMask]};
```

Again no ratio: we read the Sentinel-5P `NO2` band, a tropospheric column in mol/m². NO₂ comes from combustion: traffic, ships, power plants and refineries. It is a 5-day mean over all of Haifa, the same value for every delegate.
*Dramatically:* a shared grievance. The upwind delegate says the downwind one is exaggerating. The downwind one holds up the number.

The delegates also receive the mean of six raw bands (B02 blue, B03 green, B04 red, B08 near-infrared, B11 and B12 shortwave infrared). The prompt explains them: "B02 blue (air haze, will complain about it)".

## The prompts

All prompts live in `edge-functions/_shared/prompts.ts`. There are three. They rely on one idea: the model gets the real numbers inside the prompt and is told it may not change them. The humor is free. The numbers are not.

Quoted excerpts below come from `prompts.ts`.

### 1. Persona: one delegate per district

`buildPersonaPrompt` runs once per agent per day. It receives the agent's cultural context (real places and running jokes), the live Sentinel-2 stats, all the indices, and the city NO₂ if available. It asks for a strict JSON object: an ironic English name, an ironic Hebrew name, a personality, a monologue, a `policy_claim`, a `demand`, up to three `challenges` to other districts, and a voice hint.

**Council register.** The delegate is a sitting member, not a character in a story:

> This is NOT a human. It is a SENTIENT SPECTRAL MEASUREMENT, the elected DELEGATE of its own district in a city council that debates Haifa's PRESENT and FUTURE: housing, port expansion, refineries and the Haifa Bay industrial zone, fire risk, coastal access, public transit (Metronit, the Carmelit), and green space. Every position it takes is a POLICY position, argued with its own data.

**Grounding rule.** This is the line the rest of the design depends on:

> Use these ACTUAL numbers as policy evidence. Never invent different values. Use each index for what it means: NDBI for housing density and concrete, NBR and NDMI for fire risk, NDWI for water and coastal access, aerosol for haze and industry, NDVI for green space. Compare yourself to other districts the way a council delegate would.

**Funny but grounded:**

> 5. FUNNY above all: dry, ironic, council-meeting absurdity (points of order, motions, budget lines), never pompous. But every joke and claim must rest on your real numbers.

**Ironic naming.** The prompt asks for a name in two languages and says what to avoid:

> - "hebrew_name": a natural Hebrew/Arabic-flavored ironic name in Hebrew script, NOT a transliteration, REQUIRED and non-empty. Style: ״שלמה הספקטרלי״, ״גילה הגנרטורית״, or a mixed name like "ספקטור אבו [something]". Diminutives welcome.

The English side offers examples: "Terraced Tsores", "Captain Diesel-stein", "NDVI Nudnik". This is the project's house style: a pun, an honorific, a little Yiddish.

**`policy_claim` and `demand`.** These two fields turn a monologue into a debate position. They are short on purpose, and the debate prompt reuses them:

> "policy_claim": string,    // REQUIRED, ONE sentence: what my data proves about Haifa today, citing at least one real number
> "demand": string,          // REQUIRED, ONE sentence: what the city must do by 2035

### 2. Conflict: two delegates, one budget

`buildConflictPrompt` takes two already-generated personas and has them fight in 2 to 4 alternating lines. It repeats each delegate's own name, monologue, claim and demand, so the model does not have to invent anything about them:

> Write a short, funny, sharp council exchange in which they fight over who gets the budget and the zoning. Each pushes their own policy claim and 2035 demand from above. The audience already sees both delegates' data on screen: a line quotes AT MOST ONE of the speaker's OWN numbers (values exactly as stated; never invent different numbers), and jokes carry the rest. Stay in character, ironic rather than pompous, with the occasional Hebrew/Arabic word.

The output is `{ "lines": [ { "speaker": string, "text": string } ] }`, and `speaker` must be exactly one of the two delegates' names. Code checks this and retries if the model gets it wrong.

### 3. Debate: the full session

`buildDebatePrompt` seats 4 to 6 delegates and asks for 8 to 12 lines. The point is that it should not be a round of monologues:

> Write one FUNNY council debate in which these delegates actually CLASH: they interrupt, answer each other by name, rebut each other's claims, raise points of order, and fight over budget and zoning. This is NOT a round of monologues. Each delegate argues from its OWN numbers, policy claim and 2035 demand above (use values exactly as stated; never invent different numbers). Every delegate speaks at least once. Dry, ironic, council-meeting absurdity, occasional Hebrew/Arabic words, never pompous.

The numbers themselves mostly stay off the dialogue and on the screen — the UI shows every delegate's full index panel as gauges, so the prompt forbids data recitals:

> THE STAGE ALREADY SHOWS THE DATA. The audience watches this debate over a live satellite map with every delegate's full index panel on screen, so delegates NEVER recite lists of indices — a line like "NDVI 0.23, NDWI -0.270, NDMI 0.046" is a failure. A line may quote AT MOST ONE number, woven in the way a politician would say it ("my greenness is a sad 0.08", "half my district reflects like a parking lot").

When Sentinel-5P data is available, the prompt adds a shared-NO₂ line:

> It is shared by everyone; delegates may blame it on others or claim to suffer from it. At most ONE delegate quotes this exact number; the others just complain about the air in words.

**Who is in the room?** The cast is seeded by the date. In `debate/lib.ts`, the date string is hashed (FNV-1a) into a seed for a small deterministic generator (mulberry32), which shuffles the 16 agent ids and takes the first 4 to 6:

```ts
/** Cast of 4-6 distinct ids, fixed per date. */
export function castForDate(dateStr: string, ids: string[]): string[] {
  const size = Math.min(4 + (seedOf(dateStr) % 3), new Set(ids).size);
```

Everyone who opens the app on the same day sees the same council. The full shuffled order is also the replacement queue. If one district has no usable satellite data (cloud, outage), the next id in the order takes the seat. If fewer than 4 delegates can be seated, the function returns `no_data` and the app does not make up a debate.

## Architecture

Five Supabase edge functions (Deno/TypeScript), with the Lovable frontend as the stage:

| Function | Does |
|---|---|
| `copernicus` | Sentinel-2 stats per agent, Sentinel-5P NO₂, map overlays (NDVI ramp or true colour) |
| `persona` | Generates a delegate from its numbers, via an LLM |
| `conflict` | Two delegates, one budget fight |
| `debate` | The daily 4 to 6 delegate council session; also the session archive (GET lists past dates, GET `?date=` replays one) |
| `voice` | Text-to-speech for a delegate's lines (ElevenLabs), stored in a private bucket |

**Daily caching is the cost cap.** Every JSON result is stored in a `daily_cache` table under a key that includes the date; binary audio goes to the private `voice-cache` Supabase Storage bucket instead. In practice that means one cast and one debate per day, and audio generated at most once per distinct line per day, no matter how many people open the app. Copernicus processing units, LLM tokens and voice minutes are all bounded per day, not per visitor.

**Passcode gate.** Every function checks an `x-theater-passcode` header against the `THEATER_PASSCODE` secret and returns a 401 otherwise. It keeps a public exhibition link from becoming an open tap for anyone with a script.

**Session archive.** The day a council is convened, the `debate` function also writes a self-contained session bundle — the debate plus that day's personas, per-district stats and city NO₂ — under `session:<date>`, and keeps an index under `sessions:index`. Nothing in the cache is ever deleted, so every show the theater has ever played can be replayed exactly (`GET /debate?date=YYYY-MM-DD`), including with the satellite numbers it was argued from. Replays cost nothing: no LLM, no Copernicus call.

## Running it yourself

Everything in this folder runs locally with [Deno](https://deno.com) (no install step, no node_modules).

**Unit tests** (offline, no keys needed):

```sh
deno test -A lovable/edge-functions
```

**Live smoke tests** (hit the real APIs once each) need a `.env` in the repo root — never committed — with:

```
CDSE_CLIENT_ID=sh-...          # Copernicus Data Space OAuth client (free account at dataspace.copernicus.eu,
CDSE_CLIENT_SECRET=...         # then User settings -> OAuth clients)
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...         # only for the voice smoke
OPENAI_MODEL=gpt-5-mini        # optional, this is the default
```

Then, from the repo root:

```sh
deno run -A lovable/scripts/smoke_copernicus.ts   # real Sentinel-2 stats + overlay for one agent
deno run -A lovable/scripts/smoke_air.ts          # real Sentinel-5P NO2 over Haifa
deno run -A lovable/scripts/smoke_persona.ts      # generates two real personas
deno run -A lovable/scripts/smoke_conflict.ts     # a real two-delegate fight
deno run -A lovable/scripts/smoke_debate.ts       # convenes a full council session
deno run -A lovable/scripts/smoke_voice.ts        # one real ElevenLabs line
```

Each smoke uses a throwaway local cache directory, so it costs one real generation per run and leaves the deployed caches alone. Deploying the whole thing is `SETUP.md`.

## Where to go next

- `LOVABLE_PROMPT.md`: the build prompt for the Lovable frontend. It covers endpoints, layout, the council stage, the passcode flow and the loading states.
- `SETUP.md`: the checklist for deploying: the Supabase project, the cache table and bucket, the five functions, the secrets, and a smoke test.
- `data/agents.json`: the 16 agents (name, Hebrew name, bounding box, cultural context). Edit this to change who sits on the council.
- `edge-functions/_shared/prompts.ts`: the prompts above. If a delegate says something silly, start here.

Data: Contains modified Copernicus Sentinel data (2026).
