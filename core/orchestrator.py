"""
DirectR Swarm Orchestrator (Open Innovation Engine)
Orchestrates autonomous multi-agent creative production across all 4 modules.
"""

import logging
from typing import Optional
from .schemas import ProjectBrief, ProductionPackage
from .event_bus import EventBus

# Lazy/dynamic imports for decoupled modules
from modules.narrative_screenplay.engine import NarrativeScreenplayEngine
from modules.visual_art_design.engine import VisualArtEngine
from modules.audio_soundscapes.engine import AudioStudioEngine
from modules.creator_distribution.engine import CreatorDistributionEngine

logger = logging.getLogger("DirectR.Orchestrator")


class DirectROrchestrator:
    """
    Central Swarm Orchestrator executing the unified 4-module production pipeline.
    """

    def __init__(self, event_bus: Optional[EventBus] = None):
        self.bus = event_bus or EventBus()
        self.narrative_engine = NarrativeScreenplayEngine(self.bus)
        self.visual_engine = VisualArtEngine(self.bus)
        self.audio_engine = AudioStudioEngine(self.bus)
        self.creator_engine = CreatorDistributionEngine(self.bus)

    def execute_production_pipeline(self, brief: ProjectBrief) -> ProductionPackage:
        """
        Execute end-to-end multi-agent production:
        1. Narrative & Screenplay: Generate scenes, dialogue, and beats.
        2. Visual Art & Design: Generate character turnarounds, SVGs, and storyboard.
        3. Music & Audio: Generate dynamic tension-adapted stems & Foley effects.
        4. Creator & Distribution: Auto-extract vertical reels & A/B test thumbnails.
        """
        logger.info(f"=== Starting DirectR Production Pipeline: {brief.title} ===")
        self.bus.publish("pipeline.started", {"project_id": brief.project_id})

        # Phase 1: Narrative Engine
        logger.info("[Phase 1] Generating Narrative Screenplay & Character Dialogue...")
        scenes = self.narrative_engine.generate_screenplay(brief)
        self.bus.publish("narrative.completed", {"scenes_count": len(scenes)})

        # Phase 2: Visual & Audio Engines
        logger.info("[Phase 2A] Synthesizing Visual Art, Turnarounds & Vector Paths...")
        visual_assets = self.visual_engine.produce_visual_package(brief, scenes)

        logger.info("[Phase 2B] Synthesizing Adaptive Soundscapes & Foley Cues...")
        stem_arrangements = self.audio_engine.arrange_soundscapes(scenes)
        foley_assets = self.audio_engine.synthesize_foley_cues(scenes)

        # Phase 3: Creator & Distribution Engine
        logger.info("[Phase 3] Generating Vertical Reels, Thumbnail Heatmaps & Distribution Assets...")
        reels = self.creator_engine.extract_tension_reels(scenes)
        thumbnails = self.creator_engine.generate_thumbnail_variants(brief, scenes)

        # Phase 4: Assembly into Final Production Package
        package = ProductionPackage(
            project_id=brief.project_id,
            brief=brief,
            scenes=scenes,
            visual_assets=visual_assets,
            stem_arrangements=stem_arrangements,
            foley_assets=foley_assets,
            reels=reels,
            thumbnails=thumbnails,
            distribution_ready=True,
        )

        self.bus.publish("pipeline.finished", {"project_id": brief.project_id})
        logger.info("=== DirectR Production Pipeline Successfully Completed! ===")
        return package
