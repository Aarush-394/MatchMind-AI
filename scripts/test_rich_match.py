
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.agents.match_workflow import build_match_workflow
from src.engine.insight_formatter import format_match_insights


DATA_PATH = (
    PROJECT_ROOT / "data" / "synthetic" / "rich_sample_match.json"
)


async def run_test():
    with DATA_PATH.open("r", encoding="utf-8") as file:
        match = json.load(file)

    workflow = build_match_workflow()
    execution_result = await workflow.run(match["events"])
    outputs = execution_result.get_outputs()

    assert outputs, "Workflow produced no output"

    result = outputs[-1]
    result["formatted_insights"] = format_match_insights(result)
    final_result = result

    insights = result["formatted_insights"]

    print(f"\nMatch: {match['home_team']} vs {match['away_team']}")
    print(f"Total synthetic events: {len(match['events'])}")
    print(f"Teams analyzed: {len(insights['teams'])}")
    print(f"Significant moments: {insights['insight_count']}")
    print(f"Review summary: {insights['review_summary']}")

    print("\nTeam statistics:")
    for team in insights["teams"]:
        print(
            f"{team['team']}: "
            f"{team['passes']} passes, "
            f"{team['pass_completion_pct']}% completion, "
            f"{team['shots']} shots, "
            f"{team['possession_pct']}% recorded possession"
        )

    assert len(insights["teams"]) == 2
    assert insights["review_summary"]["rejected"] == 0
    assert insights["review_summary"]["approved"] == insights["insight_count"]
    

    print("\nRich synthetic match workflow passed!")
    assert "analyst_analysis" in final_result
    assert "Arsenal" in final_result["analyst_analysis"]
    assert "Chelsea" in final_result["analyst_analysis"]
    assert result["analyst_analysis"]
    assert result["key_moments_summary"]
    assert len(result["workflow_trace"]) == 5

    assert result["workflow_trace"] == [
        "Input Validation",
        "Match Statistics",
        "Analyst Interpretation",
        "Key Moment Identification",
        "Evidence Review",
    ]

    print("Agent outputs and workflow handoffs verified.")
    print("Analyst output successfully preserved in workflow.")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_test())
