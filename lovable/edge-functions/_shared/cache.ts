/** Key = parts joined by ":" plus the UTC date (YYYY-MM-DD). */
export function dailyKey(...parts: string[]): string {
  return parts.join(":") + ":" + new Date().toISOString().slice(0, 10);
}

function supabase(): { url: string; key: string } | null {
  const url = Deno.env.get("SUPABASE_URL");
  const key = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  return url && key ? { url: url.replace(/\/+$/, ""), key } : null;
}

function localPath(dir: string, key: string): string {
  return `${dir.replace(/[\/]+$/, "")}/${encodeURIComponent(key)}.json`;
}

export async function cacheGet(key: string): Promise<unknown | null> {
  try {
    const sb = supabase();
    if (sb) {
      const res = await fetch(
        `${sb.url}/rest/v1/daily_cache?key=eq.${encodeURIComponent(key)}&select=value`,
        { headers: { apikey: sb.key, Authorization: `Bearer ${sb.key}` } },
      );
      if (!res.ok) { await res.body?.cancel(); return null; }
      const rows = await res.json();
      return Array.isArray(rows) && rows.length ? rows[0].value ?? null : null;
    }
    const dir = Deno.env.get("LOCAL_CACHE_DIR");
    if (!dir) return null;
    return JSON.parse(await Deno.readTextFile(localPath(dir, key)));
  } catch {
    return null;
  }
}

export async function cacheSet(key: string, value: unknown): Promise<void> {
  try {
    const sb = supabase();
    if (sb) {
      const res = await fetch(`${sb.url}/rest/v1/daily_cache`, {
        method: "POST",
        headers: {
          apikey: sb.key,
          Authorization: `Bearer ${sb.key}`,
          "Content-Type": "application/json",
          Prefer: "resolution=merge-duplicates",
        },
        body: JSON.stringify({ key, value, created_at: new Date().toISOString() }),
      });
      await res.body?.cancel();
      return;
    }
    const dir = Deno.env.get("LOCAL_CACHE_DIR");
    if (!dir) return;
    await Deno.mkdir(dir, { recursive: true });
    await Deno.writeTextFile(localPath(dir, key), JSON.stringify(value));
  } catch {
    // silent no-op
  }
}

const BUCKET = "voice-cache";

function binPath(dir: string, key: string): string {
  return `${dir.replace(/[\/]+$/, "")}/${encodeURIComponent(key)}.bin`;
}

export async function cacheGetBytes(key: string): Promise<Uint8Array | null> {
  try {
    const sb = supabase();
    if (sb) {
      const res = await fetch(`${sb.url}/storage/v1/object/${BUCKET}/${encodeURIComponent(key)}`, {
        headers: { apikey: sb.key, Authorization: `Bearer ${sb.key}` },
      });
      if (!res.ok) { await res.body?.cancel(); return null; }
      const bytes = new Uint8Array(await res.arrayBuffer());
      return bytes.length ? bytes : null;
    }
    const dir = Deno.env.get("LOCAL_CACHE_DIR");
    if (!dir) return null;
    return await Deno.readFile(binPath(dir, key));
  } catch {
    return null;
  }
}

export async function cacheSetBytes(key: string, bytes: Uint8Array): Promise<void> {
  try {
    const sb = supabase();
    if (sb) {
      const res = await fetch(`${sb.url}/storage/v1/object/${BUCKET}/${encodeURIComponent(key)}`, {
        method: "POST",
        headers: {
          apikey: sb.key,
          Authorization: `Bearer ${sb.key}`,
          "Content-Type": "audio/mpeg",
          "x-upsert": "true",
        },
        body: bytes as BodyInit,
      });
      await res.body?.cancel();
      return;
    }
    const dir = Deno.env.get("LOCAL_CACHE_DIR");
    if (!dir) return;
    await Deno.mkdir(dir, { recursive: true });
    await Deno.writeFile(binPath(dir, key), bytes);
  } catch {
    // silent no-op
  }
}
