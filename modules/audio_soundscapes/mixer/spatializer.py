"""
Acoustic Room Spatializer
Matches scene physical environments to reverb impulse response and spatial parameters.
"""

from typing import Dict, Any


class AcousticSpatializer:
    """
    Computes environmental acoustic reverb and spatial parameters
    from narrative setting and location descriptions.
    """

    ROOM_PRESETS = {
        "cathedral_vast": {
            "room_size": 0.95,
            "decay_time_sec": 4.5,
            "damping_hz": 2500,
            "wet_gain": 0.45,
            "dry_gain": 0.65,
            "stereo_width": 1.0,
        },
        "underground_vault": {
            "room_size": 0.75,
            "decay_time_sec": 2.8,
            "damping_hz": 1800,
            "wet_gain": 0.35,
            "dry_gain": 0.70,
            "stereo_width": 0.85,
        },
        "narrow_corridor": {
            "room_size": 0.40,
            "decay_time_sec": 1.1,
            "damping_hz": 4000,
            "wet_gain": 0.25,
            "dry_gain": 0.80,
            "stereo_width": 0.50,
        },
        "outdoor_open": {
            "room_size": 0.20,
            "decay_time_sec": 0.4,
            "damping_hz": 6000,
            "wet_gain": 0.10,
            "dry_gain": 0.90,
            "stereo_width": 0.90,
        },
    }

    def infer_acoustic_space(self, location_text: str) -> Dict[str, Any]:
        """
        Maps setting keywords to acoustic room parameters.
        """
        loc = location_text.lower()
        if "vault" in loc or "subterranean" in loc or "underground" in loc or "tunnel" in loc:
            preset = "underground_vault"
        elif "cathedral" in loc or "temple" in loc or "hall" in loc or "chasm" in loc:
            preset = "cathedral_vast"
        elif "corridor" in loc or "alley" in loc or "room" in loc or "chamber" in loc:
            preset = "narrow_corridor"
        else:
            preset = "outdoor_open"

        params = dict(self.ROOM_PRESETS[preset])
        params["inferred_preset"] = preset
        params["location_source"] = location_text
        return params
