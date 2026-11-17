"""
Module 2: Palette Generator
Procedural color harmony and mood-driven palette engine.
"""

from typing import Dict, Optional
from ..schemas import ColorPalette


class PaletteGenerator:
    """
    Generates harmonious color palettes adapted to scene visual mood,
    dramatic tension, and time of day.
    """

    PRESET_PALETTES: Dict[str, ColorPalette] = {
        "cyberpunk_noir": ColorPalette(
            palette_name="Cyberpunk Noir",
            mood="Cyberpunk Noir",
            background="#0a0a14",
            primary="#121829",
            secondary="#00f3ff",
            accent="#ff0055",
            highlight="#ffe600",
            shadow="#050508",
            glow="rgba(0, 243, 255, 0.6)",
        ),
        "moody_cinematic": ColorPalette(
            palette_name="Moody Cinematic",
            mood="Moody Cinematic",
            background="#0d1117",
            primary="#161b22",
            secondary="#58a6ff",
            accent="#f78166",
            highlight="#f0f6fc",
            shadow="#010409",
            glow="rgba(88, 166, 255, 0.4)",
        ),
        "dawn_overlook": ColorPalette(
            palette_name="Golden Dawn Horizon",
            mood="Dawn / Golden Hour",
            background="#1a1423",
            primary="#3d2645",
            secondary="#832161",
            accent="#da4167",
            highlight="#f4d35e",
            shadow="#0c0714",
            glow="rgba(244, 211, 94, 0.5)",
        ),
        "neon_crisis": ColorPalette(
            palette_name="High-Tension Neon Alert",
            mood="Crisis / High Tension",
            background="#190204",
            primary="#3a0509",
            secondary="#ff1e42",
            accent="#ff8500",
            highlight="#ffffff",
            shadow="#080001",
            glow="rgba(255, 30, 66, 0.85)",
        ),
        "deep_space": ColorPalette(
            palette_name="Deep Space Void",
            mood="Cosmic / Sci-Fi",
            background="#030712",
            primary="#111827",
            secondary="#6366f1",
            accent="#a855f7",
            highlight="#38bdf8",
            shadow="#000000",
            glow="rgba(99, 102, 241, 0.5)",
        ),
    }

    @classmethod
    def get_palette_for_scene(
        cls,
        visual_mood: str,
        setting_time: str = "DAY",
        tension_score: float = 0.5,
    ) -> ColorPalette:
        """
        Determines the optimal color palette for a scene based on mood, time, and tension.
        """
        mood_lower = visual_mood.lower()
        time_lower = setting_time.lower()

        # High tension override (> 0.75 triggers emergency neon / stark contrast)
        if tension_score >= 0.75:
            return cls.PRESET_PALETTES["neon_crisis"]

        if "cyberpunk" in mood_lower or "neon" in mood_lower:
            return cls.PRESET_PALETTES["cyberpunk_noir"]
        elif "dawn" in time_lower or "morning" in time_lower or "golden" in mood_lower:
            return cls.PRESET_PALETTES["dawn_overlook"]
        elif "space" in mood_lower or "void" in mood_lower or "cosmic" in mood_lower:
            return cls.PRESET_PALETTES["deep_space"]
        else:
            return cls.PRESET_PALETTES["moody_cinematic"]
