# DirectR: Autonomous Multi-Agent AI Creative Production Studio

> **DirectR** is an autonomous multi-agent creative studio that unifies screenplay writing, visual art and 3D design, adaptive musical soundscapes, and autonomous content distribution into a single real-time collaborative production pipeline.

[![CI](https://github.com/Aoi-03/DirectR/actions/workflows/ci.yml/badge.svg)](https://github.com/Aoi-03/DirectR/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)

---

## 🌟 The Vision & The 4 Core Tracks

DirectR bridges the creative gap between indie creators and high-end studio production. By assembling four specialized AI modules orchestrated by an Open Innovation multi-agent swarm, DirectR can turn an initial concept into a fully scored, illustrated, and distribution-ready production.

```
                              ┌───────────────────────────────────┐
                              │     DIRECTR SWARM ORCHESTRATOR    │
                              │     (Wildcard: Open Innovation)   │
                              └─────────────────┬─────────────────┘
                                                │
         ┌───────────────────────────┬──────────┴────────────────┬───────────────────────────┐
         ▼                           ▼                           ▼                           ▼
┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
│     MODULE 1     │        │     MODULE 2     │        │     MODULE 3     │        │     MODULE 4     │
│   Storytelling   │───────>│    Visual Art    │───────>│   Audio Studio   │───────>│  Creator Agents  │
│   & Co-Writers   │        │  & Design Assist │        │  & Soundscapes   │        │  & Distribution  │
│  [Teammate 1]    │        │   [Teammate 2]   │        │   [Teammate 3]   │        │   [Teammate 4]   │
└──────────────────┘        └──────────────────┘        └──────────────────┘        └──────────────────┘
```

---

## 👥 Module Breakdown & Team Responsibilities

Four team members work concurrently from their respective machines on separate modules, linked by this unified repository:

| Module & Directory | Role / Track | Teammate | Focus Area & Tech Stack |
| :--- | :--- | :--- | :--- |
| **`modules/narrative_screenplay/`** | **Storytelling & Co-Writers** | **Member 1** | Character psychology constraints, branching lore trees, dialect-adaptive screenplay dialog. *(Structured Outputs, Context Caching, Vector Trees, Gemini/Claude Long Context)* |
| **`modules/visual_art_design/`** | **Visual Art & Design Assist** | **Member 2** | Layered SVG synthesis, multi-angle rig-ready character turnarounds, sketch-to-production inpainting. *(ControlNet, IP-Adapters, SVG Path Generation, WebGPU Shaders)* |
| **`modules/audio_soundscapes/`** | **Music & Audio Studios** | **Member 3** | Tension-adaptive stem arrangement, zero-shot Foley SFX, micro-tonal vocal harmony matching. *(Web Audio API, Lyria/MusicLM, Audio Embeddings, Realtime MIDI)* |
| **`modules/creator_distribution/`** | **Autonomous Creator Agents** | **Member 4** | High-tension vertical reel extraction, A/B thumbnail heatmap testing, creator persona responder. *(Multimodal Vision LLMs, Video Stitching, Whisper ASR, Agentic Tool Calling)* |
| **`core/`** | **Swarm Orchestrator (Wildcard)** | **Shared / Lead** | Event bus, shared Pydantic data schemas, multi-agent pipeline orchestration. *(Multi-Agent Frameworks, Realtime APIs, WebSockets)* |

---

## 🤝 Collaboration Architecture: "Read All, Edit Only Yours"

To enable smooth parallel development across 4 different computers without git merge conflicts:

1. **Strict Folder Boundaries**:
   - Each collaborator **only modifies files inside their assigned module folder** (`modules/<assigned_module>/`).
   - Collaborators can freely **read and import** from `core/` and other teammates' modules.
   - Any modifications to `core/schemas.py` or shared utilities require team consensus via Pull Request (PR).
2. **Dedicated Feature Branches**:
   - `feature/narrative` (Member 1)
   - `feature/visual-art` (Member 2)
   - `feature/audio-studio` (Member 3)
   - `feature/creator-agents` (Member 4)
3. **Automated Enforcement**:
   - GitHub `CODEOWNERS` automatically assigns module reviews.
   - Automated CI testing runs on every Pull Request.

📖 **For detailed setup, Git commands, and collaboration guidelines, read the [Team Collaboration Guide](TEAM_COLLABORATION_GUIDE.md).**

---

## 📁 Repository Directory Structure

```text
DirectR/
├── .github/
│   ├── CODEOWNERS                      # Automated PR ownership rules
│   └── workflows/
│       └── ci.yml                      # CI pipeline for automated testing
├── core/                               # Shared contracts and Swarm Engine
│   ├── __init__.py
│   ├── schemas.py                      # Inter-module data schemas (Pydantic)
│   ├── event_bus.py                    # Realtime inter-module pub/sub bus
│   └── orchestrator.py                 # Multi-agent swarm pipeline runner
├── modules/
│   ├── narrative_screenplay/           # Module 1: Storytelling & Screenplay
│   │   ├── README.md                   # Task specs & documentation
│   │   ├── engine.py                   # Narrative & dialogue implementation
│   │   └── test_narrative.py           # Unit tests
│   ├── visual_art_design/              # Module 2: Visual Art & 3D Assist
│   │   ├── README.md                   # Task specs & documentation
│   │   ├── engine.py                   # SVG, Turnarounds, & Diffusion pipeline
│   │   └── test_visual.py              # Unit tests
│   ├── audio_soundscapes/              # Module 3: Music & Audio Studios
│   │   ├── README.md                   # Task specs & documentation
│   │   ├── engine.py                   # Dynamic stems & Foley synthesis
│   │   └── test_audio.py               # Unit tests
│   └── creator_distribution/           # Module 4: Creator Agents & Distribution
│       ├── README.md                   # Task specs & documentation
│       ├── engine.py                   # Reel extraction, Thumbnails & Community AI
│       └── test_creator.py             # Unit tests
├── scripts/
│   └── pre_commit_guard.py             # Pre-commit boundary checker
├── main.py                             # Interactive CLI / Pipeline test entrypoint
├── requirements.txt                    # Project dependencies
├── .env.example                        # Template for API keys
├── .gitignore                          # Ignores screenshots, images, cache
├── CONTRIBUTING.md                     # Contribution standards & PR template
├── MODULE_SPECS.md                     # Deep task specifications & requirements
└── TEAM_COLLABORATION_GUIDE.md         # Step-by-step Git guide for the 4 teammates
```

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Aoi-03/DirectR.git
cd DirectR
```

### 2. Setup Virtual Environment & Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your respective API keys (Gemini, OpenAI, Anthropic, Replicate, etc.)
```

### 4. Run the Full Pipeline Test
Execute the end-to-end swarm demonstration connecting all 4 modules:
```bash
python main.py
```

### 5. Run Unit Tests Across All Modules
```bash
pytest
```

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
