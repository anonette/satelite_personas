import { json } from "./http.ts";

/** Returns null when the passcode header matches THEATER_PASSCODE, else a 401 Response. */
export function checkPasscode(req: Request): Response | null {
  const expected = Deno.env.get("THEATER_PASSCODE");
  const given = req.headers.get("x-theater-passcode");
  if (expected && given !== null && given === expected) return null;
  return json({ error: "passcode" }, 401);
}
