"""
Zero-Shot Foley Synthesizer
Transforms natural language text cues into synthesized cinematic sound effects.
"""

import math
import struct
import io
import wave
import random
from typing import List, Dict, Any, Optional
from core.schemas import SceneBeat, FoleyCue, FoleyAsset
from .sound_library import FOLEY_MATERIAL_PROFILES, FoleyMaterialProfile


class ZeroShotFoleySynthesizer:
    """
    Parses textual action and environmental cues to synthesize cinematic Foley sound effects.
    """

    SAMPLE_RATE = 44100

    def __init__(self):
        self.profiles = FOLEY_MATERIAL_PROFILES

    def match_material_profile(self, text_cue: str) -> FoleyMaterialProfile:
        """
        Extracts material and acoustic resonance attributes by semantic keyword matching.
        Defaults to metallic_impact if no direct match.
        """
        cue_lower = text_cue.lower()
        best_match = None
        max_score = 0

        for key, profile in self.profiles.items():
            score = sum(1 for kw in profile.keywords if kw in cue_lower)
            if score > max_score:
                max_score = score
                best_match = profile

        return best_match or self.profiles["metallic_impact"]

    def synthesize_cue_audio(
        self, profile: FoleyMaterialProfile, duration_sec: float = 1.5
    ) -> bytes:
        """
        Synthesizes parametric sound waveform based on material acoustic properties.
        """
        num_samples = int(self.SAMPLE_RATE * duration_sec)
        samples = []
        decay_factor = profile.decay_ms / 1000.0

        for i in range(num_samples):
            t = i / self.SAMPLE_RATE
            # Exponential decay envelope
            envelope = math.exp(-t / max(0.01, decay_factor))
            if t < (profile.attack_ms / 1000.0):
                envelope *= t / max(0.001, (profile.attack_ms / 1000.0))

            # Resonant oscillation + noise texture
            osc = math.sin(2.0 * math.pi * profile.base_frequency_hz * t)
            noise = (random.random() * 2.0 - 1.0) * (0.3 if profile.noise_color == "white" else 0.15)

            val = envelope * (0.7 * osc + 0.3 * noise)
            clamped = max(-1.0, min(1.0, val))
            samples.append(int(clamped * 32767))

        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.SAMPLE_RATE)
            packed = struct.pack(f"<{len(samples)}h", *samples)
            wav_file.writeframes(packed)

        return buffer.getvalue()

    def process_foley_cue(self, cue: FoleyCue) -> FoleyAsset:
        """
        Synthesizes a FoleyAsset from a single FoleyCue descriptor.
        """
        profile = self.match_material_profile(cue.description)
        duration = max(1.0, min(5.0, profile.decay_ms / 300.0))

        return FoleyAsset(
            cue_name=cue.cue_name,
            synthesized_from_text=cue.description,
            duration_seconds=round(duration, 2),
            audio_format="wav",
            audio_uri=f"assets/audio/foley/{cue.cue_name.lower()}.wav",
        )

    def process_scene_foley_cues(self, scenes: List[SceneBeat]) -> List[FoleyAsset]:
        """
        Iterates over all scenes, synthesizing all embedded Foley cues.
        """
        assets: List[FoleyAsset] = []
        for scene in scenes:
            for cue in scene.foley_cues:
                asset = self.process_foley_cue(cue)
                assets.append(asset)
        return assets
