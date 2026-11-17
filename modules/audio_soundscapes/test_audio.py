"""
Unit tests for Module 3: Music & Audio Studios
Tests stems, zero-shot Foley, microtonal harmony, dialogue ducking, and DSP spatialization.
"""

import unittest
from core.schemas import SceneBeat, FoleyCue, DialogueLine
from modules.audio_soundscapes.engine import AudioStudioEngine
from modules.audio_soundscapes.stems.generator import ProceduralWavSynthesizer
from modules.audio_soundscapes.stems.arranger import DynamicStemArranger
from modules.audio_soundscapes.foley.synthesizer import ZeroShotFoleySynthesizer
from modules.audio_soundscapes.harmony.microtonal import MicrotonalScaleTuner
from modules.audio_soundscapes.harmony.chord_progressions import MicrotonalChordBuilder
from modules.audio_soundscapes.mixer.ducking import DialogueSidechainDucker
from modules.audio_soundscapes.mixer.spatializer import AcousticSpatializer


class TestAudioSoundscapes(unittest.TestCase):
    def setUp(self):
        self.engine = AudioStudioEngine()

    # 1. Stem Engine Tests
    def test_tension_to_stem_mapping(self):
        low_stems = self.engine.map_tension_to_stems(0.2)
        self.assertIn("ambient_pad", low_stems)
        self.assertNotIn("heavy_industrial_drums", low_stems)

        high_stems = self.engine.map_tension_to_stems(0.9)
        self.assertIn("heavy_industrial_drums", high_stems)
        self.assertIn("distorted_808", high_stems)

    def test_bpm_calculation_curve(self):
        arranger = DynamicStemArranger()
        self.assertEqual(arranger.calculate_bpm(0.0), 65)
        self.assertEqual(arranger.calculate_bpm(1.0), 150)
        self.assertTrue(65 <= arranger.calculate_bpm(0.5) <= 150)

    def test_procedural_wav_generation(self):
        wav_bytes = ProceduralWavSynthesizer.generate_sine_tone(440.0, duration_sec=0.1)
        self.assertTrue(len(wav_bytes) > 44)  # RIFF header + samples
        self.assertTrue(wav_bytes.startswith(b"RIFF"))

        riser_bytes = ProceduralWavSynthesizer.generate_tension_riser(100, 500, duration_sec=0.1)
        self.assertTrue(riser_bytes.startswith(b"RIFF"))

    # 2. Foley Engine Tests
    def test_foley_material_matching(self):
        foley_synth = ZeroShotFoleySynthesizer()
        profile_rain = foley_synth.match_material_profile("Persistent rain tapping on steel roof")
        self.assertEqual(profile_rain.category, "ambient_weather")

        profile_spark = foley_synth.match_material_profile("High voltage electrical sparks from severed cable")
        self.assertEqual(profile_spark.category, "electrical")

    def test_foley_synthesis_audio(self):
        foley_synth = ZeroShotFoleySynthesizer()
        profile = foley_synth.match_material_profile("metal sword clang")
        audio_data = foley_synth.synthesize_cue_audio(profile, duration_sec=0.2)
        self.assertTrue(audio_data.startswith(b"RIFF"))

    # 3. Microtonal Harmony Tests
    def test_microtonal_scale_24edo(self):
        tuner = MicrotonalScaleTuner(edo_divisions=24, reference_hz=440.0)
        scale = tuner.generate_microtonal_scale(root_hz=440.0)
        self.assertEqual(len(scale), 24)
        self.assertEqual(scale[0].frequency_hz, 440.0)
        # 1st quarter-tone (50 cents) must be higher than root
        self.assertGreater(scale[1].frequency_hz, 440.0)
        # Neutral third (step 7 = 350 cents)
        self.assertEqual(scale[7].cents, 350.0)

    def test_psychological_chord_voicings(self):
        chord = self.engine.get_psychological_chord("uncanny mystery", root_hz=220.0)
        self.assertEqual(chord["preset_name"], "uncanny_submerged")
        self.assertEqual(len(chord["frequencies_hz"]), 4)

    # 4. Mixer & Spatializer Tests
    def test_dialogue_sidechain_ducking(self):
        ducker = DialogueSidechainDucker(attenuation_db=-12.0)
        scene = SceneBeat(
            scene_number=1,
            title="Confrontation",
            location="Underground Vault",
            action_description="Argue over the key",
            visual_mood="Dark",
            tension_score=0.75,
            dialogue=[
                DialogueLine(speaker="Lyra", line="The perimeter is completely breached!", emotion="Urgent"),
                DialogueLine(speaker="Kael", line="Hold the line, don't run!", emotion="Defiant"),
            ]
        )
        profile = ducker.calculate_ducking_profile(scene)
        self.assertTrue(profile["sidechain_active"])
        self.assertEqual(profile["ducked_gain_db"], -12.0)
        self.assertEqual(len(profile["dialogue_events"]), 2)

    def test_acoustic_spatializer(self):
        spatializer = AcousticSpatializer()
        space = spatializer.infer_acoustic_space("Underground Subterranean Cipher Vault")
        self.assertEqual(space["inferred_preset"], "underground_vault")
        self.assertGreater(space["decay_time_sec"], 2.0)

    # 5. Full End-to-End Scene Master Mix
    def test_full_scene_master_mix(self):
        scene = SceneBeat(
            scene_number=2,
            title="The Cathedral Encounter",
            location="Grand Gothic Cathedral",
            action_description="Sparks fly as the vault opens",
            visual_mood="Cyberpunk Mystery",
            tension_score=0.85,
            dialogue=[
                DialogueLine(speaker="Lyra", line="Look at the architecture shifting!", emotion="Awe")
            ],
            foley_cues=[
                FoleyCue(cue_name="Sparks", description="Electric spark discharge", trigger_beat_second=5.0)
            ]
        )
        arrangements = self.engine.arrange_soundscapes([scene])
        foley_assets = self.engine.synthesize_foley_cues([scene])

        master_mix = self.engine.generate_scene_master_mix(scene, arrangements[0], foley_assets)
        self.assertEqual(master_mix["scene_number"], 2)
        self.assertGreater(master_mix["tempo_bpm"], 120)
        self.assertEqual(master_mix["stems_channel_count"], len(arrangements[0].active_stems))
        self.assertTrue(master_mix["ducking"]["sidechain_active"])
        self.assertEqual(master_mix["spatial_acoustics"]["inferred_preset"], "cathedral_vast")


if __name__ == "__main__":
    unittest.main()
