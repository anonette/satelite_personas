"""
Export the 16 Haifa locations to lovable/data/agents.json.

Source modules:
  core/haifa/haifa_neighborhoods.py      -> HaifaNeighborhoods.LOCATIONS
  core/haifa/haifa_cultural_context.py   -> HaifaCulturalContext string data

HaifaCulturalContext has no per-location keys. Each location is matched to
context strings by explicit name aliases (case-insensitive substring match on
the full alias, so short tokens like "Port" are deliberately not used), plus
HAIFA_STEREOTYPES["by_neighborhood"] entries whose key equals the location's
name or neighborhood. Matches are joined with newlines; no match gives "".

Run from anywhere:
  ./vnv/Scripts/python.exe lovable/scripts/export_agents.py
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "agents.json"

sys.path.insert(0, str(REPO_ROOT))

from core.haifa.haifa_cultural_context import HaifaCulturalContext  # noqa: E402
from core.haifa.haifa_neighborhoods import HaifaNeighborhoods  # noqa: E402

# location name (as in HaifaLocation.name) -> aliases searched in context strings
CONTEXT_ALIASES = {
    "Baha'i Gardens": ["Baháʼí Gardens", "19 terraced gardens", "19 terraces"],
    "Haifa Port": ["Haifa Port"],
    "Wadi Nisnas": ["Wadi Nisnas"],
    "Wadi Salib": ["Wadi Salib"],
    "Carmel Center": ["Carmel Center"],
    "Technion": ["Technion"],
    "University of Haifa": ["University of Haifa"],
    "Haifa Bay Industrial Zone": ["Haifa Bay"],
    "Nesher Cement Factory": ["Nesher Cement"],
    "Bat Galim Beach": ["Bat Galim"],
    "Dado Beach": ["Dado Beach"],
    "Carmel National Park": ["Carmel National Park"],
    "Gan HaEm": ["Gan HaEm"],
    "Stella Maris Monastery": ["Stella Maris"],
    "Haifa Metronit Central": ["Metronit"],
    "Carmelit (Subway)": ["Carmelit"],
}


# neighborhood value on HaifaLocation -> by_neighborhood keys naming the same area
NEIGHBORHOOD_ALIASES = {
    "Port District": ["Port Area"],
}


def _iter_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for value in obj.values():
            yield from _iter_strings(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from _iter_strings(item)


def _all_context_strings():
    strings = []
    for attr, value in vars(HaifaCulturalContext).items():
        if attr.isupper() and isinstance(value, (dict, list)):
            strings.extend(_iter_strings(value))
    return strings


def _kebab_id(name):
    """'Baha'i Gardens' -> 'bahai-gardens', 'Carmelit (Subway)' -> 'carmelit-subway'."""
    cleaned = name.lower().replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", cleaned).strip("-")


def _neighborhood_context(name, neighborhood):
    """Entries in HAIFA_STEREOTYPES["by_neighborhood"] whose KEY equals the
    agent's neighborhood or location name, or a NEIGHBORHOOD_ALIASES entry for
    that neighborhood (case-insensitive)."""
    by_neighborhood = HaifaCulturalContext.HAIFA_STEREOTYPES["by_neighborhood"]
    wanted = {name.lower(), neighborhood.lower()}
    wanted.update(alias.lower() for alias in NEIGHBORHOOD_ALIASES.get(neighborhood, []))
    return [text for key, text in by_neighborhood.items() if key.lower() in wanted]


def _cultural_context(name, neighborhood, all_strings):
    aliases = [a.lower() for a in CONTEXT_ALIASES.get(name, [])]
    hits = [s for s in all_strings if any(a in s.lower() for a in aliases)]
    for text in _neighborhood_context(name, neighborhood):
        if text not in hits:
            hits.append(text)
    return "\n".join(hits)


def build_agents():
    all_strings = _all_context_strings()
    agents = []
    for loc in HaifaNeighborhoods.get_all_locations():
        agents.append({
            "id": _kebab_id(loc.name),
            "name_en": loc.name,
            "name_he": loc.name_hebrew,
            "neighborhood": loc.neighborhood,
            "type": loc.location_type,
            "lat": loc.latitude,
            "lon": loc.longitude,
            "cultural_context": _cultural_context(loc.name, loc.neighborhood, all_strings),
            "stats_bbox": [
                round(loc.longitude - 0.001, 6),
                round(loc.latitude - 0.001, 6),
                round(loc.longitude + 0.001, 6),
                round(loc.latitude + 0.001, 6),
            ],
        })
    return agents


def main():
    agents = build_agents()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(agents, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(agents)} agents to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
