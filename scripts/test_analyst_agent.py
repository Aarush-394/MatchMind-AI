
import json

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from src.agents.analyst_agent import analyze_match_with_grok
from src.engine.match_engine import analyze_match


PROJECT_ROOT = Path(__file__).resolve().parent.parent

data_path = (
    PROJECT_ROOT / "data" / "synthetic" / "sample_match.json"
)

with data_path.open("r", encoding="utf-8") as file:
    match = json.load(file)

analysis = analyze_match(match["events"])

print(f"\nAnalyzing synthetic match: {match['home_team']} vs {match['away_team']}")
print("Sending match statistics to Grok...\n")

insight = analyze_match_with_grok(analysis)

print("=== GROK ANALYST REPORT ===\n")
print(insight)
