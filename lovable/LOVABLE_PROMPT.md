# Build prompt: Haifa Satellite Personas

Build a single-page web app (React, TypeScript, react-leaflet) called "Haifa Satellite Personas". 16 places in Haifa become characters. Each character is generated from real Sentinel-2 satellite statistics for its location, can argue with another character, and can speak aloud.

**Styling is yours.** All visual design, branding, colors, typography, spacing, iconography, animation and tone of the UI are entirely Lovable's to decide (the owner's explicit choice). This prompt specifies only structure, behavior and data contracts.

The attached `agents.json` is the list of 16 places. Embed it in the app as a static module. Each item has: `id`, `name_en`, `name_he`, `neighborhood`, `type`, `lat`, `lon`, `cultural_context`, `stats_bbox`. Never call any API to list agents.

## Backend

Five Supabase edge functions already exist. Base URL (placeholder, keep it in one constant / env var):

`https://<project-ref>.supabase.co/functions/v1`

Do NOT create new backend code and do NOT use the Supabase JS client for these calls. Use plain `fetch`. Send ONLY these headers: `x-theater-passcode: <passcode>` and, on POST, `Content-Type: application/json`. Do NOT send `Authorization` or `apikey` headers (CORS rejects them). All error bodies are JSON `{"error": "<code>"}`.

### 1. GET `/copernicus?action=stats&agent=<agentId>`
Returns:
```json
{ "ndvi": {"mean": 0.31, "min": -0.02, "max": 0.78},
  "bands": {"B02": 0.0, "B03": 0.0, "B04": 0.0, "B08": 0.0, "B11": 0.0, "B12": 0.0},
  "indices": {"ndwi": 0.0, "ndmi": 0.0, "ndbi": 0.0, "nbr": 0.0, "aerosol": 0.0},
  "interval": {"from": "2026-09-14T00:00:00Z", "to": "2026-10-14T00:00:00Z"} }
```
Each value in `indices` is a number or `null` (show "n/a" for null). Meaning: `ndwi` water, `ndmi` moisture, `ndbi` built-up, `nbr` burn/disturbance, `aerosol` haze (mean of Sentinel-2 band B01).
Errors: 400 `unknown_agent`, 401 `passcode`, 503 `no_data`, 502 `upstream`.

### 1b. GET `/copernicus?action=air`
City-wide Sentinel-5P nitrogen dioxide over the Haifa bounding box. Returns `{ "no2": 0.00005, "interval": {"from": "...", "to": "..."} }` (`no2` is a small mean value; show it scaled or in scientific notation, labelled "NO₂"). Errors: 401 `passcode`, 503 `no_data` (not available right now: hide the badge or show "NO₂ n/a"; this is not a blocking error). Fetch it once per session.

### 2. GET `/copernicus?action=overlay` (optionally `&kind=truecolor`)
Returns `image/png` of the Haifa bounding box. Default (no `kind`) is the NDVI colour ramp. `&kind=truecolor` returns the photographic true-colour image (the council stage backdrop). Errors: 401 `passcode`, 502 `upstream`.
Because it needs the passcode header, you cannot put the URL in an `<img>` tag. Fetch it with the header, turn the response into a blob, and use `URL.createObjectURL` as the URL of a Leaflet `ImageOverlay`.

### 3. POST `/persona`   body `{"agentId": "<id>"}`
Returns:
```json
{ "agent_id": "technion", "name": "...", "hebrew_name": "...", "location": "...",
  "personality": "...", "monologue": "...",
  "policy_claim": "...", "demand": "...",
  "challenges": [ {"target": "...", "line": "..."} ],
  "voice_hint": "..." }
```
Errors: 400 `unknown_agent`, 401 `passcode`, 405 `method`, 503 `no_data`, 502 `upstream`, 502 `llm`.
`policy_claim` is one sentence: what this place's data proves about Haifa today. `demand` is one sentence: what the city must do by 2035. Both are always present.
The persona response does not contain the satellite numbers; fetch them separately with endpoint 1 (same agent; it is cached server-side so it is cheap).

### 4. POST `/conflict`   body `{"agentA": "<id>", "agentB": "<id>"}`
Returns `{"lines": [ {"speaker": "<persona name>", "text": "..."} ]}` (2 to 4 lines). `speaker` equals the `name` field of one of the two personas, so map it back to the persona on stage by `name`.
Errors: 400 `bad_request` (missing ids or both the same), 401 `passcode`, 405 `method`, 409 `persona_missing`, 502 `llm`.
Both personas must have been generated (endpoint 3) before calling this.

