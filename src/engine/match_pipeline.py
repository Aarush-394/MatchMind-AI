
from src.engine.match_engine import analyze_match
from src.engine.insight_formatter import format_match_insights
from src.agents.key_moments_agent import identify_key_moments
from src.agents.review_agent import review_key_moments
from src.utils.validation import validate_match_events


def run_match_pipeline(events: list[dict]) -> dict:
    """Run the local MatchMind AI analysis pipeline."""

    # Stage 1: Validate incoming events.
    errors = validate_match_events(events)

    if errors:
        raise ValueError("Invalid match events: " + "; ".join(errors))

    # Stage 2: Calculate statistics.
    match_analysis = analyze_match(events)

    # Stage 3: Identify significant moments.
    key_moments = identify_key_moments(
        events=events,
        match_analysis=match_analysis,
    )

    # Stage 4: Review the moments against the original dataset.
    review = review_key_moments(
        key_moments=key_moments,
        original_events=events,
    )

    # Stage 5: Assemble the verified results.
    pipeline_result = {
        "match_analysis": match_analysis,
        "key_moments": review["approved"],
        "rejected_moments": review["rejected"],
        "review_summary": {
            "total_reviewed": review["total_reviewed"],
            "approved": len(review["approved"]),
            "rejected": len(review["rejected"]),
        },
    }

    # Stage 6: Prepare dashboard-ready output.
    pipeline_result["formatted_insights"] = format_match_insights(
        pipeline_result
    )

    return pipeline_result
