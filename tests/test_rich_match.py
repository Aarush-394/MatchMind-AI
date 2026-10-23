
import json
from pathlib import Path

from src.engine.match_pipeline import run_match_pipeline


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "synthetic" / "rich_sample_match.json"


def test_rich_match_pipeline():
    with DATA_PATH.open("r", encoding="utf-8") as file:
        match = json.load(file)

    result = run_match_pipeline(match["events"])

    assert len(result["match_analysis"]["team_stats"]) == 2
    assert result["review_summary"]["rejected"] == 0
    assert result["review_summary"]["approved"] == 4

    insights = result["formatted_insights"]
    assert insights["insight_count"] == 4
    assert len(insights["teams"]) == 2
