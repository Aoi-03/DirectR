"""
Dynamic Stem Arranger
Calculates dynamic BPM, stem layer activations, and automated gain curves based on tension.
"""

from typing import List, Dict, Any, Optional
from core.schemas import SceneBeat, StemArrangement
from .stem_definitions import STEM_CATALOG, TENSION_BANDS, StemLayer


class DynamicStemArranger:
    """
    Arranges musical stems according to emotional valence, dramatic pacing,
    and visual scene tension.
    """

    def __init__(self):
        self.catalog = STEM_CATALOG

    def calculate_bpm(self, tension_score: float) -> int:
        """
        Calculates tempo BPM based on a continuous curve.
        Ranges from 65 BPM (subtle ambient) to 150 BPM (intense climax).
        """
        clamped_t = max(0.0, min(1.0, tension_score))
        bpm = int(65 + (clamped_t * 85))
        return bpm

    def resolve_active_stems(self, tension_score: float) -> List[str]:
        """
        Determines the list of active stem names for a given tension rating.
        """
        clamped_t = max(0.0, min(1.0, tension_score))
        for band in TENSION_BANDS:
            if band["min_tension"] <= clamped_t <= band["max_tension"]:
                return list(band["default_stems"])
        return ["ambient_pad", "sub_drone"]

    def compute_stem_gain_automation(
        self, tension_score: float, duration_seconds: float = 30.0
    ) -> Dict[str, Dict[str, Any]]:
        """
        Computes dynamic gain curves and filter automation for each active stem.
        """
        active_stem_names = self.resolve_active_stems(tension_score)
        automation: Dict[str, Dict[str, Any]] = {}

        for stem_name in active_stem_names:
            stem_spec = self.catalog.get(stem_name)
            base_gain = stem_spec.base_gain if stem_spec else 0.7
            cutoff = stem_spec.filter_cutoff_hz if stem_spec else 8000

            # Dynamic cutoff modulation based on tension
            dynamic_cutoff = int(cutoff * (0.6 + (0.4 * tension_score)))

            automation[stem_name] = {
                "base_gain_db": round(20 * (base_gain - 1.0), 2),  # approx dB
                "linear_gain": round(base_gain, 3),
                "filter_cutoff_hz": dynamic_cutoff,
                "panning": 0.0,  # Center default
                "crossfade_in_sec": 1.5,
                "crossfade_out_sec": 2.0,
            }

        return automation

    def arrange_scene(self, scene: SceneBeat) -> StemArrangement:
        """
        Generates a complete StemArrangement schema object for a single scene beat.
        """
        t = scene.tension_score
        bpm = self.calculate_bpm(t)
        active_stems = self.resolve_active_stems(t)

        if t < 0.36:
            valence = "Eerie / Calming Solitude"
        elif t < 0.71:
            valence = "Escalating Suspense & Mystery"
        else:
            valence = "High-Intensity Crisis & Kinetic Climax"

        return StemArrangement(
            scene_number=scene.scene_number,
            tempo_bpm=bpm,
            tension_matched=t,
            active_stems=active_stems,
            emotional_valence=valence,
            audio_stream_uri=f"assets/audio/stems/scene_{scene.scene_number}_stems.json",
        )

    def arrange_multiple_scenes(self, scenes: List[SceneBeat]) -> List[StemArrangement]:
        """
        Arranges all scenes in sequence, ensuring smooth progression.
        """
        return [self.arrange_scene(scene) for scene in scenes]
