"""
Module 1: Narrative & Screenplay Engine
========================================
Implements three seed inspirations from the DirectR spec:

  1. Character Psychology Constraints  — validate & enforce non-negotiable
     psychological traits across a 10-chapter nonlinear branching tree.
  2. Dialect & Voice Fidelity          — real-time dialect rule application
     with per-character speech-pattern registers, contractions, and regional
     vocabulary substitutions.
  3. Reactive NPC Backstory Sandbox    — autonomous generator that builds
     interconnected NPC backstories and relationship webs anchored to the
     world-state produced so far.

Tech stack used (pure-Python, no external LLM calls needed to pass tests):
  - Structured Outputs  : Pydantic models from core.schemas
  - Context Caching     : LoreBible dataclass keeps world-state in memory
  - Vector Memory Trees : NodeMemoryTree (prefix-tree) for character recall
  - Long-Context aware  : all public APIs accept full ProjectBrief payloads
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from core.schemas import (
    CharacterProfile,
    DialogueLine,
    FoleyCue,
    ProjectBrief,
    SceneBeat,
)
from core.event_bus import EventBus

logger = logging.getLogger("DirectR.NarrativeEngine")


# ---------------------------------------------------------------------------
# NVIDIA Nemotron LLM Client
# ---------------------------------------------------------------------------

class NemotronNarrativeClient:
    """
    Client for NVIDIA's Nemotron-3-Ultra-550B (or compatible models) via NVIDIA NIM.
    Used for intelligent dialect-adaptive dialogue and reactive NPC backstory generation.
    Gracefully falls back when API key is unset or network calls fail.
    """

    DEFAULT_MODEL = "nvidia/nemotron-3-ultra-550b-a55b"
    API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY")
        self.model = model or self.DEFAULT_MODEL

    @property
    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key.startswith("nvapi-"))

    def generate(
        self,
        prompt: str,
        system_prompt: str = "You are an elite narrative screenplay writer and world builder.",
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> Optional[str]:
        """
        Invoke Nemotron chat completion. Returns None on network error, missing key, or timeout.
        Extracts message content (preferring 'content', with fallback to 'reasoning_content').
        """
        if not self.is_available:
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "DirectR/1.0",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            req = urllib.request.Request(
                self.API_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                choice = data["choices"][0]["message"]
                content = choice.get("content")
                if not content:
                    content = choice.get("reasoning_content")
                return content.strip() if content else None
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, KeyError, IndexError) as err:
            logger.warning("[NemotronClient] API call failed: %s. Using procedural fallback.", err)
            return None


# ---------------------------------------------------------------------------
# Context Caching: LoreBible
# ---------------------------------------------------------------------------

@dataclass
class LoreBible:
    """
    Persistent in-memory world context cache (simulates LLM context caching).
    Stores canonical facts, timeline events, and relationship edges so that
    iterative screenplay calls never contradict previously established lore.
    """
    project_id: str
    canon_facts: List[str] = field(default_factory=list)
    timeline: List[str] = field(default_factory=list)
    # {character_id: {other_character_id: relationship_description}}
    relationship_web: Dict[str, Dict[str, str]] = field(default_factory=dict)
    chapter_states: Dict[int, Dict[str, Any]] = field(default_factory=dict)

    def register_character(self, char: CharacterProfile) -> None:
        """Cache a character's core identity into lore."""
        entry = (
            f"[CHAR:{char.id}] {char.name} ({char.archetype}) — "
            f"constraints: {', '.join(char.psychology_constraints)}"
        )
        if entry not in self.canon_facts:
            self.canon_facts.append(entry)
        if char.id not in self.relationship_web:
            self.relationship_web[char.id] = {}

    def add_canon_fact(self, fact: str) -> None:
        if fact not in self.canon_facts:
            self.canon_facts.append(fact)

    def link_characters(
        self, char_a_id: str, char_b_id: str, relationship: str
    ) -> None:
        self.relationship_web.setdefault(char_a_id, {})[char_b_id] = relationship
        self.relationship_web.setdefault(char_b_id, {})[char_a_id] = relationship

    def record_chapter_state(
        self, chapter: int, character_id: str, state_key: str, value: Any
    ) -> None:
        ch = self.chapter_states.setdefault(chapter, {})
        ch[f"{character_id}::{state_key}"] = value

    def get_chapter_state(
        self, chapter: int, character_id: str, state_key: str
    ) -> Optional[Any]:
        return self.chapter_states.get(chapter, {}).get(f"{character_id}::{state_key}")

    def summarise(self) -> str:
        """Return a compact world-bible string for context injection."""
        lines = ["=== LORE BIBLE ==="]
        lines += self.canon_facts
        lines.append("--- Timeline ---")
        lines += self.timeline
        lines.append("--- Relationships ---")
        for a_id, edges in self.relationship_web.items():
            for b_id, rel in edges.items():
                lines.append(f"  {a_id} <-> {b_id}: {rel}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Vector Memory Tree: NodeMemoryTree
# ---------------------------------------------------------------------------

@dataclass
class MemoryNode:
    """A single node in the hierarchical memory tree."""
    key: str
    data: Dict[str, Any] = field(default_factory=dict)
    children: Dict[str, "MemoryNode"] = field(default_factory=dict)

    def upsert_child(self, key: str, data: Dict[str, Any]) -> "MemoryNode":
        if key not in self.children:
            self.children[key] = MemoryNode(key=key, data=data)
        else:
            self.children[key].data.update(data)
        return self.children[key]


class NodeMemoryTree:
    """
    Hierarchical prefix-tree memory for characters, backstory nodes, and
    story beats.  Retrieval walks the path PROJECT → CHARACTER → BEAT.

    Example path: ["proj_001", "char_lyra", "chapter_3"]
    """

    def __init__(self) -> None:
        self._root: MemoryNode = MemoryNode(key="ROOT")

    def _traverse(self, path: List[str], create: bool = False) -> Optional[MemoryNode]:
        node = self._root
        for segment in path:
            if segment not in node.children:
                if not create:
                    return None
                node.children[segment] = MemoryNode(key=segment)
            node = node.children[segment]
        return node

    def store(self, path: List[str], data: Dict[str, Any]) -> None:
        """Store data at the given path, creating nodes as needed."""
        node = self._traverse(path, create=True)
        assert node is not None
        node.data.update(data)

    def retrieve(self, path: List[str]) -> Optional[Dict[str, Any]]:
        """Retrieve data at exact path, or None if not found."""
        node = self._traverse(path, create=False)
        return dict(node.data) if node else None

    def retrieve_subtree(self, path: List[str]) -> Dict[str, Any]:
        """Return all data under the given path, flattened with dotted keys."""
        node = self._traverse(path, create=False)
        if not node:
            return {}
        result: Dict[str, Any] = {}
        self._flatten(node, prefix="", out=result)
        return result

    def _flatten(self, node: MemoryNode, prefix: str, out: Dict[str, Any]) -> None:
        p = f"{prefix}.{node.key}" if prefix else node.key
        out.update({f"{p}.{k}": v for k, v in node.data.items()})
        for child in node.children.values():
            self._flatten(child, p, out)


# ---------------------------------------------------------------------------
# BranchingPath: Nonlinear 10-chapter constraint manager
# ---------------------------------------------------------------------------

@dataclass
class BranchingConstraint:
    """
    Represents a single constraint that must be respected across all
    branching paths leading from a chapter fork.
    """
    chapter_range: Tuple[int, int]      # (start_chapter, end_chapter) inclusive
    character_id: str
    constraint_text: str
    is_hard_constraint: bool = True     # hard = rejection; soft = warning only


class BranchingPathValidator:
    """
    Validates proposed scene actions against character psychology constraints
    across a 10-chapter nonlinear branching structure.

    A branch is accepted only when ALL hard constraints for every character
    active in that chapter are satisfied.
    """

    # Violation signal tokens: if any action contains one of these combined
    # with a constraint keyword, the action is flagged.
    _VIOLATION_PREFIXES = (
        "violate_", "betray_", "break_", "ignore_", "abandon_",
        "destroy_", "murder_", "attack_ally", "defect_",
    )

    def __init__(
        self,
        lore_bible: LoreBible,
        memory_tree: NodeMemoryTree,
        total_chapters: int = 10,
    ) -> None:
        self.lore = lore_bible
        self.tree = memory_tree
        self.total_chapters = total_chapters
        self._constraints: List[BranchingConstraint] = []

    def register_constraint(self, constraint: BranchingConstraint) -> None:
        self._constraints.append(constraint)

    def register_character_constraints(
        self, char: CharacterProfile, chapter_range: Tuple[int, int] = (1, 10)
    ) -> None:
        for c_text in char.psychology_constraints:
            self._constraints.append(
                BranchingConstraint(
                    chapter_range=chapter_range,
                    character_id=char.id,
                    constraint_text=c_text,
                    is_hard_constraint=True,
                )
            )

    def validate_branch(
        self,
        chapter: int,
        character: CharacterProfile,
        proposed_actions: List[str],
    ) -> Dict[str, Any]:
        """
        Validates a list of proposed actions for `character` at `chapter`.

        Returns:
            {
              "valid": bool,
              "violations": [{"constraint": str, "action": str}],
              "warnings": [{"constraint": str, "action": str}],
            }
        """
        violations: List[Dict[str, str]] = []
        warnings: List[Dict[str, str]] = []

        active = [
            bc
            for bc in self._constraints
            if bc.character_id == character.id
            and bc.chapter_range[0] <= chapter <= bc.chapter_range[1]
        ]

        for bc in active:
            keyword = bc.constraint_text.lower().replace(" ", "_")
            for action in proposed_actions:
                action_lower = action.lower().replace(" ", "_")
                flagged = any(
                    action_lower.startswith(pfx) or f"{pfx}{keyword}" in action_lower
                    for pfx in self._VIOLATION_PREFIXES
                )
                if flagged:
                    record = {
                        "constraint": bc.constraint_text,
                        "action": action,
                        "chapter": chapter,
                    }
                    if bc.is_hard_constraint:
                        violations.append(record)
                    else:
                        warnings.append(record)

        # Cache result into memory tree
        self.tree.store(
            [self.lore.project_id, character.id, f"chapter_{chapter}", "validation"],
            {
                "valid": len(violations) == 0,
                "violation_count": len(violations),
                "warning_count": len(warnings),
            },
        )

        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
        }

    def validate_full_arc(
        self,
        character: CharacterProfile,
        chapter_actions: Dict[int, List[str]],
    ) -> Dict[str, Any]:
        """
        Runs validation across all chapters in `chapter_actions` for a single
        character, simulating multi-chapter branching path consistency.
        """
        all_violations: List[Dict[str, str]] = []
        all_warnings: List[Dict[str, str]] = []

        for chapter, actions in sorted(chapter_actions.items()):
            result = self.validate_branch(chapter, character, actions)
            all_violations.extend(result["violations"])
            all_warnings.extend(result["warnings"])

        is_arc_valid = len(all_violations) == 0
        logger.info(
            "[BranchValidator] Character '%s' arc valid=%s "
            "(%d violations, %d warnings across %d chapters)",
            character.name,
            is_arc_valid,
            len(all_violations),
            len(all_warnings),
            len(chapter_actions),
        )
        return {
            "valid": is_arc_valid,
            "violations": all_violations,
            "warnings": all_warnings,
            "chapters_checked": sorted(chapter_actions.keys()),
        }


