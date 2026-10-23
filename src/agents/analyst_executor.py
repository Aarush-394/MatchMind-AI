
from typing import Any

from agent_framework import Executor, WorkflowContext, handler



def generate_local_analysis(match_analysis: dict[str, Any]) -> str:
    """Compare team statistics using deterministic, local logic."""
    team_stats = match_analysis.get("team_stats", {})

    if not team_stats:
        return "Insufficient match statistics to generate an analysis."

    teams = sorted(team_stats.items())
    observations = [
        "Local Analyst Agent — evidence-based comparison:"
    ]

    for team, stats in teams:
        observations.append(
            f"{team}: {stats.get('possession_pct', 0)}% possession, "
            f"{stats.get('shots_on_target', 0)} shots on target, "
            f"{stats.get('pass_completion_pct', 0)}% pass completion."
        )

    if len(teams) >= 2:
        (team_a, stats_a), (team_b, stats_b) = teams[:2]

        possession_diff = round(
            stats_a.get("possession_pct", 0)
            - stats_b.get("possession_pct", 0),
            1,
        )

        shots_diff = (
            stats_a.get("shots_on_target", 0)
            - stats_b.get("shots_on_target", 0)
        )

        observations.append("\nStatistical comparison:")

        if possession_diff > 0:
            observations.append(
                f"{team_a} recorded {possession_diff} percentage "
                f"points more possession than {team_b}."
            )
        elif possession_diff < 0:
            observations.append(
                f"{team_b} recorded {abs(possession_diff)} percentage "
                f"points more possession than {team_a}."
            )
        else:
            observations.append("Both teams recorded equal possession.")

        if shots_diff > 0:
            observations.append(
                f"{team_a} recorded {shots_diff} more shots on target."
            )
        elif shots_diff < 0:
            observations.append(
                f"{team_b} recorded {abs(shots_diff)} more shots on target."
            )
        else:
            observations.append(
                "Both teams recorded the same number of shots on target."
            )

    observations.append(
        "\nThese are statistical comparisons, not proof of tactical "
        "causes or overall match superiority."
    )

    return "\n".join(observations)



class AnalystExecutor(Executor):
    @handler
    async def process(
        self,
        data: dict[str, Any],
        ctx: WorkflowContext,
    ) -> None:
        analysis = generate_local_analysis(data["match_analysis"])

        await ctx.send_message({
            **data,
            "analyst_analysis": analysis,
            "workflow_trace": (
                data["workflow_trace"] + ["Analyst Interpretation"]
            ),
        })
