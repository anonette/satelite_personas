# Setup checklist: Haifa satellite personas on Lovable + Supabase

Do these in order. Repo root: `C:\dev\satelite`, branch `haifa-lovable`, everything under `lovable/`.

## 1. Create the Lovable project
Create a new empty project at lovable.dev. Do not paste the prompt yet.

## 2. Enable the Supabase integration
In the Lovable project, connect Supabase (create or select a Supabase project). Note the **project ref** (the `xxxx` in `https://xxxx.supabase.co`). You will need it for the CLI and for the endpoint URLs.

## 3. Create the cache table
Supabase dashboard -> SQL Editor -> paste the contents of `lovable/supabase/schema.sql` -> Run. It creates `daily_cache`.

## 4. Create the private Storage bucket
Supabase dashboard -> Storage -> New bucket -> name `voice-cache`, "Public bucket" OFF -> Save. (Used to cache generated audio per day.)

## 5. Deploy the five edge functions
The functions import `../_shared/*.ts` and `../../data/agents.json` (`with { type: "json" }`). So the function folders, `_shared` and `data` must keep their relative positions. Recommended layout inside a `supabase/` folder (the Supabase CLI standard):

```
supabase/
  data/agents.json                <- copy of lovable/data/agents.json
  functions/
    _shared/                      <- copy of lovable/edge-functions/_shared/
    copernicus/                   <- copy of lovable/edge-functions/copernicus/
    persona/
    conflict/
    voice/
    debate/
```

From the repo root (PowerShell):

```powershell
New-Item -ItemType Directory -Force supabase\functions, supabase\data
Copy-Item lovable\data\agents.json supabase\data\agents.json
Copy-Item -Recurse -Force lovable\edge-functions\* supabase\functions\
```

(The copy also brings the `*_test.ts` files; they are harmless, delete them if you like.) The relative import `../../data/agents.json` from `supabase/functions/<name>/` resolves to `supabase/data/agents.json`, and `supabase functions deploy` bundles everything the entrypoint imports, including `_shared` and the JSON.

Then:

```powershell
supabase login
supabase link --project-ref <project-ref>
supabase functions deploy copernicus --no-verify-jwt
supabase functions deploy persona    --no-verify-jwt
supabase functions deploy conflict   --no-verify-jwt
supabase functions deploy voice      --no-verify-jwt
supabase functions deploy debate     --no-verify-jwt
```

`--no-verify-jwt` is required: the browser sends only the `x-theater-passcode` and `content-type` headers (the functions' CORS allow-list), not a Supabase JWT. Access is protected by the passcode instead. If a deploy cannot resolve the imports, add `--use-api` or deploy with Docker running.

## 6. Set the secrets
```powershell
supabase secrets set CDSE_CLIENT_ID=...
supabase secrets set CDSE_CLIENT_SECRET=...
supabase secrets set OPENAI_API_KEY=...
supabase secrets set ELEVENLABS_API_KEY=...
supabase secrets set THEATER_PASSCODE=...
# optional (default is gpt-5-mini):
supabase secrets set OPENAI_MODEL=gpt-5-mini
```
`SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are provided to edge functions automatically; do not set them. CDSE credentials are an OAuth client from the Copernicus Data Space (dataspace.copernicus.eu -> account -> OAuth clients).

Note: the ElevenLabs account is currently out of credits. Voice playback will return `502 {"error":"upstream"}` until it is topped up; everything else works.

## 7. Build the frontend in Lovable
Open `lovable/LOVABLE_PROMPT.md`, replace `<project-ref>` with your project ref, paste the whole text into the Lovable chat, and attach `lovable/data/agents.json`. Lovable decides all visual styling.

## 8. Smoke test
Replace `<ref>` and `<passcode>`:

```powershell
$h = @{ "x-theater-passcode" = "<passcode>" }
$b = "https://<ref>.supabase.co/functions/v1"
Invoke-RestMethod "$b/copernicus?action=stats&agent=technion" -Headers $h        # ndvi, bands, interval
Invoke-RestMethod "$b/persona" -Method Post -Headers $h -ContentType application/json -Body '{"agentId":"technion"}'
Invoke-RestMethod "$b/persona" -Method Post -Headers $h -ContentType application/json -Body '{"agentId":"wadi-nisnas"}'
Invoke-RestMethod "$b/conflict" -Method Post -Headers $h -ContentType application/json -Body '{"agentA":"technion","agentB":"wadi-nisnas"}'
Invoke-RestMethod "$b/copernicus?action=air" -Headers $h                        # no2, interval (503 no_data if unavailable)
Invoke-RestMethod "$b/debate" -Method Post -Headers $h -ContentType application/json -Body '{}'   # date, cast, lines; slow first call of the day, then cached
```
Without the header every call must return `401 {"error":"passcode"}`. Then open the Lovable preview: the map and markers show with no passcode; click a marker, enter the passcode when asked, and a persona should appear with its NDVI numbers.
