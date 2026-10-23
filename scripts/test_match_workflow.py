
import asyncio
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.agents.match_workflow import build_match_workflow

DATA_PATH = PROJECT_ROOT / "data" / "synthetic" / "sample_match.json"


async def main():
    with DATA_PATH.open("r", encoding="utf-8") as file:
        match = json.load(file)

    workflow = build_match_workflow()
    result = await workflow.run(match["events"])

    outputs = result.get_outputs()

    print("\n=== MATCHMIND AI WORKFLOW RESULT ===")

    for output in outputs:
        print(output)

    assert outputs, "Workflow produced no outputs"

    final_result = outputs[-1]
    assert final_result["review_summary"]["approved"] == 2
    assert final_result["review_summary"]["rejected"] == 0

    print("\nWorkflow test passed!")


if __name__ == "__main__":
    asyncio.run(main())