### 5. POST `/voice`   body `{"agentId": "<id>", "text": "<text to speak>"}`
Returns `audio/mpeg` bytes. Errors: 400 `unknown_agent`, 400 `empty_text`, 400 `text_too_long` (text over 1500 characters; show a "Text too long to speak" message), 401 `passcode`, 405 `method`, 502 `upstream`.
Play it by fetching with the header, reading the blob, `URL.createObjectURL`, and an `Audio` element. Revoke old object URLs.

### 6. POST `/debate`   body `{}` (none needed)
Convenes today's council. Returns:
```json
{ "date": "2026-10-15", "cast": ["technion", "wadi-nisnas"],
  "lines": [ {"speaker": "<persona name>", "text": "..."} ] }
```
`cast` is 4 to 6 place ids; `lines` is 8 to 12 lines. `speaker` equals the `name` field of one of the cast personas (not an id). To map a speaker to a place, call endpoint 3 for each id in `cast` (cheap: the debate already generated them and they are cached) and match by `name`; then use that place's `lat`/`lon` from `agents.json`.
The debate is cached for the whole day: everyone gets the same debate all day, the first click of the day generates it (this can be slow, so show a clear "The council is convening..." loading state), and the cast changes each day. Say so in the UI ("Today's council", with the date).
Errors: 401 `passcode`, 405 `method`, 502 `llm`, 502 `upstream`, 503 `no_data`.

## Layout

Split screen. **LEFT: map. RIGHT: theater feed.**

### Left: map
- `react-leaflet` with OpenStreetMap tiles. Fit the view to the Haifa bounding box `[west 34.95, south 32.75, east 35.10, north 32.85]` (Leaflet bounds `[[32.75, 34.95], [32.85, 35.10]]`).
- 16 clickable markers from `agents.json` at `lat`/`lon`. Each shows `name_en` and `name_he` (tooltip or popup, plus a visible selected state when its persona is on stage).
- A toggle "NDVI overlay". When switched on, fetch endpoint 2 and render it as an `ImageOverlay` over the same bounding box (`[[32.75, 34.95], [32.85, 35.10]]`) with sensible opacity. Show a small loading state while fetching; if it fails, switch the toggle back off and show the error message for that code.
- The council stage (below) uses the true-colour overlay (`/copernicus?action=overlay&kind=truecolor`, fetched the same way as the NDVI one) as its backdrop.
- The map and all markers render WITHOUT the passcode. Only generating actions need it (including the overlay toggle).

### Right: theater feed
A scrolling feed of the "stage".
1. **Click a marker** -> show a loading card for that place -> call endpoint 3, and in parallel endpoint 1 -> the persona "enters the stage" as a card showing: `name`, `hebrew_name`, `location`, `personality`, `monologue`, and, prominently (this is a policy council, so these are the card's headline), its `policy_claim` ("What the data proves") and `demand` ("Demand for 2035"). Then a "Satellite evidence" block with the real numbers it was built from: NDVI mean / min / max, all five indices with short labels (NDWI water, NDMI moisture, NDBI built-up, NBR burn, Aerosol haze; null shown as "n/a"), the six band values (B02, B03, B04, B08, B11, B12), and the scene interval (`interval.from` to `interval.to`, shown as dates). If the persona call succeeds but the stats call fails, still show the persona and mark the evidence unavailable. Clicking a place already on stage just highlights its card.
   Above the feed (or in the header) show a city-wide **NO₂ badge** from `/copernicus?action=air`, with its date interval; hide it or show "NO₂ n/a" on 503.
2. Each persona card has a **play voice** button that sends the `monologue` to endpoint 5 with that persona's `agent_id`, with loading, playing and error states.
3. Personas on stage can be sent into **conflict**: let the user pick two personas on stage (e.g. a "Start conflict" action that asks for two) and call endpoint 4 with their two `agent_id`s as `agentA` and `agentB`. Render the returned `lines` as a dialogue (speaker name + text, alternating visually). Each line has its own **play voice** button: send the line's `text` to endpoint 5 with the `agent_id` of the persona whose `name` equals that line's `speaker`.
   **Challenges on entry (signature beat):** when a newly generated persona enters the stage and other personas are already on stage, use its `challenges` array. For each `{target, line}`, check whether `target` loosely matches any on-stage persona: case-insensitive substring match of `target` against that persona's `name` or `location` (either direction is fine, i.e. `target` contained in the field or the field contained in `target`). Render every matching `line` in the feed as an attack line attributed to the NEW persona (new persona's name, plus "to <matched persona's name>"), directly beneath its card. Challenges whose `target` matches no on-stage persona are NOT shown at all. These lines are a one-sided provocation only; the "Start conflict" action (endpoint 4, `/conflict`) remains the follow-up for a full two-sided exchange. If no other persona is on stage, show no challenges.