# ---------------------------------------------------------------------------
# Dialect Engine
# ---------------------------------------------------------------------------

class DialectEngine:
    """
    Real-time dialect adaptation engine.

    Features:
      - Token-level replacement via character `dialect_rules` dictionary.
      - Whole-word matching (regex word-boundary) to avoid partial collisions.
      - Case-preserving substitution (preserves Title / UPPER / lower casing).
      - Register detection: identifies spoken register (formal / casual / regional).
    """

    # Common contraction expansions used for formality normalisation
    _CONTRACTIONS: Dict[str, str] = {
        "cannot": "can't",
        "will not": "won't",
        "do not": "don't",
        "is not": "isn't",
        "are not": "aren't",
        "have not": "haven't",
        "has not": "hasn't",
        "would not": "wouldn't",
        "should not": "shouldn't",
        "could not": "couldn't",
        "I am": "I'm",
        "you are": "you're",
        "we are": "we're",
        "they are": "they're",
    }

    def _preserve_case(self, original: str, replacement: str) -> str:
        """Return replacement with the same casing style as original."""
        if original.isupper():
            return replacement.upper()
        if original.istitle():
            return replacement.capitalize()
        return replacement

    def _word_boundary_replace(self, text: str, term: str, replacement: str) -> str:
        """Replace `term` in `text` with case-preservation, whole-word only."""
        pattern = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)

        def _replacer(m: re.Match) -> str:
            return self._preserve_case(m.group(0), replacement)

        return pattern.sub(_replacer, text)

    def apply_dialect_rules(self, raw_dialogue: str, rules: Dict[str, str]) -> str:
        """
        Adapts `raw_dialogue` to character speech patterns defined in `rules`.
        Rules are applied in insertion order; longer/more-specific rules should
        be listed first in the character profile for correct priority.
        """
        adapted = raw_dialogue
        for term, replacement in rules.items():
            adapted = self._word_boundary_replace(adapted, term, replacement)
        return adapted

    def apply_contractions(self, text: str) -> str:
        """Apply standard English contractions for casual spoken register."""
        result = text
        for formal, contracted in self._CONTRACTIONS.items():
            result = self._word_boundary_replace(result, formal, contracted)
        return result

    def detect_register(self, text: str) -> str:
        """
        Heuristic register detector.
        Returns one of: 'formal', 'casual', 'regional', 'terse'.
        """
        words = text.lower().split()
        word_count = len(words)
        contraction_count = sum(1 for w in words if "'" in w)
        sentence_count = max(1, len(re.findall(r"[.!?]", text)))
        avg_sent_len = word_count / sentence_count

        if contraction_count / max(1, word_count) > 0.15:
            return "casual"
        if avg_sent_len < 6:
            return "terse"
        if any(indicator in text.lower() for indicator in ["therefore", "henceforth", "pursuant", "aforementioned"]):
            return "formal"
        return "regional"

    def generate_dialect_line(
        self,
        raw_text: str,
        character: CharacterProfile,
        emotion: str = "Neutral",
        apply_contractions: bool = True,
    ) -> DialogueLine:
        """
        Full pipeline: apply contractions → dialect rules → package as DialogueLine.
        """
        text = raw_text
        if apply_contractions and not character.dialect_rules:
            text = self.apply_contractions(text)

        adapted = self.apply_dialect_rules(text, character.dialect_rules)
        dialect_applied = adapted != raw_text

        register = self.detect_register(adapted)
        delivery_note = {
            "formal": "Measured, deliberate delivery",
            "casual": "Relaxed, spontaneous cadence",
            "regional": "Accent-coloured with regional inflection",
            "terse": "Clipped, high-tension delivery",
        }.get(register, "Neutral delivery")

        return DialogueLine(
            speaker=character.name,
            line=adapted,
            emotion=emotion,
            dialect_applied=dialect_applied,
            delivery_note=delivery_note,
        )


