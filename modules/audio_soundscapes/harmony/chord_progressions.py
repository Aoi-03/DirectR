"""
Microtonal Chord & Voice Leading Builder
Constructs psychological scene harmonies with micro-intervals (neutral thirds, quarter-tones).
"""

from typing import List, Dict, Any
from .microtonal import MicrotonalScaleTuner


class MicrotonalChordBuilder:
    """
    Constructs expressive microtonal voicings matching character psychological states.
    """

    PSYCHOLOGICAL_PRESETS: Dict[str, List[int]] = {
        # Interval cents from root:
        "uncanny_submerged": [0, 350, 700, 1050],  # Neutral third + neutral seventh (Arabian Rast flavor)
        "dystopian_paranoia": [0, 150, 600, 850],  # Quarter-tone sharp second + tritone + neutral sixth
        "cyber_mysticism": [0, 250, 700, 950],   # Sub-minor third + harmonic resonance
        "hyper_tension_crisis": [0, 150, 550, 600, 1150],  # Microtonal clusters creating extreme acoustic dissonance
        "peaceful_solitude": [0, 400, 700, 1100],  # Consonant Western major with pure fifth
    }

    def __init__(self, tuner: MicrotonalScaleTuner = None):
        self.tuner = tuner or MicrotonalScaleTuner()

    def build_chord_voicing(
        self, preset_name: str, root_hz: float = 220.0
    ) -> Dict[str, Any]:
        """
        Builds frequencies, cents, and descriptive harmonic notes for a chosen emotional preset.
        """
        intervals_cents = self.PSYCHOLOGICAL_PRESETS.get(
            preset_name, self.PSYCHOLOGICAL_PRESETS["uncanny_submerged"]
        )

        frequencies = [
            self.tuner.cents_to_frequency(c, root_hz) for c in intervals_cents
        ]

        return {
            "preset_name": preset_name,
            "root_hz": root_hz,
            "intervals_cents": intervals_cents,
            "frequencies_hz": frequencies,
            "voice_count": len(frequencies),
            "description": f"Microtonal chord for '{preset_name}' featuring intervals: {intervals_cents}",
        }

    def match_emotion_to_chord(self, emotion: str, root_hz: float = 220.0) -> Dict[str, Any]:
        """
        Maps emotional valence to appropriate microtonal preset.
        """
        emo = emotion.lower()
        if "crisis" in emo or "high" in emo or "panic" in emo:
            preset = "hyper_tension_crisis"
        elif "eerie" in emo or "mystery" in emo or "noir" in emo:
            preset = "uncanny_submerged"
        elif "paranoia" in emo or "urgent" in emo:
            preset = "dystopian_paranoia"
        elif "mystic" in emo or "sacred" in emo:
            preset = "cyber_mysticism"
        else:
            preset = "peaceful_solitude"

        return self.build_chord_voicing(preset, root_hz)
