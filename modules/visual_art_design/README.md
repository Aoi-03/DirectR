# Module 2: Visual Art & Design Assist (Digital Illustration & 3D)

**Assigned Collaborator:** Friend 2  
**Feature Branch:** `feature/visual-art`  

---

## 🎯 Task Objectives

Generative image models often produce uncontrollable random hallucinations rather than controllable iterative layer workflows that real artists require.

### Seed Prompting Inspirations to Implement:
1. **Controllable Vector Synthesis:** Layered SVG and vector path synthesis preserving controllable anchor nodes.
2. **Production Turnaround Rigging:** Consistent multi-angle character turnarounds (front, 3/4, side, back) with rig-ready topology.
3. **Interactive Guided Inpainting:** Interactive sketch-to-production pipeline with live semantic brush guidance and localized inpainting.

---

## 💻 Tech Stack & APIs
- **ControlNet & IP-Adapters** (Rigid pose, spatial depth, and character style preservation)
- **Diffusion Inpainting Pipelines** (Iterative layer-based modification)
- **SVG Path Generation** (Semantic vector generation with grouped nodes)
- **WebGPU Shaders** (High-performance in-browser canvas and brush rendering)

---

## 📁 Files in this Module
- `engine.py`: SVG generator, turnaround sheet synthesis, and inpainting pipeline.
- `test_visual.py`: Unit tests verifying vector anchor node counts and multi-angle turnaround structure.

---

## 🧪 Testing Your Work
Run tests for your module:
```bash
pytest modules/visual_art_design/
```
