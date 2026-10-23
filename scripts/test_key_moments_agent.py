
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.engine.match_engine import analyze_match
from src.agents.key_moments_agent import identify_key_moments


data_path = PROJECT_ROOT / "data" / "synthetic" / "sample_match.json"

with data_path.open("r", encoding="utf-8") as file:
    match = json.load(file)

analysis = analyze_match(match["events"])

moments = identify_key_moments(
    events=match["events"],
    match_analysis=analysis,
)

print(f"\nKey moments: {match['home_team']} vs {match['away_team']}")
print("=" * 50)

for moment in moments:
    print(f"\nMinute: {moment['minute']}")
    print(f"Team: {moment['team']}")
    print(f"Event: {moment['description']}")
    print(f"Interpretation: {moment['interpretation']}")

print(f"\nTotal key moments identified: {len(moments)}")

assert len(moments) == 2
assert moments[0]["minute"] == 15
assert moments[1]["minute"] == 42

print("\nAll Key Moments Agent checks passed!")
