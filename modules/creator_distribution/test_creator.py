"""
Unit tests for Module 4: Creator Agents & Distribution
"""

import unittest
from core.schemas import SceneBeat, ProjectBrief, DialogueLine
from modules.creator_distribution.engine import CreatorDistributionEngine


class TestCreatorDistribution(unittest.TestCase):
    def setUp(self):
        self.engine = CreatorDistributionEngine()

    def test_vertical_reel_extraction(self):
        scenes = [
            SceneBeat(
                scene_number=1,
                title="Calm Intro",
                location="Room",
                action_description="Sitting",
                visual_mood="Quiet",
                tension_score=0.2,
            ),
            SceneBeat(
                scene_number=2,
                title="Action Climax",
                location="Alley",
                action_description="Running from drones",
                visual_mood="Dark",
                tension_score=0.88,
                dialogue=[DialogueLine(speaker="Kael", line="Run, don't look back!", emotion="Terrified")],
            ),
        ]

        reels = self.engine.extract_tension_reels(scenes, min_tension_threshold=0.65)
        self.assertEqual(len(reels), 1)
        self.assertEqual(reels[0].source_scene_number, 2)
        self.assertEqual(reels[0].vertical_aspect_ratio, "9:16")
        self.assertIn("Run, don't look back!", reels[0].hook_text)

    def test_thumbnail_ab_variants(self):
        brief = ProjectBrief(
            project_id="p1",
            title="DirectR Odyssey",
            genre="Sci-Fi",
            logline="AI film revolution",
        )
        variants = self.engine.generate_thumbnail_variants(brief, [])
        self.assertEqual(len(variants), 3)
        best = max(variants, key=lambda v: v.attention_heatmap_score)
        self.assertGreater(best.attention_heatmap_score, 90.0)

    def test_community_response(self):
        response = self.engine.respond_to_community_comment("The background music in scene 2 gave me chills!")
        self.assertIn("adaptive audio", response.generated_response.lower())
        self.assertEqual(response.sentiment, "Positive")


if __name__ == "__main__":
    unittest.main()
