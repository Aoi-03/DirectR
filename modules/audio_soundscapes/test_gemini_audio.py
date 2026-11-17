"""
Test suite for Gemini Audio Engine in Module 3.
Includes offline unit tests and live Gemini API verification tests.
"""

import unittest
from modules.audio_soundscapes.gemini_audio import GeminiAudioEngine


class TestGeminiAudioEngine(unittest.TestCase):
    def setUp(self):
        self.gemini = GeminiAudioEngine()

    def test_initialization_and_models(self):
        self.assertIsNotNone(self.gemini.SUPPORTED_MODELS)
        self.assertIn("gemini-3-flash-preview", self.gemini.SUPPORTED_MODELS)
        self.assertIn("gemini-flash-latest", self.gemini.SUPPORTED_MODELS)

    def test_json_cleaner(self):
        raw_markdown = '```json\n{\n  "tempo_bpm": 128,\n  "key": "D Minor"\n}\n```'
        parsed = self.gemini._clean_and_parse_json(raw_markdown)
        self.assertEqual(parsed.get("tempo_bpm"), 128)
        self.assertEqual(parsed.get("key"), "D Minor")

    def test_live_gemini_soundscape_generation(self):
        """
        Runs live test when GEMINI_API_KEY is configured in .env.
        If key is not set, skips gracefully.
        """
        if not self.gemini.is_configured():
            self.skipTest(
                "GEMINI_API_KEY not found in .env yet. Paste your key into .env to execute live test."
            )

        print("\n🚀 Executing LIVE Gemini Soundscape Composition Call...")
        result = self.gemini.generate_soundscape_composition(
            scene_title="Vault Infiltration",
            tension_score=0.88,
            visual_mood="Cyberpunk Noir",
            location="Subterranean Server Vault",
            action_description="Laser grid activates as security drones descend from ceiling",
        )

        self.assertIsInstance(result, dict)
        self.assertIn("tempo_bpm", result)
        self.assertIn("lyria_musiclm_prompt", result)
        self.assertTrue(len(result["lyria_musiclm_prompt"]) > 10)
        print(f"✅ Gemini Live Tempo: {result.get('tempo_bpm')} BPM")
        print(f"✅ Gemini Live Lyria Prompt: {result.get('lyria_musiclm_prompt')[:80]}...")

    def test_live_gemini_foley_design(self):
        """
        Runs live Foley sound design test when GEMINI_API_KEY is configured in .env.
        """
        if not self.gemini.is_configured():
            self.skipTest(
                "GEMINI_API_KEY not found in .env yet. Paste your key into .env to execute live test."
            )

        print("\n🚀 Executing LIVE Gemini Zero-Shot Foley Design Call...")
        result = self.gemini.design_zero_shot_foley(
            cue_name="LaserTripwireSnap",
            cue_description="High-frequency plasma beam cut by intruder boot with metallic reverberation",
            scene_location="Underground Vault",
        )

        self.assertIsInstance(result, dict)
        self.assertIn("detected_material", result)
        self.assertIn("envelope", result)
        print(f"✅ Gemini Detected Material: {result.get('detected_material')}")
        print(f"✅ Gemini Envelope: {result.get('envelope')}")

    def test_live_gemini_microtonal_harmony(self):
        """
        Runs live microtonal chord design test when GEMINI_API_KEY is configured in .env.
        """
        if not self.gemini.is_configured():
            self.skipTest(
                "GEMINI_API_KEY not found in .env yet. Paste your key into .env to execute live test."
            )

        print("\n🚀 Executing LIVE Gemini Microtonal Harmony Call...")
        result = self.gemini.design_microtonal_harmony(
            scene_mood="Surreal Cyberpunk Mystery",
            character_psychology="Paranoid archivist discovering forbidden AI consciousness",
            root_note_hz=220.0,
        )

        self.assertIsInstance(result, dict)
        self.assertIn("intervals_cents", result)
        self.assertIn("computed_frequencies_hz", result)
        print(f"✅ Gemini Microtonal Voicing: {result.get('voicing_name')}")
        print(f"✅ Gemini Intervals: {result.get('intervals_cents')}")


if __name__ == "__main__":
    unittest.main()
