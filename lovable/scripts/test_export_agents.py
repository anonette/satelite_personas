import json
from pathlib import Path

AGENTS_PATH = Path(__file__).resolve().parents[1] / "data" / "agents.json"


def test_agents_json():
    data = json.loads(AGENTS_PATH.read_text(encoding="utf-8"))
    assert len(data) == 16
    port = next(a for a in data if a["id"] == "haifa-port")
    assert port["name_he"] == "נמל חיפה"
    assert port["stats_bbox"] == [34.989, 32.819, 34.991, 32.821]
    assert all(a["name_he"] and a["cultural_context"] is not None for a in data)


def test_neighborhood_keyed_context_included():
    data = {a["id"]: a for a in json.loads(AGENTS_PATH.read_text(encoding="utf-8"))}
    # by_neighborhood entries are keyed by neighborhood name, not by location text
    assert "Tel Aviv" in data["bat-galim-beach"]["cultural_context"]
    assert data["dado-beach"]["cultural_context"] != ""
    assert "Beach people" in data["dado-beach"]["cultural_context"]


if __name__ == "__main__":
    test_agents_json()
    print("test_agents_json passed")
