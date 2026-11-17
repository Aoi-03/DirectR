"""
Microtonal Scale Tuner & Frequency Calculator
Computes frequencies, cents intervals, and MIDI pitch-bend offsets
for 24-EDO (quarter-tones) and non-Western microtonal temperaments.
"""

import math
from typing import List, Dict, Tuple, Optional
from pydantic import BaseModel


class MicrotonalInterval(BaseModel):
    name: str
    cents: float
    frequency_hz: float
    midi_note_base: int
    pitch_bend_val: int  # 0 to 16383, 8192 is center (0 bend)
    ratio_approx: str


class MicrotonalScaleTuner:
    """
    Mathematical tuner for micro-tonal temperaments (default 24-EDO quarter-tone system).
    Standard Western octave = 1200 cents (12 semitones of 100 cents each).
    24-EDO divides the octave into 24 equal steps of 50 cents each.
    """

    A4_REFERENCE_HZ = 440.0
    MIDI_A4 = 69

    def __init__(self, edo_divisions: int = 24, reference_hz: float = 440.0):
        self.divisions = edo_divisions
        self.step_cents = 1200.0 / self.divisions
        self.reference_hz = reference_hz

    def cents_to_frequency(self, cents: float, root_hz: float = 440.0) -> float:
        """Calculates frequency: f = f0 * 2^(cents / 1200)."""
        return round(root_hz * math.pow(2.0, cents / 1200.0), 2)

    def calculate_pitch_bend_value(self, cents_offset: float, bend_range_semitones: int = 2) -> int:
        """
        Converts cents offset into 14-bit MIDI pitch-bend value (0-16383).
        Center (no bend) = 8192.
        Bend range = +/- (bend_range_semitones * 100) cents.
        """
        max_cents = bend_range_semitones * 100.0
        normalized = max(-1.0, min(1.0, cents_offset / max_cents))
        midi_val = int(8192 + (normalized * 8191))
        return midi_val

    def generate_microtonal_scale(
        self, root_hz: float = 440.0, root_midi_note: int = 69
    ) -> List[MicrotonalInterval]:
        """
        Generates full 24-EDO quarter-tone chromatic scale over one octave.
        """
        scale: List[MicrotonalInterval] = []

        quarter_tone_names = [
            "Root",
            "Quarter-tone Sharp",
            "Minor Second (Half-step)",
            "Three-quarter-tone Sharp",
            "Major Second",
            "Neutral Third (Sub-minor)",
            "Minor Third",
            "Neutral Third (Super-minor)",
            "Major Third",
            "Super-major Third",
            "Perfect Fourth",
            "Quarter-tone Sharp Fourth",
            "Tritone",
            "Quarter-tone Flat Fifth",
            "Perfect Fifth",
            "Quarter-tone Sharp Fifth",
            "Minor Sixth",
            "Neutral Sixth",
            "Major Sixth",
            "Super-major Sixth",
            "Minor Seventh",
            "Harmonic Seventh",
            "Major Seventh",
            "Quarter-tone Flat Octave",
        ]

        for step in range(self.divisions):
            cents = step * self.step_cents
            freq = self.cents_to_frequency(cents, root_hz)

            # Determine closest standard 12-TET semitone and cents offset
            semitones = round(cents / 100.0)
            offset = cents - (semitones * 100.0)
            base_midi = root_midi_note + semitones
            bend_val = self.calculate_pitch_bend_value(offset)

            name = quarter_tone_names[step] if step < len(quarter_tone_names) else f"Step {step}"

            scale.append(
                MicrotonalInterval(
                    name=name,
                    cents=round(cents, 2),
                    frequency_hz=freq,
                    midi_note_base=base_midi,
                    pitch_bend_val=bend_val,
                    ratio_approx=f"2^({step}/{self.divisions})",
                )
            )

        return scale
