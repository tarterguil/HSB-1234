# HARNESS AI AGENTIC: AI-Driven Career Pathfinder & Storyteller
## Project Concept & Architecture Plan | JSB12 Science & Technology Competition

---

### 1. Executive Summary & Concept Vision
**HARNESS AI AGENTIC** is an interactive, multi-agent career exploration and storytelling platform designed for students and job seekers. Utilizing state-of-the-art AI agent orchestration (**LangGraph**), the system transforms traditional, flat job search results into visual, dynamic, and localized career narratives.

Instead of presenting static job bullet points, the platform acts as an intelligent career director: analyzing personal user traits, mapping real-world regional opportunities, breaking down day-in-the-life career scenarios, and generating rich visual infographic stories for each path.

---

### 2. High-Level System Architecture

The project seamlessly integrates a lightweight web frontend (**JavaScript + Bootstrap 5**) with a robust async backend (**FastAPI**), orchestrated by a multi-agent backend graph (**LangGraph**).

```
                      +---------------------------------------+
                      |          Frontend UI (JSB)            |
                      |   JS Logic + Bootstrap 5 Styling     |
                      +-------------------+-------------------+
                                          |
                                    REST API / WebSockets
                                          |
                      +-------------------v-------------------+
                      |            FastAPI Server             |
                      |   Route Handlers & State Manager      |
                      +-------------------+-------------------+
                                          |
                                          | Orchestrates via
                                          v
                      +---------------------------------------+
                      |         LangGraph Multi-Agent         |
                      |               Pipeline                |
                      +-------------------+-------------------+
                                          |
         +--------------------------------+--------------------------------+
         |                                |                                |
+--------v-------+               +--------v-------+               +--------v-------+
| Director Model |               | Scene Scenario |               | Job Matching & |
|  (Gemini/DS)   +-------------->| Model (DS/Gem)  +-------------->| Visual Model   |
| Router & Advice|  State Pass   | Step Breakdown |  State Pass   | (Qwen 3 Pro)   |
+----------------+               +----------------+               +----------------+
```

---

### 3. Core Multi-Agent Architecture

The core logic is powered by a multi-node **LangGraph** execution DAG (Directed Acyclic Graph):

#### 🤖 Agent 1: The Director Model (`DirectorAgent`)
* **Underlying LLMs:** Gemini 2.5 / DeepSeek
* **Inputs:** Personal traits, background, skill matrix, location/region.
* **Responsibilities:**
  * Analyzes strengths, personality, and qualification fit.
  * Queries localized regional job requirements.
  * Formulates high-level career advisory strategy and selects optimal career trajectories.
  * Delegates concrete scenario generation to Model 2.

#### 🤖 Agent 2: Scene & Scenario Breakdown Model (`ScenarioAgent`)
* **Underlying LLMs:** DeepSeek / Gemini 2.5
* **Inputs:** Director's advisory output and target job profiles.
* **Responsibilities:**
  * Deconstructs a high-level job into sequential "Day-in-the-Life" visual scenes and milestones.
  * Generates actionable steps, skills needed for each phase, and typical workplace challenges.
  * Passes structured JSON scene representations to the Job Matching/Creation Model.

#### 🤖 Agent 3: Job Matching & Visual Creation Model (`VisualMatchAgent`)
* **Underlying LLM / Multimodal Engine:** Qwen 3 Pro
* **Inputs:** Scene breakdown JSON, career trajectory, regional context.
* **Responsibilities:**
  * Synthesizes Pros & Cons for each career path.
  * Identifies adjacent/alternative career trajectories.
  * Renders/generates structured visual output cards and illustrative infographic images capturing job roles and day-in-the-life scenes.

---

### 4. Interactive & Web Platform Features

1. **Interactive Trait & Profiling Wizard (Prompt Engine):**
   * Multi-step dynamic form powered by vanilla JavaScript.
   * Gathers personality traits, academic background, preferred working style, and geographic constraints.

2. **Interactive Career Location Map:**
   * Embedded interactive Map view (Leaflet.js / Mapbox integration).
   * Pins real-world regional job hubs, local skill demands, and salary heatmaps based on selected career paths.

3. **Career Storybook & Community Gallery (Save & Share):**
   * Saves generated visual career scenarios to SQLite/PostgreSQL database.
   * Unique link generation for sharing personalized career storylines.
   * Public gallery showcasing top-rated or trending career paths explored by other students.

---

### 5. Tech Stack Matrix

| Domain | Technology / Library | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | **FastAPI** (Python 3.11+) | Async API endpoints, WebSockets for streaming state updates |
| **Agentic Framework** | **LangGraph** (Python) | State graph execution, multi-agent communication & fallback |
| **Frontend UI** | **HTML5 + JS + Bootstrap 5** | JSB Stack: client-side logic, responsive styling, map rendering |
| **AI Models** | **Gemini 2.5, DeepSeek, Qwen 3 Pro** | Multi-tiered reasoning, scene planning, and visual generation |
| **Mapping Engine** | **Leaflet.js / OpenStreetMap** | Interactive job geolocation rendering |
| **Database** | **SQLite / Async SQLAlchemy** | Storing saved stories, user profiles, and map markers |

---

### 6. Project Roadmap & Development Milestones

```
[Phase 1: Architecture Setup] ---> [Phase 2: LangGraph Integration] ---> [Phase 3: Web UI & Map] ---> [Phase 4: Gallery & Polish]
    (FastAPI + Models)                   (Agents 1, 2, 3)                     (JS + Bootstrap)                 (Testing & Pitch)
```

#### Phase 1: Foundation & Core Setup (Week 1)
- [x] Define FastAPI structure and API routes (`/api/v1/profile`, `/api/v1/generate-story`).
- [x] Configure API keys and client adapters for Gemini 2.5, DeepSeek, and Qwen 3 Pro.
- [x] Establish LangGraph `StateGraph` dictionary structure.

#### Phase 2: Agent Orchestration (Week 2)
- [x] Implement **Director Model**: User Trait Analysis -> Career Strategy.
- [x] Implement **Scenario Model**: Scenario -> Actionable Steps & Scenes.
- [x] Implement **Visual Matching Model (Qwen 3 Pro)**: Card/Infographic creation with Pros/Cons & Alternatives.
- [x] Connect agents into unified LangGraph workflow with error recovery.

#### Phase 3: Frontend Development & Mapping (Week 3)
- [x] Build interactive Bootstrap 5 multi-step wizard.
- [x] Integrate Leaflet.js map view to display regional job pins and key requirements.
- [x] Implement asynchronous polling or WebSocket live stream for step-by-step AI progress feedback.

#### Phase 4: Social Features, Testing & Competition Pitch (Week 4)
- [x] Build "Save Story" & "Public Gallery" showcase tab.
- [x] Perform end-to-end user evaluation and prompt tuning.


---
*Created for JSB12 Science & Technology Competition submission.*
