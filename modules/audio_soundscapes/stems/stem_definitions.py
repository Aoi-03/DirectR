"""
Definitions of musical stem layers and tension bands.
"""

from enum import Enum
from typing import Dict, List
from pydantic import BaseModel


class StemCategory(str, Enum):
    AMBIENT_PAD = "pad"
    BASS = "bass"
    PERCUSSION = "percussion"
    LEAD = "lead"
    TEXTURE = "texture"
    TRANSITION = "transition"


class StemLayer(BaseModel):
    name: str
    category: StemCategory
    description: str
    base_gain: float  # 0.0 to 1.0
    frequency_range_hz: tuple[int, int]
    midi_root_note: int = 48  # C3
    filter_cutoff_hz: int = 8000


STEM_CATALOG: Dict[str, StemLayer] = {
    # Low Tension Stems (Calm / Ambient)
    "ambient_pad": StemLayer(
        name="ambient_pad",
        category=StemCategory.AMBIENT_PAD,
        description="Lush analog synthesized pad with slow chorus and low pass filtering",
        base_gain=0.75,
        frequency_range_hz=(100, 2500),
        filter_cutoff_hz=1800,
    ),
    "sub_drone": StemLayer(
        name="sub_drone",
        category=StemCategory.BASS,
        description="Deep sine/sub-bass drone providing foundation warmth",
        base_gain=0.70,
        frequency_range_hz=(35, 95),
        midi_root_note=36,
    ),
    "soft_keys": StemLayer(
        name="soft_keys",
        category=StemCategory.LEAD,
        description="Felt piano and vintage electric rhodes playing minimal motifs",
        base_gain=0.65,
        frequency_range_hz=(200, 4500),
    ),
    # Mid Tension Stems (Suspense / Building)
    "rhythm_percussion": StemLayer(
        name="rhythm_percussion",
        category=StemCategory.PERCUSSION,
        description="Syncopated muted rimshots, shaker, and subtle organic pulse",
        base_gain=0.70,
        frequency_range_hz=(80, 8000),
    ),
    "electric_bass": StemLayer(
        name="electric_bass",
        category=StemCategory.BASS,
        description="Pulsing 8th-note acid bassline with resonant envelope filter",
        base_gain=0.80,
        frequency_range_hz=(45, 800),
    ),
    "cello_melody": StemLayer(
        name="cello_melody",
        category=StemCategory.LEAD,
        description="Haunting expressive cello playing minor/micro-tonal intervals",
        base_gain=0.75,
        frequency_range_hz=(90, 1500),
    ),
    # High Tension Stems (Action / Climax)
    "heavy_industrial_drums": StemLayer(
        name="heavy_industrial_drums",
        category=StemCategory.PERCUSSION,
        description="Aggressive compressed kick, layered metallic snare, and driving velocity",
        base_gain=0.90,
        frequency_range_hz=(30, 12000),
    ),
    "distorted_808": StemLayer(
        name="distorted_808",
        category=StemCategory.BASS,
        description="Overdriven saturation 808 sub with aggressive mid-range punch",
        base_gain=0.88,
        frequency_range_hz=(30, 450),
    ),
    "tension_riser": StemLayer(
        name="tension_riser",
        category=StemCategory.TRANSITION,
        description="Shepard tone riser with exponential pitch sweep and white noise build",
        base_gain=0.75,
        frequency_range_hz=(100, 15000),
    ),
    "screaming_lead_synth": StemLayer(
        name="screaming_lead_synth",
        category=StemCategory.LEAD,
        description="Detuned supersaw lead with biting distortion and ping-pong delay",
        base_gain=0.82,
        frequency_range_hz=(400, 10000),
    ),
    "rapid_hihats": StemLayer(
        name="rapid_hihats",
        category=StemCategory.PERCUSSION,
        description="Trap 16th and 32nd triplet rolls with velocity ramps",
        base_gain=0.65,
        frequency_range_hz=(3000, 16000),
    ),
}

TENSION_BANDS = [
    {
        "name": "Atmospheric Calm",
        "min_tension": 0.0,
        "max_tension": 0.35,
        "default_stems": ["ambient_pad", "sub_drone", "soft_keys"],
        "min_bpm": 65,
        "max_bpm": 85,
    },
    {
        "name": "Rising Suspense",
        "min_tension": 0.36,
        "max_tension": 0.70,
        "default_stems": ["ambient_pad", "rhythm_percussion", "electric_bass", "cello_melody"],
        "min_bpm": 86,
        "max_bpm": 115,
    },
    {
        "name": "High Conflict & Crisis",
        "min_tension": 0.71,
        "max_tension": 1.0,
        "default_stems": [
            "heavy_industrial_drums",
            "distorted_808",
            "tension_riser",
            "screaming_lead_synth",
            "rapid_hihats",
        ],
        "min_bpm": 116,
        "max_bpm": 150,
    },
]
