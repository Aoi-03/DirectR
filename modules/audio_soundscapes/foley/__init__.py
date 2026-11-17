"""
Foley sub-engine for zero-shot cinematic sound effect synthesis.
"""

from .sound_library import FOLEY_MATERIAL_PROFILES, FoleyMaterialProfile
from .synthesizer import ZeroShotFoleySynthesizer

__all__ = [
    "FOLEY_MATERIAL_PROFILES",
    "FoleyMaterialProfile",
    "ZeroShotFoleySynthesizer",
]
