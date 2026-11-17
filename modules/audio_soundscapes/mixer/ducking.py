"""
Dialogue Sidechain Ducking Engine
Ensures speech clarity by dynamically attenuating musical stem levels during dialogue delivery.
"""

from typing import List, Dict, Any, Optional
from core.schemas import SceneBeat, DialogueLine


class DialogueSidechainDucker:
    """
    Calculates sidechain attenuation envelopes so background music
    smoothly ducks under dialogue without pumping artifacts.
    """

    def __init__(
        self,
        attenuation_db: float = -12.0,
        attack_ms: float = 60.0,
        release_ms: float = 350.0,
        hold_ms: float = 150.0,
    ):
        self.attenuation_db = attenuation_db
        self.attack_ms = attack_ms
        self.release_ms = release_ms
        self.hold_ms = hold_ms

    def calculate_ducking_profile(self, scene: SceneBeat) -> Dict[str, Any]:
        """
        Calculates sidechain ducking curve for a scene based on dialogue lines.
        """
        has_dialogue = len(scene.dialogue) > 0
        dialogue_events = []

        current_time = 2.0  # Initial offset in scene

        for idx, line in enumerate(scene.dialogue):
            # Estimate spoken duration based on word count (~3 words per second)
            words = len(line.line.split())
            spoken_duration_sec = max(1.8, round(words / 3.0, 2))

            start_t = round(current_time, 2)
            end_t = round(start_t + spoken_duration_sec, 2)

            dialogue_events.append({
                "speaker": line.speaker,
                "text": line.line,
                "start_sec": start_t,
                "end_sec": end_t,
                "attenuation_db": self.attenuation_db,
                "attack_sec": self.attack_ms / 1000.0,
                "release_sec": self.release_ms / 1000.0,
            })

            current_time = end_t + 1.5  # Gap between dialogue lines

        return {
            "scene_number": scene.scene_number,
            "sidechain_active": has_dialogue,
            "nominal_gain_db": 0.0,
            "ducked_gain_db": self.attenuation_db,
            "dialogue_events": dialogue_events,
            "total_dialogue_lines": len(scene.dialogue),
        }
