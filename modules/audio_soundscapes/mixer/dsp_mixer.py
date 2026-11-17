"""
DSP Audio Mixdown Engine
Coordinates stems, Foley cues, sidechain ducking, and spatial parameters into a unified mix configuration.
"""

from typing import List, Dict, Any
from core.schemas import SceneBeat, StemArrangement, FoleyAsset
from .ducking import DialogueSidechainDucker
from .spatializer import AcousticSpatializer


class AudioMixDownEngine:
    """
    Assembles a full multi-track master mix manifest for each scene.
    """

    def __init__(self):
        self.ducker = DialogueSidechainDucker()
        self.spatializer = AcousticSpatializer()

    def build_scene_mix_manifest(
        self,
        scene: SceneBeat,
        arrangement: StemArrangement,
        foley_assets: List[FoleyAsset],
    ) -> Dict[str, Any]:
        """
        Creates a synchronized mixdown manifest ready for rendering or Web Audio API dispatch.
        """
        ducking_profile = self.ducker.calculate_ducking_profile(scene)
        spatial_profile = self.spatializer.infer_acoustic_space(scene.location)

        foley_cues_manifest = []
        for f in foley_assets:
            foley_cues_manifest.append({
                "cue_name": f.cue_name,
                "description": f.synthesized_from_text,
                "duration_seconds": f.duration_seconds,
                "uri": f.audio_uri,
            })

        return {
            "scene_number": scene.scene_number,
            "scene_title": scene.title,
            "tempo_bpm": arrangement.tempo_bpm,
            "tension_score": scene.tension_score,
            "emotional_valence": arrangement.emotional_valence,
            "stems_channel_count": len(arrangement.active_stems),
            "active_stems": arrangement.active_stems,
            "foley_cues": foley_cues_manifest,
            "ducking": ducking_profile,
            "spatial_acoustics": spatial_profile,
            "master_volume_db": -1.0,
            "target_lufs": -14.0,  # Standard broadcast / streaming loudness
        }
