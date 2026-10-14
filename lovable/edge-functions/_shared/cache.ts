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
