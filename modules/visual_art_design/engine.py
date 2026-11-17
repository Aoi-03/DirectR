"""
Module 2: Visual Art & Design Assist Engine
Coordinates layered SVG synthesis, rig-ready character turnarounds,
cinematic storyboard framing, and interactive sketch-to-inpaint pipelines.
"""

from typing import List, Dict, Optional, Any, Tuple
from core.schemas import (
    ProjectBrief,
    SceneBeat,
    VisualAsset,
    CharacterProfile,
)
from core.event_bus import EventBus
from .schemas import (
    ColorPalette,
    LayeredSVGDocument,
    InpaintingMaskSpec,
    CharacterTurnaroundSpec,
    StoryboardShot,
    SkeletalTopology,
)
from .vector.svg_synthesizer import SVGSynthesizer
from .vector.palette_generator import PaletteGenerator
from .turnaround.rigging_engine import CharacterTurnaroundEngine
from .inpainting.sketch_pipeline import InpaintingPipeline
from .storyboard.storyboard_director import StoryboardDirector


class VisualArtEngine:
    """
    Unified Engine for:
    - Layered SVG synthesis with controllable Bezier anchor nodes.
    - 5-angle orthographic character turnarounds with rig-ready skeletal topology.
    - Tension-driven cinematic storyboard composition with 9:16 safe bounds.
    - Interactive sketch-to-production inpainting mask guidance.
    """

    def __init__(self, event_bus: Optional[EventBus] = None):
        self.bus = event_bus
        self.svg_synthesizer = SVGSynthesizer()

    def generate_layered_svg(
        self,
        prompt: str,
        scene_number: int,
        layers: Optional[List[str]] = None,
        visual_mood: str = "Moody Cinematic",
        setting_time: str = "NIGHT",
        tension_score: float = 0.5,
    ) -> Dict[str, Any]:
        """
        Synthesizes layered vector SVG markup preserving controllable anchor nodes.
        Maintains backward compatibility with original dictionary output.
        """
        doc: LayeredSVGDocument = self.svg_synthesizer.synthesize_scene_svg(
            scene_number=scene_number,
            prompt=prompt,
            visual_mood=visual_mood,
            setting_time=setting_time,
            tension_score=tension_score,
            layers=layers,
        )

        layer_names = [l.layer_name for l in doc.layers]

        if self.bus:
            self.bus.publish(
                "visual.svg_layered",
                {
                    "scene_number": scene_number,
                    "anchor_nodes_count": doc.total_anchor_nodes,
                    "layers": layer_names,
                },
            )

        return {
            "svg_markup": doc.svg_source,
            "anchor_nodes_count": doc.total_anchor_nodes,
            "layer_names": layer_names,
            "palette": doc.palette.model_dump(),
            "viewbox": doc.viewbox,
        }

    def generate_character_turnaround(
        self, character: CharacterProfile, stance: str = "A-Pose"
    ) -> VisualAsset:
        """
        Synthesizes consistent multi-angle character turnarounds with rig-ready topology.
        Angles: Front (0°), 3/4 Front (45°), Profile (90°), 3/4 Rear (135°), Back (180°).
        """
        asset = CharacterTurnaroundEngine.generate_turnaround_asset(character, stance=stance)

        if self.bus:
            self.bus.publish(
                "visual.turnaround_generated",
                {
                    "character_id": character.id,
                    "character_name": character.name,
                    "angles": asset.turnaround_angles,
                },
            )

        return asset

    def generate_turnaround_spec(
        self, character: CharacterProfile, stance: str = "A-Pose"
    ) -> CharacterTurnaroundSpec:
        """
        Generates full turnaround spec including skeletal topology and ControlNet configs.
        """
        return CharacterTurnaroundEngine.build_turnaround_spec(character, stance=stance)

    def generate_storyboard_frames(self, scenes: List[SceneBeat]) -> List[VisualAsset]:
        """
        Generates cinematic storyboard frame assets mapped to scene beats and tension curves.
        """
        storyboard_assets: List[VisualAsset] = []
        for scene in scenes:
            asset = StoryboardDirector.generate_scene_storyboard_asset(scene, shot_index=1)
            storyboard_assets.append(asset)

        if self.bus:
            self.bus.publish(
                "visual.storyboard_rendered",
                {"frames_count": len(storyboard_assets)},
            )

        return storyboard_assets

    def create_inpainting_job(
        self,
        task_id: str,
        target_layer_id: str,
        bounding_box: Tuple[int, int, int, int],
        semantic_label: str,
        mode: str = "feature_redesign",
        prompt_guidance: str = "",
    ) -> InpaintingMaskSpec:
        """
        Creates an inpainting task with localized mask and diffusion denoising schedule.
        """
        return InpaintingPipeline.create_inpainting_task(
            task_id=task_id,
            target_layer_id=target_layer_id,
            bounding_box=bounding_box,
            semantic_label=semantic_label,
            mode=mode,
            prompt_guidance=prompt_guidance,
        )

    def produce_visual_package(
        self, brief: ProjectBrief, scenes: List[SceneBeat]
    ) -> List[VisualAsset]:
        """
        Produces storyboard frames, layered SVGs, and character turnarounds for the project.
        Integrates seamlessly into the central DirectR production pipeline.
        """
        assets: List[VisualAsset] = []

        # 1. Generate Turnaround sheets for all characters
        for char in brief.characters:
            turnaround = self.generate_character_turnaround(char)
            assets.append(turnaround)

        # 2. Generate Layered SVG for each scene
        for scene in scenes:
            svg_info = self.generate_layered_svg(
                prompt=f"Scene {scene.scene_number}: {scene.visual_mood} - {scene.action_description}",
                scene_number=scene.scene_number,
                visual_mood=scene.visual_mood,
                setting_time=scene.setting_time,
                tension_score=scene.tension_score,
            )

            svg_asset = VisualAsset(
                asset_id=f"svg_scene_{scene.scene_number}",
                scene_number=scene.scene_number,
                asset_type="layered_svg",
                prompt=f"{scene.title}: {scene.visual_mood}",
                svg_data=svg_info["svg_markup"],
                anchor_nodes_count=svg_info["anchor_nodes_count"],
            )
            assets.append(svg_asset)

        # 3. Generate Cinematic Storyboard Frames for each scene
        storyboard_frames = self.generate_storyboard_frames(scenes)
        assets.extend(storyboard_frames)

        if self.bus:
            self.bus.publish("visual.package_produced", {"assets_count": len(assets)})

        return assets
