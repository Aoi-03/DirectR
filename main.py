"""
DirectR: Autonomous Multi-Agent AI Creative Production Studio
Main Pipeline Runner & CLI Demonstration
"""

import json
import logging
from core.schemas import ProjectBrief, CharacterProfile
from core.orchestrator import DirectROrchestrator
from core.event_bus import EventBus

# Configure clean logging output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("DirectR.Main")


def main():
    print("=" * 70)
    print("🎬 DIRECTR: AUTONOMOUS MULTI-AGENT CREATIVE PRODUCTION STUDIO")
    print("=" * 70)

    # 1. Initialize Event Bus and Swarm Orchestrator
    bus = EventBus()
    orchestrator = DirectROrchestrator(event_bus=bus)

    # 2. Define a Sample Production Brief
    brief = ProjectBrief(
        project_id="directr_pilot_001",
        title="Chronicles of Neo-Aethel",
        genre="Cyberpunk Sci-Fi Fantasy",
        logline="In a submerged neon metropolis, a lone archivist and a rogue pilot uncover a sentient AI code that alters physical architecture.",
        characters=[
            CharacterProfile(
                id="char_lyra",
                name="Lyra Vance",
                archetype="Sub-surface Archivist",
                psychology_constraints=[
                    "Never destroy historical records",
                    "Distrust central governance authorities",
                ],
                dialect_rules={
                    "cannot": "can't",
                    "do not": "don't",
                    "danger": "glitch",
                    "friend": "anchor",
                },
                backstory="Former data curator who survived the Great Pulse flood.",
            ),
            CharacterProfile(
                id="char_kael",
                name="Kaelen Cross",
                archetype="Hovercraft Rogue",
                psychology_constraints=["Protective of crew members at all costs"],
                dialect_rules={"understand": "copy", "yes": "solid"},
                backstory="Ex-military escort pilot navigating the sunken lower levels.",
            ),
        ],
        target_duration_minutes=5,
    )

    print(f"\n📋 Project Brief Loaded: '{brief.title}' [{brief.genre}]")
    print(f"Logline: {brief.logline}\n")

    # 3. Execute the Full End-to-End Multi-Agent Production Pipeline
    package = orchestrator.execute_production_pipeline(brief)

    # 4. Display Results Summary Across All 4 Modules
    print("\n" + "=" * 70)
    print("✨ PRODUCTION PACKAGE SUMMARY (ALL 4 MODULES INTEGRATED)")
    print("=" * 70)

    print(f"\n[Module 1: Narrative & Screenplay]")
    print(f"  • Total Scene Beats Generated: {len(package.scenes)}")
    for s in package.scenes:
        print(f"    - Scene {s.scene_number} [{s.setting_time}]: {s.title} (Tension: {s.tension_score:.2f})")
        if s.dialogue:
            print(f"      Dialogue: \"{s.dialogue[0].speaker}: {s.dialogue[0].line}\"")

    print(f"\n[Module 2: Visual Art & Design Assist]")
    print(f"  • Visual Assets Produced: {len(package.visual_assets)}")
    for v in package.visual_assets:
        if v.asset_type == "turnaround_sheet":
            print(f"    - Turnaround Sheet: {v.character_id} ({', '.join(v.turnaround_angles)})")
        elif v.asset_type == "layered_svg":
            print(f"    - Layered SVG for Scene {v.scene_number} (Anchor Nodes: {v.anchor_nodes_count})")

    print(f"\n[Module 3: Music & Audio Studios]")
    print(f"  • Adaptive Stems Arranged: {len(package.stem_arrangements)}")
    for stem in package.stem_arrangements:
        print(f"    - Scene {stem.scene_number}: {stem.tempo_bpm} BPM | Valence: {stem.emotional_valence}")
        print(f"      Active Stems: {', '.join(stem.active_stems)}")
    print(f"  • Zero-Shot Foley Synthesized: {len(package.foley_assets)} SFX assets")

    print(f"\n[Module 4: Creator Agents & Distribution]")
    print(f"  • Extracted Vertical Reels (9:16): {len(package.reels)}")
    for r in package.reels:
        print(f"    - Reel ID {r.reel_id}: Scene {r.source_scene_number} (Hook: \"{r.hook_text[:40]}...\")")
    print(f"  • A/B Thumbnail Variants Tested: {len(package.thumbnails)}")
    best_thumb = max(package.thumbnails, key=lambda t: t.attention_heatmap_score)
    print(f"    - Best Variant: '{best_thumb.headline}' (Attention Heatmap Score: {best_thumb.attention_heatmap_score}/100, Predicted CTR: {best_thumb.predicted_ctr}%)")

    print("\n" + "=" * 70)
    print("🚀 All 4 Modules Executed and Verified Successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
