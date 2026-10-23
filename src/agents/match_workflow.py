
from typing import Any
from src.agents.analyst_executor import AnalystExecutor
from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler

from src.engine.match_engine import analyze_match
from src.agents.key_moments_agent import (
    identify_key_moments,
    summarize_key_moments,
)
from src.agents.review_agent import review_key_moments
from src.utils.validation import validate_match_events


class ValidationExecutor(Executor):
    @handler
    async def process(
        self, events: list[dict[str, Any]], ctx: WorkflowContext
    ) -> None:
        errors = validate_match_events(events)

        if errors:
            raise ValueError(
                "Invalid match events: " + "; ".join(errors)
            )

        print("Workflow: input validation passed")

        await ctx.send_message({
            "events": events,
            "workflow_trace": ["Input Validation"],
        })


class StatisticsExecutor(Executor):
    @handler
    async def process(
        self, data: dict[str, Any], ctx: WorkflowContext
    ) -> None:
        analysis = analyze_match(data["events"])

        trace = data["workflow_trace"] + ["Match Statistics"]

        await ctx.send_message({
            **data,
            "match_analysis": analysis,
            "workflow_trace": trace,
        })


class KeyMomentsExecutor(Executor):
    @handler
    async def process(
        self, data: dict[str, Any], ctx: WorkflowContext
    ) -> None:
        moments = identify_key_moments(
            events=data["events"],
            match_analysis=data["match_analysis"],
        )
        key_moments_summary = summarize_key_moments(moments)
        trace = data["workflow_trace"] + ["Key Moment Identification"]

        await ctx.send_message({
            **data,
            "key_moments": moments,
            "key_moments_summary": key_moments_summary,
            "workflow_trace": (
                data["workflow_trace"] + ["Key Moment Identification"]
            ),
        })


class ReviewExecutor(Executor):
    @handler
    async def process(
        self, data: dict[str, Any], ctx: WorkflowContext
    ) -> None:
        review = review_key_moments(
            key_moments=data["key_moments"],
            original_events=data["events"],
        )

        output = {
            "analyst_analysis": data["analyst_analysis"],
            "match_analysis": data["match_analysis"],
            "key_moments": review["approved"],
            "rejected_moments": review["rejected"],
            "review_summary": {
                "total_reviewed": review["total_reviewed"],
                "approved": len(review["approved"]),
                "rejected": len(review["rejected"]),
            },
            "key_moments_summary": data["key_moments_summary"],
            "workflow_trace": (
                data["workflow_trace"] + ["Evidence Review"]
            ),
        }

        await ctx.yield_output(output)


def build_match_workflow():
    validation = ValidationExecutor(id="validation")
    statistics = StatisticsExecutor(id="statistics")
    analyst = AnalystExecutor(id="analyst")
    key_moments = KeyMomentsExecutor(id="key_moments")
    review = ReviewExecutor(id="review")

    return (
        WorkflowBuilder(start_executor=validation)
        .add_edge(validation, statistics)
        .add_edge(statistics, analyst)
        .add_edge(analyst, key_moments)
        .add_edge(key_moments, review)
        .build()
    )
