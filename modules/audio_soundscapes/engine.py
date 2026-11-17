"""
Module 3: Music & Audio Studios Engine
Unifies dynamic stem arrangement, zero-shot Foley sound synthesis,
micro-tonal harmonic voicings, dialogue ducking, and spatial DSP mixdowns.
"""

from typing import List, Dict, Optional, Any
from core.schemas import SceneBeat, StemArrangement, FoleyAsset
from core.event_bus import EventBus

from .stems.arranger import DynamicStemArranger
from .stems.generator import ProceduralWavSynthesizer
from .foley.synthesizer import ZeroShotFoleySynthesizer
from .harmony.microtonal import MicrotonalScaleTuner
from .harmony.chord_progressions import MicrotonalChordBuilder
from .mixer.dsp_mixer import AudioMixDownEngine
from .mixer.ducking import DialogueSidechainDucker
from .mixer.spatializer import AcousticSpatializer


class AudioStudioEngine:
    """
    Facade engine for all audio and music studio functions.
    Exposes simple interfaces for the Core Swarm Orchestrator while leveraging
    dedicated sub-engines for stems, Foley, harmony, and DSP mixing.
    """

    def __init__(self, event_bus: Optional[EventBus] = None):
        self.bus = event_bus
        self.stem_arranger = DynamicStemArranger()
        self.foley_synthesizer = ZeroShotFoleySynthesizer()
        self.scale_tuner = MicrotonalScaleTuner()
        self.chord_builder = MicrotonalChordBuilder(self.scale_tuner)
        self.dsp_mixer = AudioMixDownEngine()
        self.ducker = DialogueSidechainDucker()
        self.spatializer = AcousticSpatializer()
        self.wav_synth = ProceduralWavSynthesizer()

    # -------------------------------------------------------------------------
    # 1. Dynamic Tension-Adaptive Stem Arrangements
    # -------------------------------------------------------------------------

    def map_tension_to_stems(self, tension_score: float) -> List[str]:
        """
        Dynamically shifts musical stem arrangements based on visual scene tension.
        """
        return self.stem_arranger.resolve_active_stems(tension_score)

    def arrange_soundscapes(self, scenes: List[SceneBeat]) -> List[StemArrangement]:
        """
        Calculates tempo BPM and active stem configuration for each scene
        based on dramatic tension curve.
        """
        arrangements = self.stem_arranger.arrange_multiple_scenes(scenes)
        if self.bus:
            self.bus.publish("audio.stems_arranged", {"arrangements_count": len(arrangements)})
        return arrangements

    # -------------------------------------------------------------------------
    # 2. Zero-Shot Cinematic Foley Sound Effects
    # -------------------------------------------------------------------------

    def synthesize_foley_cues(self, scenes: List[SceneBeat]) -> List[FoleyAsset]:
        """
        Synthesizes zero-shot cinematic Foley sound effects from text cues and action descriptions.
        """
        foley_assets = self.foley_synthesizer.process_scene_foley_cues(scenes)
        if self.bus:
            self.bus.publish("audio.foley_synthesized", {"foley_count": len(foley_assets)})
        return foley_assets

    # -------------------------------------------------------------------------
    # 3. AI-Driven Micro-Tonal Harmony Engine
    # -------------------------------------------------------------------------

    def compute_microtonal_harmony(
        self, root_hz: float = 440.0, temperament_cents: Optional[List[int]] = None
    ) -> List[float]:
        """
        AI-driven vocal harmony arrangement matching micro-tonal scale intervals.
        Default: 24-EDO quarter-tone intervals (cents offset from root).
        """
        if temperament_cents is None:
            temperament_cents = [0, 150, 350, 700, 850]

        frequencies = [
            self.scale_tuner.cents_to_frequency(c, root_hz) for c in temperament_cents
        ]
        return frequencies

    def get_psychological_chord(self, emotion_or_valence: str, root_hz: float = 220.0) -> Dict[str, Any]:
        """
        Constructs evocative microtonal chord voicing based on character psychological state.
        """
        return self.chord_builder.match_emotion_to_chord(emotion_or_valence, root_hz)

    # -------------------------------------------------------------------------
    # 4. Multi-Track Master Mix & DSP Spatializer
    # -------------------------------------------------------------------------

    def generate_scene_master_mix(
        self, scene: SceneBeat, arrangement: StemArrangement, foley_assets: List[FoleyAsset]
    ) -> Dict[str, Any]:
        """
        Builds a comprehensive synchronized master mix manifest for a scene,
        incorporating stem channels, dialogue sidechain ducking, and room acoustic spatialization.
        """
        return self.dsp_mixer.build_scene_mix_manifest(scene, arrangement, foley_assets)
