# Drug Side Effect Tracker

An AI-powered Flask application that tracks drug side effects using LangChain agents and MCP (Model Context Protocol) servers. The app fetches real side effect data from ClinicalTrials.gov and stores it in a local SQLite database.

## Features

- **AI Chat Interface** – Ask about drug side effects in natural language
- **Real-time Data** – Fetches side effect data from ClinicalTrials.gov API
- **Local Database** – Stores drugs and side effects in SQLite for quick access
- **MCP Integration** – Uses Arcade MCP server for external tool access

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│   Flask Web UI  │────▶│  LangChain Agent │────▶│  Local Tools (DB)   │
└─────────────────┘     └──────────────────┘     └─────────────────────┘
                               │
                               ▼
                        ┌──────────────────┐     ┌─────────────────────┐
                        │   Arcade MCP     │────▶│  ClinicalTrials.gov │
                        └──────────────────┘     └─────────────────────┘
```

## Project Structure

```
slide_effect_tracker/
├── agent_app/              # Main Flask application
│   ├── main.py             # Flask app & agent setup
│   ├── agent.py            # Tool definitions
│   ├── models.py           # SQLAlchemy models
│   └── templates/
│       └── home.html       # Web interface
├── side_effects_mcp/       # MCP server for clinical trials data
│   └── src/side_effects_mcp/
│       └── server.py       # MCP tool: get_side_effects_for_drugs
├── pyproject.toml
└── README.md
```

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

## Environment Variables

Create a `.env` file in `agent_app/`:

```env
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=gemini-2.0-flash
ARCADE_API_KEY=your_arcade_api_key
ARCADE_USER_ID=your_arcade_user_id
```

## Installation

```bash
# Clone and navigate to project
cd slide_effect_tracker

# Install dependencies
uv sync

# Navigate to agent app
cd agent_app
uv sync
```

## Running the App

```bash
cd agent_app
uv run main.py
```

The app runs at `http://127.0.0.1:5000`

## Available Tools

| Tool | Description |
|------|-------------|
| `list_drugs` | List all drugs in the database |
| `create_drug` | Add a new drug to the database |
| `delete_drug` | Delete a drug and all its side effects |
| `list_side_effects` | List side effects for a specific drug |
| `create_side_effect` | Add a side effect report for a drug |
| `delete_side_effect` | Remove a specific side effect from a drug |
| `get_side_effects_for_drugs` | Fetch side effects from ClinicalTrials.gov (MCP) |

## Database Models

**Drug**
- `id` (Integer, PK)
- `drug_name` (String)

**SideEffectReport**
- `id` (Integer, PK)
- `side_effect_name` (String)
- `side_effect_probability` (Float)
- `drug_id` (FK → Drug)

## Example Queries

- "What are the side effects of Aspirin?"
- "Add Ibuprofen to the database"
- "Delete headache side effect from Aspirin"
- "List all drugs"


