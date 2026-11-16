"""
Unit tests for Module 1: Narrative & Screenplay
"""

import unittest
from core.schemas import ProjectBrief, CharacterProfile
from modules.narrative_screenplay.engine import NarrativeScreenplayEngine


class TestNarrativeScreenplay(unittest.TestCase):
    def setUp(self):
        self.engine = NarrativeScreenplayEngine()

    def test_dialect_adaptation(self):
        rules = {"cannot": "can't", "peril": "danger", "mate": "friend"}
        original = "We cannot ignore this peril, mate!"
        adapted = self.engine.apply_dialect_rules(original, rules)
        self.assertIn("can't", adapted)
        self.assertIn("danger", adapted)
        self.assertIn("friend", adapted)

    def test_psychology_constraint_validation(self):
        character = CharacterProfile(
            id="char_1",
            name="Elena",
            archetype="Idealist Rebel",
            psychology_constraints=["Never Betray Allies", "Value Truth Above Safety"],
        )
        valid_actions = ["Seek the hidden transmitter", "Confront the commissioner"]
        self.assertTrue(self.engine.validate_psychology_constraints(character, valid_actions))

        invalid_actions = ["violate_never betray allies for money"]
        self.assertFalse(self.engine.validate_psychology_constraints(character, invalid_actions))

    def test_screenplay_generation(self):
        character = CharacterProfile(
            id="char_1",
            name="Kael",
            archetype="Cipher Rogue",
            dialect_rules={"cannot": "can't"},
        )
        brief = ProjectBrief(
            project_id="proj_001",
            title="Neon Shadows",
            genre="Cyberpunk Thriller",
            logline="A rogue cipher expert discovers a subterranean city conspiracy.",
            characters=[character],
        )

        scenes = self.engine.generate_screenplay(brief)
        self.assertEqual(len(scenes), 3)
        self.assertLess(scenes[0].tension_score, scenes[1].tension_score)
        self.assertGreaterEqual(len(scenes[1].foley_cues), 1)
        self.assertIn("can't", scenes[0].dialogue[0].line)


if __name__ == "__main__":
    unittest.main()
