
def format_match_insights(pipeline_result: dict) -> dict:
    """Convert verified pipeline output into dashboard-ready insights."""

    analysis = pipeline_result["match_analysis"]
    team_stats = analysis["team_stats"]
    key_moments = pipeline_result["key_moments"]

    teams = []

    for team, stats in team_stats.items():
        teams.append({
            "team": team,
            "passes": stats["passes"],
            "completed_passes": stats["completed_passes"],
            "pass_completion_pct": stats["pass_completion_pct"],
            "shots": stats["shots"],
            "shots_on_target": stats["shots_on_target"],
            "possession_pct": stats["possession_pct"],
        })

    teams.sort(key=lambda item: item["team"])

    timeline = [
        {
            "minute": moment["minute"],
            "team": moment["team"],
            "event": moment["description"],
            "status": moment["review_status"],
            "explanation": moment["interpretation"],
        }
        for moment in key_moments
    ]

    return {
        "teams": teams,
        "timeline": timeline,
        "review_summary": pipeline_result["review_summary"],
        "insight_count": len(timeline),
    }


def generate_tactical_takeaways(pipeline_result: dict) -> list[str]:
    """Generate basic, evidence-based takeaways from match statistics."""
    team_stats = pipeline_result["match_analysis"]["team_stats"]
    takeaways = []

    if not team_stats:
        return ["No team statistics are available for analysis."]

    teams = list(team_stats.items())

    if len(teams) >= 2:
        team_a, stats_a = teams[0]
        team_b, stats_b = teams[1]

        possession_a = stats_a["possession_pct"]
        possession_b = stats_b["possession_pct"]

        if possession_a > possession_b:
            takeaways.append(
                f"{team_a} recorded more possession "
                f"({possession_a}% vs {possession_b}%)."
            )
        elif possession_b > possession_a:
            takeaways.append(
                f"{team_b} recorded more possession "
                f"({possession_b}% vs {possession_a}%)."
            )
        else:
            takeaways.append("Both teams recorded equal possession.")

        shots_a = stats_a["shots_on_target"]
        shots_b = stats_b["shots_on_target"]

        if shots_a > shots_b:
            takeaways.append(
                f"{team_a} registered more shots on target "
                f"({shots_a} vs {shots_b})."
            )
        elif shots_b > shots_a:
            takeaways.append(
                f"{team_b} registered more shots on target "
                f"({shots_b} vs {shots_a})."
            )
        else:
            takeaways.append(
                "Both teams recorded the same number of shots on target."
            )

        accuracy_a = stats_a["pass_completion_pct"]
        accuracy_b = stats_b["pass_completion_pct"]

        if accuracy_a > accuracy_b:
            takeaways.append(
                f"{team_a} had the higher pass completion rate "
                f"({accuracy_a}% vs {accuracy_b}%)."
            )
        elif accuracy_b > accuracy_a:
            takeaways.append(
                f"{team_b} had the higher pass completion rate "
                f"({accuracy_b}% vs {accuracy_a}%)."
            )
        else:
            takeaways.append(
                "Both teams recorded the same pass completion rate."
            )

    return takeaways
