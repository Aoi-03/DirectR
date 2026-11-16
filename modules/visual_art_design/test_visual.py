"""
Unit tests for Module 2: Visual Art & Design Assist
"""

import unittest
from core.schemas import CharacterProfile
from modules.visual_art_design.engine import VisualArtEngine


class TestVisualArtDesign(unittest.TestCase):
    def setUp(self):
        self.engine = VisualArtEngine()

    def test_layered_svg_synthesis(self):
        layers = ["sky", "mountains", "character", "atmosphere"]
        res = self.engine.generate_layered_svg("Cyberpunk alleyway", 1, layers)
        self.assertIn("<svg", res["svg_markup"])
        self.assertIn("</svg>", res["svg_markup"])
        self.assertEqual(res["anchor_nodes_count"], 16)
        self.assertEqual(len(res["layer_names"]), 4)

    def test_character_turnaround(self):
        character = CharacterProfile(
            id="char_test",
            name="Aria",
            archetype="Cybernetic Pilot",
        )
        asset = self.engine.generate_character_turnaround(character)
        self.assertEqual(asset.asset_type, "turnaround_sheet")
        self.assertEqual(asset.turnaround_angles, ["front", "three_quarters", "side", "back"])
        self.assertIn("Rig-ready topology", asset.prompt)


if __name__ == "__main__":
    unittest.main()
