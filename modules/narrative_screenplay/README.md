# Module 1: Narrative & Screenplay (Storytelling & Co-Writers)

**Assigned Collaborator:** Friend 1  
**Feature Branch:** `feature/narrative`  

---

## 🎯 Task Objectives

Modern storytellers struggle with maintaining intricate lore consistency, dialogue voice fidelity, and dynamic nonlinear branching across episodic sagas.

### Seed Prompting Inspirations to Implement:
1. **Psychology Constraints:** Maintain character psychology constraints across 10-chapter branching paths.
2. **Dialect & Voice Fidelity:** Generate screenplay dialogue adapting dialect rules in real-time based on character background and regional identity.
3. **Reactive Backstories:** Autonomous narrative sandbox generating reactive NPC backstories.

---

## 💻 Tech Stack & APIs
- **Structured Outputs** (Pydantic models, JSON schema guarantees)
- **Context Caching** (Persisting world bible and lore across iterative LLM calls)
- **Vector Memory Trees** (Hierarchical memory retrieval for character states)
- **Claude / Gemini Long Context** (Processing full script drafts)

---

## 📁 Files in this Module
- `engine.py`: Core narrative generation logic, character psychology validator, and dialect engine.
- `test_narrative.py`: Unit tests ensuring character constraints and dialogue output match specifications.

---

## 🧪 Testing Your Work
Run tests for your module:
```bash
pytest modules/narrative_screenplay/
```
