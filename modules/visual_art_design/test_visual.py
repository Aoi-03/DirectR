"""
Unit tests for Module 2: Visual Art & Design Assist
Covers layered SVG synthesis, Bezier anchor nodes, 5-angle turnarounds,
skeletal topology landmarks, inpainting masks, and cinematic storyboard framing.
"""

import unittest
from core.schemas import CharacterProfile, ProjectBrief, SceneBeat
from core.event_bus import EventBus
from modules.visual_art_design.engine import VisualArtEngine
from modules.visual_art_design.vector.palette_generator import PaletteGenerator
from modules.visual_art_design.turnaround.rigging_engine import CharacterTurnaroundEngine
from modules.visual_art_design.inpainting.sketch_pipeline import InpaintingPipeline
from modules.visual_art_design.storyboard.storyboard_director import StoryboardDirector


class TestVisualArtDesign(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus()
        self.engine = VisualArtEngine(event_bus=self.bus)

    def test_layered_svg_synthesis(self):
        """Test parametric SVG synthesis with default layers and anchor nodes."""
        layers = ["sky", "mountains", "character", "atmosphere"]
        res = self.engine.generate_layered_svg("Cyberpunk alleyway", 1, layers=layers)
        self.assertIn("<svg", res["svg_markup"])
        self.assertIn("</svg>", res["svg_markup"])
        self.assertGreaterEqual(res["anchor_nodes_count"], 16)
        self.assertEqual(len(res["layer_names"]), 4)
        self.assertIn("palette", res)

    def test_mood_palette_mapping(self):
        """Test color palette selection based on visual mood and tension."""
        palette_cyber = PaletteGenerator.get_palette_for_scene("Cyberpunk Noir", tension_score=0.4)
        self.assertEqual(palette_cyber.palette_name, "Cyberpunk Noir")
        self.assertEqual(palette_cyber.secondary, "#00f3ff")

        # High tension override (> 0.75)
        palette_crisis = PaletteGenerator.get_palette_for_scene("Cyberpunk Noir", tension_score=0.9)
        self.assertEqual(palette_crisis.palette_name, "High-Tension Neon Alert")

        # Dawn mood
        palette_dawn = PaletteGenerator.get_palette_for_scene("Moody Cinematic", setting_time="DAWN")
        self.assertEqual(palette_dawn.palette_name, "Golden Dawn Horizon")

    def test_character_turnaround(self):
        """Test multi-angle turnaround generation with 5 orthographic angles."""
        character = CharacterProfile(
            id="char_test",
            name="Aria",
            archetype="Cybernetic Pilot",
            backstory="Survived deep orbital transit.",
        )
        asset = self.engine.generate_character_turnaround(character)
        self.assertEqual(asset.asset_type, "turnaround_sheet")
        self.assertIn("front", asset.turnaround_angles)
        self.assertIn("back", asset.turnaround_angles)
        self.assertIn("profile", asset.turnaround_angles)
        self.assertIn("three_quarters_front", asset.turnaround_angles)
        self.assertIn("Rig-ready topology", asset.prompt)

    def test_skeletal_topology_landmarks(self):
        """Test 15-joint humanoid skeletal rig landmarks and OpenPose config."""
        spec = CharacterTurnaroundEngine.generate_skeletal_topology(stance="A-Pose")
        self.assertEqual(spec.stance, "A-Pose")
        self.assertEqual(len(spec.joints), 15)
        joint_names = [j.name for j in spec.joints]
        self.assertIn("nose", joint_names)
        self.assertIn("neck", joint_names)
        self.assertIn("left_wrist", joint_names)
        self.assertIn("right_ankle", joint_names)

        # Check normalization bounds
        for j in spec.joints:
            self.assertTrue(0.0 <= j.x <= 1.0)
            self.assertTrue(0.0 <= j.y <= 1.0)

    def test_inpainting_mask_pipeline(self):
        """Test localized inpainting mask creation and SVG mask rendering."""
        task = self.engine.create_inpainting_job(
            task_id="inpaint_001",
            target_layer_id="layer_foreground",
            bounding_box=(400, 300, 800, 700),
            semantic_label="cybernetic_arm",
            mode="feature_redesign",
        )
        self.assertEqual(task.semantic_label, "cybernetic_arm")
        self.assertEqual(task.denoising_strength, 0.68)
        self.assertIn("blurry", task.negative_prompt)

        # Generate SVG mask
        mask_svg = InpaintingPipeline.generate_mask_svg(1920, 1080, task.bounding_box)
        self.assertIn('<rect width="1920" height="1080" fill="#000000"', mask_svg)
        self.assertIn('fill="#ffffff"', mask_svg)

    def test_storyboard_cinematography_framing(self):
        """Test dynamic shot type selection and 9:16 vertical crop bounds."""
        scene_calm = SceneBeat(
            scene_number=1,
            title="Calm Dawn",
            location="Overlook",
            action_description="Wind blows through high grasses.",
            visual_mood="Moody Cinematic",
            tension_score=0.25,
        )
        shot_calm = StoryboardDirector.calculate_shot_parameters(scene_calm)
        self.assertEqual(shot_calm.shot_type, "wide")
        self.assertEqual(shot_calm.focal_length_mm, 24)

        scene_climax = SceneBeat(
            scene_number=2,
            title="Final Breach",
            location="Vault",
            action_description="Explosive charge shatters the blast doors.",
            visual_mood="Cyberpunk Crisis",
            tension_score=0.92,
        )
        shot_climax = StoryboardDirector.calculate_shot_parameters(scene_climax)
        self.assertEqual(shot_climax.shot_type, "dutch_tilt")
        self.assertEqual(shot_climax.focal_length_mm, 18)

        # Verify 9:16 vertical crop bounds for Module 4 Reels
        # 1080 height * (9/16) = 607.5 -> 607px width centered in 1920
        safe_x1, safe_y1, safe_x2, safe_y2 = shot_climax.vertical_9_16_safe_bounds
        self.assertEqual(safe_y1, 0)
        self.assertEqual(safe_y2, 1080)
        self.assertTrue(safe_x1 > 0)
        self.assertTrue(safe_x2 < 1920)

    def test_produce_visual_package_integration(self):
        """Test full end-to-end visual package production."""
        brief = ProjectBrief(
            project_id="test_proj",
            title="Neon Horizon",
            genre="Sci-Fi",
            logline="A test adventure.",
            characters=[
                CharacterProfile(id="c1", name="Kai", archetype="Hacker"),
                CharacterProfile(id="c2", name="Vex", archetype="Enforcer"),
            ],
        )
        scenes = [
            SceneBeat(
                scene_number=1,
                title="Scene 1",
                location="Neon Docks",
                action_description="Rain falls on docks.",
                visual_mood="Cyberpunk Noir",
                tension_score=0.35,
            ),
            SceneBeat(
                scene_number=2,
                title="Scene 2",
                location="Core Reactor",
                action_description="Alarms blare as core overheats.",
                visual_mood="Crisis Neon",
                tension_score=0.88,
            ),
        ]

        assets = self.engine.produce_visual_package(brief, scenes)

        # Expected: 2 turnarounds + 2 layered SVGs + 2 storyboard frames = 6 assets
        self.assertEqual(len(assets), 6)
        types = [a.asset_type for a in assets]
        self.assertEqual(types.count("turnaround_sheet"), 2)
        self.assertEqual(types.count("layered_svg"), 2)
        self.assertEqual(types.count("storyboard_frame"), 2)


if __name__ == "__main__":
    unittest.main()
