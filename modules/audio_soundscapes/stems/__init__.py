"""
Stems sub-engine for dynamic tension-adaptive soundscapes.
"""

from .stem_definitions import StemCategory, StemLayer, TENSION_BANDS, STEM_CATALOG
from .arranger import DynamicStemArranger
from .generator import ProceduralWavSynthesizer

__all__ = [
    "StemCategory",
    "StemLayer",
    "TENSION_BANDS",
    "STEM_CATALOG",
    "DynamicStemArranger",
    "ProceduralWavSynthesizer",
]
