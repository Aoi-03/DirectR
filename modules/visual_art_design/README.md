# Module 2: Visual Art & Design Assist (Digital Illustration & 3D)

**Assigned Collaborator:** Friend 2 (Visual Artist)  
**Feature Branch:** `feature/visual-art`  
**Assigned Directory:** `modules/visual_art_design/`  

---

## 🎯 Task Objectives

Generative image models often produce uncontrollable random hallucinations rather than controllable iterative layer workflows that real artists require. 

Module 2 provides a fully controllable, multi-layer vector and 3D visual production engine:
1. **Controllable Vector Generation:** Multi-layer SVG synthesis with editable Bezier anchor nodes (`data-anchor-group`, `data-node-id`) and mood-driven color palettes.
2. **Production-Ready Turnaround Rigging:** 5-angle orthographic model sheets (`front`, `three_quarters_front`, `profile`, `three_quarters_back`, `back`) with 15-point skeletal joint topology landmarks and ControlNet/IP-Adapter conditioning profiles.
3. **Interactive Guided Inpainting & Sketch-to-Production:** Localized bounding box mask generation with feathered alpha edges and tiered denoising schedules (`touchup`, `redesign`, `generative`).
4. **Cinematic Storyboard Director:** Automated camera shot selection (wide establishing shots, medium two-shots, dramatic Dutch tilts) mapped to scene tension curves with calculated 9:16 vertical crop safe zones for Module 4 (Creator Distribution).

---

## 📁 Architecture & Subpackage Structure

```text
modules/visual_art_design/
├── __init__.py                     # Package exports
├── README.md                       # Module technical documentation
├── engine.py                       # Unified VisualArtEngine (pipeline orchestrator)
├── schemas.py                      # Pydantic schemas (AnchorNode, ColorPalette, StoryboardShot, etc.)
├── test_visual.py                  # Comprehensive unit test suite
├── vector/                         # Layered vector synthesis subpackage
│   ├── __init__.py
│   ├── palette_generator.py        # Mood & tension-based color harmony engine
│   └── svg_synthesizer.py          # Parametric Bezier path synthesis with anchor nodes
├── turnaround/                     # Character turnaround & rigging subpackage
│   ├── __init__.py
│   └── rigging_engine.py           # 5-angle orthographic sheets & 15-joint skeletal landmarks
├── inpainting/                     # Sketch-to-production & inpainting subpackage
│   ├── __init__.py
│   └── sketch_pipeline.py          # Localized alpha mask synthesis & denoising presets
├── storyboard/                     # Cinematography & camera director subpackage
│   ├── __init__.py
│   └── storyboard_director.py      # Dynamic shot selection (24mm–18mm) & 9:16 safe bounds
└── web_canvas/                     # Interactive Web Studio subpackage
    ├── __init__.py
    └── studio.html                 # Interactive dark-mode canvas studio viewer
```

---

## 🎨 Interactive Visual Studio (`web_canvas/studio.html`)

An interactive Web Studio is provided for visual inspection and manipulation:
- **Layer Visibility Hierarchy:** Toggle background, midground, foreground, lighting, and VFX layers.
- **Interactive Bezier Node Deformer:** Click and drag circular anchor nodes directly on the canvas to reshape curves in real-time.
- **Turnaround Inspector:** Switch between Front (0°), 3/4 Front (45°), Profile (90°), 3/4 Rear (135°), and Back (180°) views.
- **9:16 Vertical Reel Guide:** Live overlay displaying the exact vertical safe zone coordinates consumed by Module 4.
- **Inpaint Mask Inspector:** Visualizes localized mask bounding box with feather radius and denoising parameters.

To view: open `modules/visual_art_design/web_canvas/studio.html` in any web browser.

---

## 🧪 Testing

Run unit tests strictly for Module 2:
```bash
python -m unittest modules.visual_art_design.test_visual -v
```

Run all tests across the repository:
```bash
python -m unittest discover -s . -p "test_*.py" -v
```

Run full studio pipeline integration:
```bash
python main.py
```
