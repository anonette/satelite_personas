-- Haifa satellite personas: Supabase schema.
-- Run once in the Supabase SQL editor (Dashboard -> SQL Editor -> New query -> paste -> Run).

-- Daily response cache used by all four edge functions (read/written with the
-- service role key through the Supabase REST API: /rest/v1/daily_cache).
-- Keys look like "persona:technion:2026-10-14" (parts joined by ":" plus the UTC date).
-- Values: SpectralStats / Persona / Conflict objects as jsonb, or a base64 PNG string
-- for the NDVI overlay.
create table if not exists daily_cache (
  key text primary key,
  value jsonb,
  created_at timestamptz default now()
);

-- The edge functions use the service role key, which bypasses RLS. Enabling RLS with
-- no policies keeps the table closed to the browser (anon key).
alter table daily_cache enable row level security;

-- ---------------------------------------------------------------------------
-- STORAGE BUCKET "voice-cache" (audio cache, NOT created by this file)
--
-- The voice function stores generated mp3 files in a PRIVATE Storage bucket named
-- exactly:  voice-cache
-- Without it the voice function still works, but every play re-bills ElevenLabs.
--
-- Create it WITHOUT SQL, in the Supabase dashboard:
--   1. Open your project -> Storage (left sidebar).
--   2. Click "New bucket".
--   3. Name: voice-cache
--   4. Leave "Public bucket" OFF (private). Save.
--   No policies are needed: the function uses the service role key.
--
-- (SQL alternative, if you prefer:)
--   insert into storage.buckets (id, name, public) values ('voice-cache', 'voice-cache', false)
--   on conflict (id) do nothing;
-- ---------------------------------------------------------------------------
