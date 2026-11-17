"""
Foley sound material and synthesis profiles.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel


class FoleyMaterialProfile(BaseModel):
    category: str
    material: str
    base_frequency_hz: float
    resonance_q: float
    attack_ms: float
    decay_ms: float
    noise_color: str  # "white", "pink", "brownian"
    reverb_decay_sec: float
    keywords: List[str]


FOLEY_MATERIAL_PROFILES: Dict[str, FoleyMaterialProfile] = {
    "metallic_impact": FoleyMaterialProfile(
        category="impact",
        material="metal",
        base_frequency_hz=1400.0,
        resonance_q=12.0,
        attack_ms=2.0,
        decay_ms=650.0,
        noise_color="white",
        reverb_decay_sec=1.8,
        keywords=["metal", "steel", "iron", "clang", "sword", "cable", "door"],
    ),
    "gravel_footstep": FoleyMaterialProfile(
        category="footstep",
        material="gravel",
        base_frequency_hz=420.0,
        resonance_q=2.5,
        attack_ms=8.0,
        decay_ms=180.0,
        noise_color="pink",
        reverb_decay_sec=0.4,
        keywords=["gravel", "dirt", "footstep", "crunch", "stride", "boot", "walk"],
    ),
    "electric_spark": FoleyMaterialProfile(
        category="electrical",
        material="plasma",
        base_frequency_hz=2800.0,
        resonance_q=8.0,
        attack_ms=1.0,
        decay_ms=120.0,
        noise_color="white",
        reverb_decay_sec=0.6,
        keywords=["spark", "zap", "electric", "fuse", "short_circuit", "wire", "sizzle"],
    ),
    "rain_weather": FoleyMaterialProfile(
        category="ambient_weather",
        material="water_surface",
        base_frequency_hz=800.0,
        resonance_q=1.2,
        attack_ms=50.0,
        decay_ms=2500.0,
        noise_color="pink",
        reverb_decay_sec=1.2,
        keywords=["rain", "storm", "droplet", "drizzle", "roof", "puddle", "water"],
    ),
    "cinematic_explosion": FoleyMaterialProfile(
        category="explosion",
        material="sub_shockwave",
        base_frequency_hz=60.0,
        resonance_q=4.0,
        attack_ms=5.0,
        decay_ms=3200.0,
        noise_color="brownian",
        reverb_decay_sec=3.5,
        keywords=["explosion", "blast", "bomb", "shockwave", "sub_drop", "boom", "shatter"],
    ),
}