4. **Convene today's council** (button at the top of the feed): calls endpoint 6 and opens the council session view described under "The council stage". Show the date, the cast (names with `hebrew_name`), and a note that the same debate is shown all day and the cast changes daily.
5. Personas can be removed from the stage. Keep the stage state in memory; generated results are cached server-side per day, so re-requesting is cheap.

## The council stage (satellite as stage)
The council debate does NOT play in a plain text panel. It plays over the live satellite imagery: the city itself is the stage. This is the intended experience; exact animation, timing and styling are Lovable's choice.
- **Backdrop.** When the council is convened, the map switches to a stage mode with the true-colour overlay (`?action=overlay&kind=truecolor`) filling the Haifa bounding box as the backdrop (loading state while fetching; if it fails, fall back to the plain OSM map and still play the debate).
- **Speaker spotlight.** Lines play one after another. As each line is spoken, the map pans/zooms to the speaker's district (the `lat`/`lon` of the place whose persona `name` equals the line's `speaker`), that district's marker pulses, and the line appears as a speech bubble anchored at those coordinates (speaker name plus text, Hebrew with `dir="auto"`).
- **Stage lighting.** Between speakers the NDVI overlay (default `kind`) can cross-fade in and back out, so the city's data becomes the lighting of the scene.
- **Speaker tint.** A subtle colour tint over the stage per speaker, keyed to that place's dominant index from its stats (endpoint 1): green for vegetation districts (high NDVI), rust for built-up or industrial districts (high NDBI), blue for water or coast (high NDWI). If stats are unavailable use no tint.
- **Playback controls.** Lines advance automatically on a timer (long enough to read), with Pause/Resume, Next and Previous controls and a progress indicator. Each line may keep a play-voice button (endpoint 5, with the speaker's `agent_id`). At the end offer Replay and a way back to the normal map. The full transcript stays available as a list.
- The stage needs no new backend: it combines endpoints 1, 2, 3 and 6 with `agents.json` coordinates.

## Passcode flow
- No passcode is needed to view the map and markers.
- On the first generating action (marker click, overlay toggle, conflict, voice, convening the council) with no stored passcode, open a modal that asks for it once. Store it in `sessionStorage` (wrap access in try/catch) and send it as `x-theater-passcode` on every call to the endpoints above. Then continue the action the user started.
- Any 401 `{"error":"passcode"}` response: clear the stored passcode and re-prompt, with a short "wrong passcode" message, then retry the action.

## Error and loading states
Every generating action needs a visible loading state and a human-readable error, never a silent failure.
- 503 `no_data` -> "Satellite data unavailable for this location today."
- 502 `upstream` or `llm` -> "The service had a hiccup. Please try again." with a Retry button.
- 409 `persona_missing` -> "Generate both personas first: click each place on the map, then start the conflict."
- 400 `bad_request` -> "Pick two different personas."
- 401 `passcode` -> re-prompt as above.
- Network failure (fetch throws) -> same retry hint as 502.
- Debate 502 `llm`/`upstream` -> the same retry message with a Retry button; 503 `no_data` -> "Satellite data unavailable for today's council. Try again later."
- Voice 502 may mean the voice provider is temporarily unavailable; show the retry hint and keep the text readable.

## Hebrew and RTL
- Render every Hebrew string (`name_he`, `hebrew_name`, and any Hebrew inside monologues or lines) with `dir="auto"` (or `dir="rtl"` for pure Hebrew fields) and `lang="he"` where known, so mixed English/Hebrew text lays out correctly without flipping the surrounding UI.
- Use a font stack that includes a good Hebrew face. Keep punctuation and numbers correct in mixed text (use `<bdi>` for inline names).
- The overall app chrome stays LTR.

## Responsive
On narrow screens (mobile) the map collapses above the feed: a single column, map on top at a limited height, theater feed below it, scrolling normally. Marker taps must work by touch. The passcode modal and cards must be usable at 360px width.

## Not in scope
No accounts, no database access from the frontend, no new edge functions, no saving of personas by the user. The only secret the browser handles is the user-entered passcode.
