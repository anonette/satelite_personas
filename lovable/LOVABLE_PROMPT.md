# Build prompt: Haifa Satellite Personas

Build a single-page web app (React, TypeScript, react-leaflet) called "Haifa Satellite Personas". 16 places in Haifa become characters. Each character is generated from real Sentinel-2 satellite statistics for its location, can argue with another character, and can speak aloud.

**Styling is yours.** All visual design, branding, colors, typography, spacing, iconography, animation and tone of the UI are entirely Lovable's to decide (the owner's explicit choice). This prompt specifies only structure, behavior and data contracts.

The attached `agents.json` is the list of 16 places. Embed it in the app as a static module. Each item has: `id`, `name_en`, `name_he`, `neighborhood`, `type`, `lat`, `lon`, `cultural_context`, `stats_bbox`. Never call any API to list agents.

## Backend

Four Supabase edge functions already exist. Base URL (placeholder, keep it in one constant / env var):

`https://<project-ref>.supabase.co/functions/v1`

Do NOT create new backend code and do NOT use the Supabase JS client for these calls. Use plain `fetch`. Send ONLY these headers: `x-theater-passcode: <passcode>` and, on POST, `Content-Type: application/json`. Do NOT send `Authorization` or `apikey` headers (CORS rejects them). All error bodies are JSON `{"error": "<code>"}`.

### 1. GET `/copernicus?action=stats&agent=<agentId>`
Returns:
```json
{ "ndvi": {"mean": 0.31, "min": -0.02, "max": 0.78},
  "bands": {"B02": 0.0, "B03": 0.0, "B04": 0.0, "B08": 0.0, "B11": 0.0, "B12": 0.0},
  "interval": {"from": "2026-09-14T00:00:00Z", "to": "2026-10-14T00:00:00Z"} }
```
Errors: 400 `unknown_agent`, 401 `passcode`, 503 `no_data`, 502 `upstream`.

### 2. GET `/copernicus?action=overlay`
Returns `image/png`: an NDVI colour image of the Haifa bounding box. Errors: 401 `passcode`, 502 `upstream`.
Because it needs the passcode header, you cannot put the URL in an `<img>` tag. Fetch it with the header, turn the response into a blob, and use `URL.createObjectURL` as the URL of a Leaflet `ImageOverlay`.

### 3. POST `/persona`   body `{"agentId": "<id>"}`
Returns:
```json
{ "agent_id": "technion", "name": "...", "hebrew_name": "...", "location": "...",
  "personality": "...", "monologue": "...",
  "challenges": [ {"target": "...", "line": "..."} ],
  "voice_hint": "..." }
```
Errors: 400 `unknown_agent`, 401 `passcode`, 405 `method`, 503 `no_data`, 502 `upstream`, 502 `llm`.
The persona response does not contain the satellite numbers; fetch them separately with endpoint 1 (same agent; it is cached server-side so it is cheap).

### 4. POST `/conflict`   body `{"agentA": "<id>", "agentB": "<id>"}`
Returns `{"lines": [ {"speaker": "<persona name>", "text": "..."} ]}` (2 to 4 lines). `speaker` equals the `name` field of one of the two personas, so map it back to the persona on stage by `name`.
Errors: 400 `bad_request` (missing ids or both the same), 401 `passcode`, 405 `method`, 409 `persona_missing`, 502 `llm`.
Both personas must have been generated (endpoint 3) before calling this.

### 5. POST `/voice`   body `{"agentId": "<id>", "text": "<text to speak>"}`
Returns `audio/mpeg` bytes. Errors: 400 `unknown_agent`, 400 `empty_text`, 401 `passcode`, 405 `method`, 502 `upstream`.
Play it by fetching with the header, reading the blob, `URL.createObjectURL`, and an `Audio` element. Revoke old object URLs.

## Layout

Split screen. **LEFT: map. RIGHT: theater feed.**

