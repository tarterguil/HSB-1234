# 🚀 HARNESS AI AGENTIC

> **AI-Driven Career Pathfinder & Storyteller**  
> An interactive, multi-agent career exploration and storytelling platform powered by **LangGraph**, **FastAPI**, and modern web technologies.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg?style=flat)](https://github.com/langchain-ai/langgraph)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 🌟 Overview

**HARNESS AI AGENTIC** transforms traditional, static career tests and job boards into dynamic, localized, visual career narratives. 

Instead of generic bullet points, the platform uses an intelligent multi-agent orchestration pipeline to:
1. Analyze personal user traits, skills, and background.
2. Formulate high-level regional career strategies.
3. Generate granular "Day-in-the-Life" scenarios and milestone progression steps.
4. Render interactive story cards, regional job maps, and community-shareable career storybooks.

---

## 🏗️ System Architecture

The core engine is driven by a multi-agent Directed Acyclic Graph (DAG) built with **LangGraph**:

```
                      +---------------------------------------+
                      |          Frontend UI (JSB)            |
                      |    Bootstrap 5 + Vanilla JS + Map     |
                      +-------------------+-------------------+
                                          |
                                    REST API / JSON
                                          |
                      +-------------------v-------------------+
                      |            FastAPI Server             |
                      |   Route Handlers & State Manager      |
                      +-------------------+-------------------+
                                          |
                                           v Orchestrates via
                      +---------------------------------------+
                      |         LangGraph Multi-Agent         |
                      |               Pipeline                |
                      +-------------------+-------------------+
                                          |
         +--------------------------------+--------------------------------+
         |                                |                                |
+--------v-------+               +--------v-------+               +--------v-------+
| Director Agent |               | Scenario Agent |               | Visual Matching|
| (Gemini / DS)  +-------------->| (DS / Gemini)  +-------------->|     Agent      |
| Profile Routing|  State Pass   | Step Breakdown |  State Pass   | (Qwen 3 / DS)  |
+----------------+               +----------------+               +----------------+
```

### 🤖 Multi-Agent Workflow
- **Director Agent (`DirectorAgent`)**: Analyzes personal skills, academic background, and personality traits to curate tailored career trajectories and localized opportunities.
- **Scenario Agent (`ScenarioAgent`)**: Breaks down selected paths into sequential workplace milestones, daily routines, actionable skill steps, and challenges.
- **Visual Match Agent (`VisualMatchAgent`)**: Synthesizes career pros/cons, explores adjacent alternative pathways, and structures visual infographics & cards for display.

---

## ✨ Features

- **🎯 Interactive Profiling Wizard**: Multi-step intuitive assessment capturing strengths, working styles, and career goals.
- **🗺️ Regional Opportunity Map**: Leaflet.js-powered map showing local job clusters, regional salary ranges, and localized industry hotspots.
- **📖 Dynamic Career Storybook**: Visual day-in-the-life cards detailing early-career, mid-level, and senior-level progression.
- **🏛️ Public Community Gallery**: Save generated career roadmaps to SQLite and share unique career stories with peers.
- **⚡ Live Streaming & Fallback**: Fast multi-model routing with built-in fallback mechanisms for high reliability.

---

## 🛠️ Tech Stack

| Domain | Technology |
| :--- | :--- |
| **Backend** | Python 3.11+, FastAPI, Uvicorn, Pydantic v2, SQLAlchemy |
| **Agent Orchestration** | LangGraph, LangChain Core |
| **LLM Integrations** | DeepSeek (`deepseek-chat`), Google Gemini (`gemini-2.5-flash`), Qwen (`qwen-2.5-72b-instruct`) via OpenRouter |
| **Frontend** | HTML5, CSS3 (Modern Glassmorphism & Responsive Design), Vanilla JavaScript, Bootstrap 5 |
| **Mapping Engine** | Leaflet.js & OpenStreetMap |
| **Database** | SQLite (Async-ready with SQLAlchemy ORM) |

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/tarterguil/HSB-1234.git
cd HSB-1234
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the template `.env.example` to create your local `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```env
DEEPSEEK_API_KEY="your_deepseek_api_key_here"
OPENROUTER_API_KEY="your_openrouter_api_key_here"

# Optional configuration overrides
HOST="0.0.0.0"
PORT=8000
DEBUG=True
```

### 5. Run the Server
```bash
python main.py
```
Or with Uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open your browser and visit:
- **Web App**: [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📂 Project Structure

```text
├── app/
│   ├── api/
│   │   ├── endpoints/       # API endpoints (profile, story, gallery, health)
│   │   │   ├── gallery.py
│   │   │   ├── health.py
│   │   │   ├── profile.py
│   │   │   └── story.py
│   │   └── router.py        # Central API v1 router
│   ├── core/
│   │   ├── config.py        # Pydantic settings & environment configuration
│   │   └── llm.py           # LLM client initializations & model routing
│   ├── db/
│   │   ├── models.py        # SQLAlchemy database models
│   │   └── session.py       # DB engine and session factory
│   ├── graph/
│   │   ├── prompts.py       # System & node prompt templates
│   │   ├── state.py         # LangGraph state schema definition
│   │   └── workflow.py      # Multi-agent LangGraph workflow execution
│   └── schemas/             # Pydantic request & response validation models
│       ├── profile.py
│       └── story.py
├── static/                  # Frontend assets
│   ├── css/
│   │   └── style.css        # Modern responsive design & animations
│   ├── js/
│   │   └── app.js           # Multi-step wizard, map logic, API interactions
│   └── index.html           # Main single-page web app
├── .env.example             # Environment template
├── .gitignore               # Ignored files (secrets, caches, db)
├── main.py                  # FastAPI application entrypoint
├── requirements.txt         # Project Python dependencies
└── test_phase1.py - test_phase3.py # Automated test suite
```

---

## 🧪 Testing

Run test suites using `pytest`:

```bash
pytest test_phase1.py test_phase2.py test_phase3.py -v
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to check the [issues page](https://github.com/tarterguil/HSB-1234/issues).

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
