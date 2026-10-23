from src.agents.key_moments_agent import rank_key_moments
def build_match_report(result: dict) -> dict:
    """Combine workflow outputs into one structured match report."""
    analysis = result["match_analysis"]
    review = result["review_summary"]

    return {
        "report_title": "MatchMind AI — Match Intelligence Report",
        "teams": analysis["team_stats"],
        "analyst_analysis": result.get(
            "analyst_analysis",
            "Analyst analysis is unavailable.",
        ),
        "key_moments_summary": result.get(
            "key_moments_summary",
            "Key moments summary is unavailable.",
        ),
        "key_moments": rank_key_moments(result["key_moments"]),
        "verification": {
            "total_reviewed": review["total_reviewed"],
            "approved": review["approved"],
            "rejected": review["rejected"],
        },
        "workflow_trace": result.get("workflow_trace", []),
    }
