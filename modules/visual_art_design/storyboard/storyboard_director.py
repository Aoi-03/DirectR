"""
Module 2: Storyboard Director & Cinematography Engine
Computes camera angles, lens focal lengths, lighting schemes, and aspect ratio safe zones.
"""

from typing import List, Tuple
from core.schemas import SceneBeat, VisualAsset
from ..schemas import StoryboardShot


class StoryboardDirector:
    """
    Transforms narrative scene beats into dynamic storyboard compositions
    with 16:9 master framing and 9:16 vertical crop bounds.
    """

    CANVAS_WIDTH: int = 1920
    CANVAS_HEIGHT: int = 1080

    @classmethod
    def calculate_shot_parameters(
        cls, scene: SceneBeat, shot_index: int = 1
    ) -> StoryboardShot:
        """
        Determines cinematic shot parameters driven by tension curve and action description.
        """
        t = scene.tension_score

        # Map dramatic tension to cinematic shot language
        if t <= 0.35:
            shot_type = "wide"
            camera_mov = "slow_dolly_back"
            focal_length = 24  # Wide angle establishing environment
            dof = "deep_focus_infinite"
            lighting = "soft_ambient_fill"
        elif t <= 0.70:
            shot_type = "medium"
            camera_mov = "tracking_forward"
            focal_length = 50  # Natural human eye perspective
            dof = "moderate_falloff"
            lighting = "three_point_key_rim"
        elif t <= 0.85:
            shot_type = "close_up"
            camera_mov = "handheld_micro_jitter"
            focal_length = 85  # Portrait compression
            dof = "shallow_bokeh"
            lighting = "stark_high_contrast_rim"
        else:
            shot_type = "dutch_tilt"
            camera_mov = "rapid_whip_pan"
            focal_length = 18  # Ultra-wide distortion + dramatic Dutch angle
            dof = "hyperfocal_split_diopter"
            lighting = "strobe_neon_emergency"

        # Calculate 16:9 full bounds
        w, h = cls.CANVAS_WIDTH, cls.CANVAS_HEIGHT
        bounds_16_9 = (0, 0, w, h)

        # Calculate centered 9:16 vertical safe zone (for Module 4 Reels extraction)
        # Height is 1080, so 9:16 width = 1080 * (9/16) = 607.5 -> 608px
        reel_w = int(h * (9 / 16))
        margin_x = (w - reel_w) // 2
        bounds_9_16 = (margin_x, 0, margin_x + reel_w, h)

        prompt = (
            f"Cinematic storyboard shot {shot_index} of Scene {scene.scene_number}: '{scene.title}'. "
            f"Shot Type: {shot_type.upper()} ({focal_length}mm lens), Camera Movement: {camera_mov}. "
            f"Lighting: {lighting}, Mood: {scene.visual_mood}. Action: {scene.action_description}."
        )

        return StoryboardShot(
            scene_number=scene.scene_number,
            shot_index=shot_index,
            shot_type=shot_type,
            camera_movement=camera_mov,
            focal_length_mm=focal_length,
            depth_of_field=dof,
            lighting_scheme=lighting,
            tension_level=t,
            aspect_ratio_16_9_bounds=bounds_16_9,
            vertical_9_16_safe_bounds=bounds_9_16,
            prompt=prompt,
        )

    @classmethod
    def generate_scene_storyboard_asset(
        cls, scene: SceneBeat, shot_index: int = 1
    ) -> VisualAsset:
        """
        Creates a core VisualAsset representing this storyboard frame.
        """
        shot = cls.calculate_shot_parameters(scene, shot_index=shot_index)

        return VisualAsset(
            asset_id=f"storyboard_scene_{scene.scene_number}_shot_{shot_index}",
            scene_number=scene.scene_number,
            asset_type="storyboard_frame",
            prompt=shot.prompt,
            render_url=f"https://directr.internal/storyboards/scene_{scene.scene_number}_s{shot_index}.json",
        )
