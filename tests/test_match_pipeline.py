
import json
from pathlib import Path

from src.engine.match_pipeline import run_match_pipeline


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "synthetic" / "sample_match.json"


def test_complete_match_pipeline():
    with DATA_PATH.open("r", encoding="utf-8") as file:
        match = json.load(file)

    result = run_match_pipeline(match["events"])

    assert "match_analysis" in result
    assert len(result["key_moments"]) == 2
    assert result["review_summary"]["approved"] == 2
    assert result["review_summary"]["rejected"] == 0


def test_pipeline_handles_empty_events():
    result = run_match_pipeline([])

    assert result["match_analysis"]["team_stats"] == {}
    assert result["key_moments"] == []
    assert result["review_summary"]["approved"] == 0
    assert result["review_summary"]["rejected"] == 0
