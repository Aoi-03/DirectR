"""
Unit tests for Module 3: Music & Audio Studios
"""

import unittest
from core.schemas import SceneBeat, FoleyCue
from modules.audio_soundscapes.engine import AudioStudioEngine


class TestAudioSoundscapes(unittest.TestCase):
    def setUp(self):
        self.engine = AudioStudioEngine()

    def test_tension_to_stem_mapping(self):
        low_stems = self.engine.map_tension_to_stems(0.2)
        self.assertIn("ambient_pad", low_stems)
        self.assertNotIn("heavy_industrial_drums", low_stems)

        high_stems = self.engine.map_tension_to_stems(0.9)
        self.assertIn("heavy_industrial_drums", high_stems)
        self.assertIn("distorted_808", high_stems)

    def test_soundscape_arrangement(self):
        scene = SceneBeat(
            scene_number=1,
            title="Chase",
            location="Roof",
            action_description="Running across rooftops",
            visual_mood="Dark",
            tension_score=0.8,
            foley_cues=[
                FoleyCue(cue_name="FootstepGravel", description="Boot crunching gravel", trigger_beat_second=1.0)
            ]
        )
        arrangements = self.engine.arrange_soundscapes([scene])
        self.assertEqual(len(arrangements), 1)
        self.assertGreaterEqual(arrangements[0].tempo_bpm, 120)
        self.assertEqual(arrangements[0].tension_matched, 0.8)

    def test_microtonal_harmony(self):
        freqs = self.engine.compute_microtonal_harmony(440.0)
        self.assertEqual(len(freqs), 5)
        self.assertEqual(freqs[0], 440.0)
        self.assertGreater(freqs[1], 440.0)


if __name__ == "__main__":
    unittest.main()
