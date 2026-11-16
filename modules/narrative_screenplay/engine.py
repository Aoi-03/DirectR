"""
Module 1: Narrative & Screenplay Engine
Implementation of character psychology constraints, dialect adaptation, and dynamic branching.
"""

from typing import List, Dict, Optional, Any
from core.schemas import (
    ProjectBrief,
    SceneBeat,
    DialogueLine,
    FoleyCue,
    CharacterProfile,
)
from core.event_bus import EventBus


class NarrativeScreenplayEngine:
    """
    Engine for generating structured screenplays with character psychology integrity,
    dialect-adaptive dialogue, and reactive lore backstories.
    """

    def __init__(self, event_bus: Optional[EventBus] = None):
        self.bus = event_bus

    def apply_dialect_rules(self, raw_dialogue: str, rules: Dict[str, str]) -> str:
        """
        Adapts raw dialogue to character dialect and speech pattern rules in real time.
        """
        adapted = raw_dialogue
        for term, replacement in rules.items():
            adapted = adapted.replace(term, replacement)
        return adapted

    def validate_psychology_constraints(
        self, character: CharacterProfile, proposed_actions: List[str]
    ) -> bool:
        """
        Validates that proposed scene actions do not violate character psychological constraints.
        """
        # Ensure non-negotiable psychological traits are respected
        for constraint in character.psychology_constraints:
            for action in proposed_actions:
                if f"violate_{constraint.lower()}" in action.lower():
                    return False
        return True

    def generate_reactive_npc_backstory(
        self, npc_name: str, relationship_to_protagonist: str, setting: str
    ) -> Dict[str, Any]:
        """
        Autonomous narrative sandbox generator for reactive NPC backstories.
        """
        return {
            "name": npc_name,
            "relationship": relationship_to_protagonist,
            "origin_setting": setting,
            "secret_motivation": f"Protect the ancient archives in {setting}",
            "allegiance_level": 0.85,
            "memory_tree_nodes": [
                f"Met protagonist during the rebellion at {setting}",
                "Possesses the cipher key for the lower districts",
            ],
        }

    def generate_screenplay(self, brief: ProjectBrief) -> List[SceneBeat]:
        """
        Generates structured scene beats for the given project brief,
        respecting character voice, tension progression, and sound cues.
        """
        scenes: List[SceneBeat] = []

        # Example 3-act tension arc: 0.3 -> 0.85 -> 0.6
        tension_curve = [0.3, 0.85, 0.55]
        scene_titles = [
            ("The Inciting Encounter", "District 9 Lower Alleyway", "NIGHT"),
            ("The Revelation & Confrontation", "Underground Cipher Vault", "NIGHT"),
            ("The Aftermath & Next Frontier", "Overlook Tower", "DAWN"),
        ]

        char_map = {c.name: c for c in brief.characters}

        for i, (title, loc, setting_time) in enumerate(scene_titles, start=1):
            tension = tension_curve[i - 1]

            dialogue_lines: List[DialogueLine] = []
            foley_cues: List[FoleyCue] = []

            # Populate dialogue with dialect rules if characters are present
            if brief.characters:
                speaker_char = brief.characters[(i - 1) % len(brief.characters)]
                raw_text = (
                    f"We cannot stay here much longer. The perimeter is breached."
                    if i == 1
                    else f"Look closely at the cipher data. It doesn't lie!"
                )
                adapted_text = self.apply_dialect_rules(
                    raw_text, speaker_char.dialect_rules
                )
                dialogue_lines.append(
                    DialogueLine(
                        speaker=speaker_char.name,
                        line=adapted_text,
                        emotion="Urgent" if tension > 0.5 else "Reflective",
                        dialect_applied=bool(speaker_char.dialect_rules),
                        delivery_note="Whispered with high tension",
                    )
                )

            # Populate action and foley cues based on tension
            if tension > 0.7:
                action = "Sparks fly from severed cables as security alarms blare in sync with the strobe lights."
                foley_cues.append(
                    FoleyCue(
                        cue_name="SparksSizzle",
                        description="Electrical spark fizzle and metal hit",
                        trigger_beat_second=12.4,
                    )
                )
                foley_cues.append(
                    FoleyCue(
                        cue_name="SirenWail",
                        description="Distant heavy industrial security siren",
                        trigger_beat_second=14.0,
                    )
                )
            else:
                action = "Rain trickles down the neon-lit corrugated steel roof as footsteps approach."
                foley_cues.append(
                    FoleyCue(
                        cue_name="RainOnRoof",
                        description="Soft persistent raindrops tapping on tin roofing",
                        trigger_beat_second=2.0,
                    )
                )

            scene = SceneBeat(
                scene_number=i,
                title=title,
                location=loc,
                setting_time=setting_time,
                action_description=action,
                visual_mood="Cyberpunk Noir" if "Lower" in loc else "Moody Cinematic",
                tension_score=tension,
                dialogue=dialogue_lines,
                foley_cues=foley_cues,
            )
            scenes.append(scene)

        if self.bus:
            self.bus.publish("narrative.scenes_generated", {"count": len(scenes)})

        return scenes
