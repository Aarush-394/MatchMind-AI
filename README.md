# MatchMind AI — Beyond the Scoreline

**Every pass tells a story. Every moment has a meaning.**

MatchMind AI is an explainable, multi-agent football match intelligence system built to go beyond the scoreline. It analyzes match events, compares team statistics, identifies important moments, verifies evidence, and generates personalized team briefings through an interactive dashboard.

## Features

- **Match Statistics:** Calculate pass completion, shots, shots on target, and possession.
- **Analyst Agent:** Generate evidence-based comparisons between teams.
- **Key Moments Agent:** Identify significant events and rank them by priority.
- **Evidence Review:** Verify identified moments against the original match data.
- **Tactical Takeaways:** Produce deterministic comparisons from available statistics.
- **Personalized Briefings:** Explore statistics and key moments for a selected team.
- **Match Intelligence Reports:** View and download structured reports in JSON format.
- **Multi-Agent Workflow:** Coordinate validation, statistics, analysis, key-moment identification, and evidence review.
- **Interactive Dashboard:** Explore match insights using Streamlit.

## Technology Stack

- Python
- Microsoft Agent Framework
- Streamlit
- Pandas
- pytest and pytest-asyncio
- OpenAI-compatible client for optional xAI Grok integration

## Architecture

The match analysis workflow follows these stages:

1. **Input Validation** — Validate the structure and values of match events.
2. **Match Statistics** — Calculate team-level match statistics.
3. **Analyst Interpretation** — Generate evidence-based statistical comparisons.
4. **Key Moment Identification** — Extract significant events and summarize them.
5. **Evidence Review** — Check identified moments against the original dataset.

The system also provides key-moment ranking, tactical takeaways, personalized team briefings, and downloadable match reports.

## Getting Started

### Prerequisites

- Python 3.12 or a compatible Python version
- Git

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/MatchMind-AI.git
cd MatchMind-AI
```

Replace `YOUR-USERNAME` with the GitHub account that owns the repository.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Launch the dashboard

```powershell
python -m streamlit run src/dashboard.py
```

Open the local URL printed in your terminal, usually `http://localhost:8501`.

## Running Tests

Run the test suite from the project root:

```powershell
python -m pytest -v
```

The project has passed **28 tests** in the current development environment. Run the tests again after making changes to verify the current state.

## Data

The repository includes synthetic football match datasets for development, testing, and demonstration. These datasets are not official Premier League match data.

## Optional Grok Integration

The project includes an optional xAI Grok integration for match analysis. The current workflow also supports local, deterministic analysis.

To configure the optional integration:

1. Create a local `.env` file using `.env.example` as a reference.
2. Add your own xAI API key and the required configuration.
3. Never commit `.env` or expose API keys publicly.

Live API usage may incur charges or consume account credits. The core local workflow and test suite should be run without making live API calls.

## Project Structure

```text
MatchMind-AI/
├── data/
│   ├── synthetic/
│   └── processed/
├── docs/
├── scripts/
├── src/
│   ├── agents/
│   ├── engine/
│   ├── personalization/
│   ├── utils/
│   └── dashboard.py
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Project Goals

MatchMind AI aims to make football analysis more accessible, transparent, and personalized by combining multi-agent orchestration with evidence-based statistics and explainable insights.

**Built