### Left: map
- `react-leaflet` with OpenStreetMap tiles. Fit the view to the Haifa bounding box `[west 34.95, south 32.75, east 35.10, north 32.85]` (Leaflet bounds `[[32.75, 34.95], [32.85, 35.10]]`).
- 16 clickable markers from `agents.json` at `lat`/`lon`. Each shows `name_en` and `name_he` (tooltip or popup, plus a visible selected state when its persona is on stage).
- A toggle "NDVI overlay". When switched on, fetch endpoint 2 and render it as an `ImageOverlay` over the same bounding box (`[[32.75, 34.95], [32.85, 35.10]]`) with sensible opacity. Show a small loading state while fetching; if it fails, switch the toggle back off and show the error message for that code.
- The map and all markers render WITHOUT the passcode. Only generating actions need it (including the overlay toggle).

### Right: theater feed
A scrolling feed of the "stage".
1. **Click a marker** -> show a loading card for that place -> call endpoint 3, and in parallel endpoint 1 -> the persona "enters the stage" as a card showing: `name`, `hebrew_name`, `location`, `personality`, `monologue`, and a "Satellite evidence" block with the real numbers it was built from: NDVI mean / min / max, the six band values (B02, B03, B04, B08, B11, B12), and the scene interval (`interval.from` to `interval.to`, shown as dates). If the persona call succeeds but the stats call fails, still show the persona and mark the evidence unavailable. Clicking a place already on stage just highlights its card.
2. Each persona card has a **play voice** button that sends the `monologue` to endpoint 5 with that persona's `agent_id`, with loading, playing and error states.
3. Personas on stage can be sent into **conflict**: let the user pick two personas on stage (e.g. a "Start conflict" action that asks for two) and call endpoint 4 with their two `agent_id`s as `agentA` and `agentB`. Render the returned `lines` as a dialogue (speaker name + text, alternating visually). Each line has its own **play voice** button: send the line's `text` to endpoint 5 with the `agent_id` of the persona whose `name` equals that line's `speaker`.
4. Personas can be removed from the stage. Keep the stage state in memory; generated results are cached server-side per day, so re-requesting is cheap.

## Passcode flow
- No passcode is needed to view the map and markers.
- On the first generating action (marker click, overlay toggle, conflict, voice) with no stored passcode, open a modal that asks for it once. Store it in `sessionStorage` (wrap access in try/catch) and send it as `x-theater-passcode` on every call to the endpoints above. Then continue the action the user started.
- Any 401 `{"error":"passcode"}` response: clear the stored passcode and re-prompt, with a short "wrong passcode" message, then retry the action.

## Error and loading states
Every generating action needs a visible loading state and a human-readable error, never a silent failure.
- 503 `no_data` -> "Satellite data unavailable for this location today."
- 502 `upstream` or `llm` -> "The service had a hiccup. Please try again." with a Retry button.
- 409 `persona_missing` -> "Generate both personas first: click each place on the map, then start the conflict."
- 400 `bad_request` -> "Pick two different personas."
- 401 `passcode` -> re-prompt as above.
- Network failure (fetch throws) -> same retry hint as 502.
- Voice 502 may mean the voice provider is temporarily unavailable; show the retry hint and keep the text readable.

## Hebrew and RTL
- Render every Hebrew string (`name_he`, `hebrew_name`, and any Hebrew inside monologues or lines) with `dir="auto"` (or `dir="rtl"` for pure Hebrew fields) and `lang="he"` where known, so mixed English/Hebrew text lays out correctly without flipping the surrounding UI.
- Use a font stack that includes a good Hebrew face. Keep punctuation and numbers correct in mixed text (use `<bdi>` for inline names).
- The overall app chrome stays LTR.

## Responsive
On narrow screens (mobile) the map collapses above the feed: a single column, map on top at a limited height, theater feed below it, scrolling normally. Marker taps must work by touch. The passcode modal and cards must be usable at 360px width.

## Not in scope
No accounts, no database access from the frontend, no new edge functions, no saving of personas by the user. The only secret the browser handles is the user-entered passcode.
