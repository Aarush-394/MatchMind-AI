
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def analyze_match_with_grok(match_analysis: dict) -> str:
    """
    Generate an evidence-based football analysis using Grok.

    match_analysis should contain the output of our Python match engine.
    """

    api_key = os.getenv("XAI_API_KEY")
    base_url = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")
    model = os.getenv(
        "XAI_MODEL",
        "grok-4.20-0309-non-reasoning",
    )

    if not api_key:
        raise ValueError(
            "XAI_API_KEY is missing. Check your local .env file."
        )

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    evidence = json.dumps(match_analysis, indent=2)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the Analyst Agent in MatchMind AI. "
                    "Analyze the supplied synthetic football statistics. "
                    "Use only the provided evidence. Do not invent events, "
                    "players, scores, causes, or statistics. "
                    "Clearly distinguish observed facts from possible "
                    "interpretations. If evidence is insufficient, say so. "
                    "Write a concise analysis for a football analyst."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Analyze these match-engine results:\n"
                    f"{evidence}"
                ),
            },
        ],
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("Grok returned an empty analysis.")

    return content
