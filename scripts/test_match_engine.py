
import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from src.engine.match_engine import analyze_match


project_root = Path(__file__).resolve().parent.parent
data_path = project_root / "data" / "synthetic" / "sample_match.json"

with data_path.open("r", encoding="utf-8") as file:
    match = json.load(file)

result = analyze_match(match["events"])

print(f"\nMatch: {match['home_team']} vs {match['away_team']}")
print("=" * 45)

for team, stats in result["team_stats"].items():
    print(f"\n{team}")
    print(f"  Passes: {stats['passes']}")
    print(f"  Completed passes: {stats['completed_passes']}")
    print(f"  Pass completion: {stats['pass_completion_pct']}%")
    print(f"  Shots: {stats['shots']}")
    print(f"  Shots on target: {stats['shots_on_target']}")
    print(f"  Possession: {stats['possession_pct']}%")

print("\nSignificant moments:")
for event in result["significant_events"]:
    print(f"  {event['minute']}' - {event['description']}")