# ---------------------------------------------------------------------------
# NPC Backstory Sandbox
# ---------------------------------------------------------------------------

class NPCBackstorySandbox:
    """
    Autonomous reactive NPC backstory generator.

    Given a protagonist context and world state from the LoreBible, it
    synthesises a rich, internally-consistent NPC record with:
      - Origin story anchored to world locations
      - Secret motivation derived from faction conflicts
      - Memory tree nodes (prior interactions with protagonist)
      - Allegiance score (0.0 hostile → 1.0 fully loyal)
      - Relationship web edges registered to the LoreBible
    """

    _FACTION_SEEDS = [
        "Cipher Collective",
        "Neon Sovereignty Council",
        "The Underdock Resistance",
        "Archive Protectorate",
        "Synthetic Accord",
    ]

    _MOTIVATION_TEMPLATES = [
        "Avenge the destruction of {setting} by any means necessary.",
        "Recover the lost cipher archives buried beneath {setting}.",
        "Protect the last uninfected data nodes hidden in {setting}.",
        "Establish a neutral safe-passage zone through {setting}.",
        "Expose the council's falsified history of the events at {setting}.",
    ]

    def __init__(self, lore: LoreBible, memory_tree: NodeMemoryTree) -> None:
        self.lore = lore
        self.tree = memory_tree

    def _deterministic_index(self, seed: str, length: int) -> int:
        """Stable hash-based index to keep results reproducible per seed."""
        h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
        return h % length

    def generate(
        self,
        npc_name: str,
        relationship_to_protagonist: str,
        setting: str,
        protagonist_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Build a fully reactive NPC backstory.

        Args:
            npc_name:                   NPC's display name.
            relationship_to_protagonist: e.g. "Reluctant Informant".
            setting:                    World location that anchors the story.
            protagonist_id:             Optional character ID of the protagonist
                                        to register a relationship edge.

        Returns:
            Rich NPC dict suitable for downstream modules.
        """
        # Deterministic but varied selection based on NPC name
        fi = self._deterministic_index(npc_name + "_faction", len(self._FACTION_SEEDS))
        mi = self._deterministic_index(npc_name + "_motive", len(self._MOTIVATION_TEMPLATES))

        faction = self._FACTION_SEEDS[fi]
        motivation = self._MOTIVATION_TEMPLATES[mi].format(setting=setting)

        allegiance = round(
            0.5 + (self._deterministic_index(npc_name + "_allegiance", 50) / 100),
            2,
        )
        allegiance = min(1.0, max(0.0, allegiance))

        memory_nodes = [
            f"First encountered protagonist during the siege of {setting}.",
            f"Provided covert intelligence on {faction} supply routes.",
            f"Was nearly captured at the outer perimeter of {setting}.",
            f"Secretly carries the decryption shard for the {faction} vaults.",
        ]

        backstory: Dict[str, Any] = {
            "name": npc_name,
            "relationship": relationship_to_protagonist,
            "origin_setting": setting,
            "faction": faction,
            "secret_motivation": motivation,
            "allegiance_level": allegiance,
            "memory_tree_nodes": memory_nodes,
            "personality_traits": [
                "Calculating under pressure",
                "Fiercely protective of their origin community",
                "Prone to cryptic warnings",
            ],
        }

        # Cache into memory tree
        npc_id = npc_name.lower().replace(" ", "_")
        self.tree.store(
            [self.lore.project_id, "npcs", npc_id],
            {k: v for k, v in backstory.items() if isinstance(v, (str, float, int))},
        )

        # Register canon facts and relationship edge into LoreBible
        self.lore.add_canon_fact(
            f"[NPC:{npc_id}] {npc_name} — {faction} member, allegiance={allegiance}"
        )
        if protagonist_id:
            self.lore.link_characters(protagonist_id, npc_id, relationship_to_protagonist)

        logger.info(
            "[NPCBackstory] Generated backstory for '%s' (faction=%s, allegiance=%.2f)",
            npc_name,
            faction,
            allegiance,
        )
        return backstory

    def generate_relationship_web(
        self, npc_names: List[str], setting: str
    ) -> Dict[str, Dict[str, str]]:
        """
        Auto-generate a full NxN relationship web for a list of NPCs,
        creating realistic rivalry, alliance, and neutrality edges.
        """
        web: Dict[str, Dict[str, str]] = {}
        relation_types = ["Allies", "Rivals", "Uneasy Truce", "Unknowing Pawns", "Former Comrades"]

        for i, a in enumerate(npc_names):
            web[a] = {}
            for j, b in enumerate(npc_names):
                if a == b:
                    continue
                seed = a + b + setting
                ri = self._deterministic_index(seed, len(relation_types))
                web[a][b] = relation_types[ri]

        return web


# ---------------------------------------------------------------------------
# Main Engine: NarrativeScreenplayEngine
# ---------------------------------------------------------------------------

class NarrativeScreenplayEngine:
    """
    Primary entry point for Module 1: Storytelling & Co-Writers.

    Orchestrates the three seed inspirations:
      1. Psychology constraint validation across branching paths.
      2. Dialect-adaptive dialogue generation.
      3. Reactive NPC backstory sandbox.

    All public methods accept core.schemas types and return structured
    Pydantic output objects, keeping the inter-module contract intact.
    """

    # 3-act tension arc used for screenplay generation
    _DEFAULT_TENSION_CURVE: List[float] = [0.3, 0.85, 0.55]

    _DEFAULT_SCENES: List[Tuple[str, str, str]] = [
        ("The Inciting Encounter",         "District 9 Lower Alleyway",   "NIGHT"),
        ("The Revelation & Confrontation",  "Underground Cipher Vault",    "NIGHT"),
        ("The Aftermath & Next Frontier",   "Overlook Tower",              "DAWN"),
    ]

    _FOLEY_HIGH_TENSION: List[Tuple[str, str, float]] = [
        ("SparksSizzle",  "Electrical spark fizzle and metal impact",     12.4),
        ("SirenWail",     "Distant heavy industrial security siren",       14.0),
        ("HeartbeatPulse","Low sub-bass heartbeat throb rising in tempo",  16.5),
    ]

    _FOLEY_LOW_TENSION: List[Tuple[str, str, float]] = [
        ("RainOnRoof",    "Soft persistent raindrops tapping on tin roofing", 2.0),
        ("NeonHum",       "Faint electrical hum from flickering neon sign",   5.5),
    ]

    def __init__(self, event_bus: Optional[EventBus] = None, nvidia_api_key: Optional[str] = None) -> None:
        self.bus = event_bus
        self.lore: Optional[LoreBible] = None
        self.memory_tree = NodeMemoryTree()
        self._dialect_engine = DialectEngine()
        self._validator: Optional[BranchingPathValidator] = None
        self._npc_sandbox: Optional[NPCBackstorySandbox] = None
        self.nemotron = NemotronNarrativeClient(api_key=nvidia_api_key)

    # ------------------------------------------------------------------
    # Public API — Seed Inspiration 2: Dialect Adaptation
    # ------------------------------------------------------------------

    def apply_dialect_rules(self, raw_dialogue: str, rules: Dict[str, str]) -> str:
        """
        Adapts raw dialogue to character dialect and speech pattern rules
        in real-time.  Delegates to DialectEngine for case-aware whole-word
        replacement.
        """
        return self._dialect_engine.apply_dialect_rules(raw_dialogue, rules)

    # ------------------------------------------------------------------
    # Public API — Seed Inspiration 1: Psychology Constraint Validation
    # ------------------------------------------------------------------

    def validate_psychology_constraints(
        self,
        character: CharacterProfile,
        proposed_actions: List[str],
        chapter: int = 1,
    ) -> bool:
        """
        Returns True when all proposed actions respect the character's
        psychology constraints at the given chapter.

        Backward-compatible with the original single-bool signature.
        """
        if self._validator is None:
            lore = self._ensure_lore(character)
            self._validator = BranchingPathValidator(lore, self.memory_tree)
            self._validator.register_character_constraints(character)

        result = self._validator.validate_branch(chapter, character, proposed_actions)
        return result["valid"]

    def validate_branching_arc(
        self,
        character: CharacterProfile,
        chapter_actions: Dict[int, List[str]],
    ) -> Dict[str, Any]:
        """
        Validates a full 10-chapter branching arc for a character.

        Args:
            character:       The CharacterProfile to validate.
            chapter_actions: Mapping of chapter number → list of proposed actions.

        Returns:
            Validation report dict with 'valid', 'violations', 'warnings'.
        """
        lore = self._ensure_lore(character)
        validator = BranchingPathValidator(lore, self.memory_tree)
        validator.register_character_constraints(character)
        return validator.validate_full_arc(character, chapter_actions)

    # ------------------------------------------------------------------
    # Public API — Seed Inspiration 3: Reactive NPC Backstory
    # ------------------------------------------------------------------

    def generate_reactive_npc_backstory(
        self,
        npc_name: str,
        relationship_to_protagonist: str,
        setting: str,
        protagonist_id: Optional[str] = None,
        use_llm: bool = True,
    ) -> Dict[str, Any]:
        """
        Autonomous narrative sandbox generator for reactive NPC backstories
        with interconnected relationship webs.
        """
        if self._npc_sandbox is None:
            lore = self.lore or LoreBible(project_id="default")
            self._npc_sandbox = NPCBackstorySandbox(lore, self.memory_tree)
        
        # Base procedural template
        backstory = self._npc_sandbox.generate(
            npc_name, relationship_to_protagonist, setting, protagonist_id
        )

        # Enhance with Nemotron-3-Ultra-550B if enabled and reachable
        if use_llm and self.nemotron.is_available:
            prompt = (
                f"NPC Name: {npc_name}\n"
                f"Relationship to Protagonist: {relationship_to_protagonist}\n"
                f"Setting: {setting}\n"
                f"Faction: {backstory.get('faction')}\n"
                f"Create a high-tension secret motivation and a visceral backstory memory.\n"
                f"Output strictly a JSON object with keys 'motivation' and 'memory_node'."
            )
            llm_res = self.nemotron.generate(
                prompt=prompt,
                system_prompt="You are an elite narrative engine. Output strictly a JSON object with keys 'motivation' and 'memory_node'. No introductory or concluding text.",
                temperature=0.7,
                max_tokens=600,
            )
            if llm_res:
                try:
                    clean = llm_res.strip()
                    if "```json" in clean:
                        clean = clean.split("```json")[-1].split("```")[0].strip()
                    elif "```" in clean:
                        clean = clean.split("```")[-1].split("```")[0].strip()
                    # Find outer curly braces
                    start = clean.find("{")
                    end = clean.rfind("}")
                    if start != -1 and end != -1:
                        clean = clean[start : end + 1]
                    parsed = json.loads(clean)
                    if "motivation" in parsed and parsed["motivation"]:
                        backstory["secret_motivation"] = parsed["motivation"]
                    if "memory_node" in parsed and parsed["memory_node"]:
                        backstory["memory_tree_nodes"].insert(0, f"[Nemotron AI] {parsed['memory_node']}")
                except Exception as err:
                    logger.debug("[NPCBackstory] Could not parse LLM JSON: %s", err)

        return backstory

    def generate_npc_relationship_web(
        self, npc_names: List[str], setting: str
    ) -> Dict[str, Dict[str, str]]:
        """Generate an NxN relationship map for a group of NPCs."""
        if self._npc_sandbox is None:
            lore = self.lore or LoreBible(project_id="default")
            self._npc_sandbox = NPCBackstorySandbox(lore, self.memory_tree)
        return self._npc_sandbox.generate_relationship_web(npc_names, setting)

    # ------------------------------------------------------------------
    # Public API — Full Screenplay Generation
    # ------------------------------------------------------------------

    def generate_screenplay(self, brief: ProjectBrief) -> List[SceneBeat]:
        """
        Generates structured scene beats for the given project brief,
        respecting character voice, tension progression, and sound cues.

        Pipeline:
          1. Initialise LoreBible and BranchingPathValidator for the brief.
          2. Register all characters into the lore cache and memory tree.
          3. Generate reactive NPC backstories for the world.
          4. Iterate over a 3-act scene structure producing:
               - Dialect-adapted DialogueLine per scene.
               - Tension-matched FoleyCue list.
               - Validated character actions (hard-constraint gate).
          5. Publish event to EventBus.
        """
        # 1. Initialise lore context
        self.lore = LoreBible(project_id=brief.project_id)
        self._npc_sandbox = NPCBackstorySandbox(self.lore, self.memory_tree)

        # 2. Register characters
        for char in brief.characters:
            self.lore.register_character(char)
            self.memory_tree.store(
                [brief.project_id, char.id, "profile"],
                {
                    "name": char.name,
                    "archetype": char.archetype,
                    "constraints": char.psychology_constraints,
                },
            )

        # Set up cross-character relationships in lore
        chars = brief.characters
        for i in range(len(chars)):
            for j in range(i + 1, len(chars)):
                self.lore.link_characters(
                    chars[i].id, chars[j].id, "Co-protagonists with shared mission"
                )

        # 3. Auto-generate world NPCs
        if brief.characters:
            self.generate_reactive_npc_backstory(
                npc_name="Riven Mox",
                relationship_to_protagonist="Black-market intelligence broker",
                setting="Sub-level 7 Maintenance Tunnels",
                protagonist_id=brief.characters[0].id,
            )

        # 4. Scene generation
        self._validator = BranchingPathValidator(self.lore, self.memory_tree)
        for char in brief.characters:
            self._validator.register_character_constraints(char, chapter_range=(1, 10))

        scenes: List[SceneBeat] = []

        for i, (title, loc, setting_time) in enumerate(self._DEFAULT_SCENES, start=1):
            tension = self._DEFAULT_TENSION_CURVE[i - 1]

            # --- Dialogue ---
            dialogue_lines: List[DialogueLine] = []
            if brief.characters:
                speaker = brief.characters[(i - 1) % len(brief.characters)]

                raw_texts = {
                    1: "We cannot stay here much longer. The perimeter is breached.",
                    2: "Look closely at the cipher data. It does not lie!",
                    3: "We made it. I cannot believe we are still standing.",
                }
                raw = raw_texts.get(i, f"Chapter {i} dialogue placeholder.")

                emotion = "Urgent" if tension > 0.5 else "Reflective"
                dl = self._dialect_engine.generate_dialect_line(
                    raw_text=raw,
                    character=speaker,
                    emotion=emotion,
                    apply_contractions=True,
                )
                dialogue_lines.append(dl)

                # Store chapter state
                self.lore.record_chapter_state(i, speaker.id, "emotion", emotion)
                self.lore.record_chapter_state(i, speaker.id, "location", loc)
                self.memory_tree.store(
                    [brief.project_id, speaker.id, f"chapter_{i}"],
                    {"tension": tension, "location": loc, "emotion": emotion},
                )

            # --- Action (with constraint validation) ---
            proposed_actions = self._build_scene_actions(i, tension, loc)
            if brief.characters:
                primary_char = brief.characters[0]
                validation = self._validator.validate_branch(
                    chapter=i,
                    character=primary_char,
                    proposed_actions=proposed_actions,
                )
                if not validation["valid"]:
                    logger.warning(
                        "[NarrativeEngine] Constraint violation in scene %d: %s",
                        i,
                        validation["violations"],
                    )
                    # Substitute safe fallback action
                    proposed_actions = [
                        f"Character reconsiders, retreating to maintain integrity. ({loc})"
                    ]

            action = proposed_actions[0]

            # --- Foley cues ---
            foley_cues = self._build_foley_cues(tension)

            # --- Assemble SceneBeat ---
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

        # 5. Publish event
        if self.bus:
            self.bus.publish(
                "narrative.scenes_generated",
                {
                    "count": len(scenes),
                    "project_id": brief.project_id,
                    "lore_facts": len(self.lore.canon_facts),
                },
            )

        logger.info(
            "[NarrativeEngine] Screenplay generated: %d scenes, %d lore facts cached.",
            len(scenes),
            len(self.lore.canon_facts),
        )
        return scenes

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_lore(self, character: CharacterProfile) -> LoreBible:
        if self.lore is None:
            self.lore = LoreBible(project_id="standalone")
        self.lore.register_character(character)
        return self.lore

    def _build_scene_actions(
        self, scene_num: int, tension: float, location: str
    ) -> List[str]:
        """Return a list of scene actions matched to tension level."""
        if tension > 0.7:
            return [
                "Sparks fly from severed cables as security alarms blare in sync "
                "with the strobe lights.",
                "Emergency blast doors seal the corridor, trapping the squad inside.",
            ]
        elif tension > 0.4:
            return [
                "The team moves cautiously through dimly-lit infrastructure, "
                "tracking the signal pulse.",
            ]
        else:
            return [
                "Rain trickles down the neon-lit corrugated steel roof as "
                "footsteps approach slowly.",
            ]

    def _build_foley_cues(self, tension: float) -> List[FoleyCue]:
        """Return tension-appropriate foley cues."""
        if tension > 0.7:
            return [
                FoleyCue(cue_name=n, description=d, trigger_beat_second=t)
                for n, d, t in self._FOLEY_HIGH_TENSION
            ]
        return [
            FoleyCue(cue_name=n, description=d, trigger_beat_second=t)
            for n, d, t in self._FOLEY_LOW_TENSION
        ]
