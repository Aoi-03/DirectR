"""
Unit Tests for Module 1: Narrative & Screenplay
================================================
Covers all three seed inspirations from the DirectR MODULE_SPECS:

  1. Character Psychology Constraints  — single-chapter and full 10-chapter arc
  2. Dialect & Voice Fidelity          — rule application, case-preservation,
                                         register detection, contraction engine
  3. Reactive NPC Backstory Sandbox    — single NPC, relationship web, lore caching

Also validates the full screenplay generation pipeline end-to-end.
"""

import unittest

from core.schemas import CharacterProfile, ProjectBrief
from modules.narrative_screenplay.engine import (
    BranchingConstraint,
    BranchingPathValidator,
    DialectEngine,
    LoreBible,
    NodeMemoryTree,
    NPCBackstorySandbox,
    NarrativeScreenplayEngine,
)


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

def _make_elena() -> CharacterProfile:
    return CharacterProfile(
        id="char_elena",
        name="Elena",
        archetype="Idealist Rebel",
        psychology_constraints=["Never Betray Allies", "Value Truth Above Safety"],
        dialect_rules={"cannot": "can't", "peril": "danger", "mate": "friend"},
        backstory="Former archivist turned rebel leader.",
    )


def _make_kael() -> CharacterProfile:
    return CharacterProfile(
        id="char_kael",
        name="Kael",
        archetype="Cipher Rogue",
        psychology_constraints=["Protective of crew members at all costs"],
        dialect_rules={"understand": "copy", "yes": "solid", "cannot": "can't"},
        backstory="Ex-military pilot navigating sunken corridors.",
    )


def _make_brief(*characters: CharacterProfile) -> ProjectBrief:
    return ProjectBrief(
        project_id="proj_test_001",
        title="Neon Shadows",
        genre="Cyberpunk Thriller",
        logline="A rogue cipher expert uncovers a subterranean conspiracy.",
        characters=list(characters),
    )


# ===========================================================================
# 1. LORE BIBLE (Context Caching)
# ===========================================================================

class TestLoreBible(unittest.TestCase):

    def test_register_character_adds_canon_fact(self):
        lore = LoreBible(project_id="proj_lore")
        char = _make_elena()
        lore.register_character(char)
        joined = " ".join(lore.canon_facts)
        self.assertIn("char_elena", joined)
        self.assertIn("Elena", joined)

    def test_register_character_idempotent(self):
        lore = LoreBible(project_id="proj_lore")
        char = _make_elena()
        lore.register_character(char)
        lore.register_character(char)   # second call must not duplicate
        self.assertEqual(1, len(lore.canon_facts))

    def test_link_characters_bidirectional(self):
        lore = LoreBible(project_id="proj_lore")
        lore.register_character(_make_elena())
        lore.register_character(_make_kael())
        lore.link_characters("char_elena", "char_kael", "Reluctant Allies")
        self.assertEqual("Reluctant Allies", lore.relationship_web["char_elena"]["char_kael"])
        self.assertEqual("Reluctant Allies", lore.relationship_web["char_kael"]["char_elena"])

    def test_chapter_state_round_trip(self):
        lore = LoreBible(project_id="proj_lore")
        lore.record_chapter_state(3, "char_elena", "mood", "determined")
        result = lore.get_chapter_state(3, "char_elena", "mood")
        self.assertEqual("determined", result)

    def test_missing_chapter_state_returns_none(self):
        lore = LoreBible(project_id="proj_lore")
        self.assertIsNone(lore.get_chapter_state(99, "char_x", "mood"))

    def test_summarise_includes_key_sections(self):
        lore = LoreBible(project_id="proj_lore")
        lore.register_character(_make_elena())
        summary = lore.summarise()
        self.assertIn("LORE BIBLE", summary)
        self.assertIn("Timeline", summary)
        self.assertIn("Relationships", summary)


# ===========================================================================
# 2. NODE MEMORY TREE (Vector Memory Trees)
# ===========================================================================

class TestNodeMemoryTree(unittest.TestCase):

    def test_store_and_retrieve_exact(self):
        tree = NodeMemoryTree()
        tree.store(["proj_001", "char_elena", "chapter_1"], {"tension": 0.3})
        result = tree.retrieve(["proj_001", "char_elena", "chapter_1"])
        self.assertIsNotNone(result)
        self.assertAlmostEqual(0.3, result["tension"])

    def test_retrieve_missing_path_returns_none(self):
        tree = NodeMemoryTree()
        self.assertIsNone(tree.retrieve(["nonexistent", "path"]))

    def test_store_updates_existing_node(self):
        tree = NodeMemoryTree()
        tree.store(["proj_001", "char_a"], {"mood": "calm"})
        tree.store(["proj_001", "char_a"], {"mood": "tense", "location": "vault"})
        result = tree.retrieve(["proj_001", "char_a"])
        self.assertEqual("tense", result["mood"])
        self.assertEqual("vault", result["location"])

    def test_retrieve_subtree_flattens_children(self):
        tree = NodeMemoryTree()
        tree.store(["proj_001", "char_a", "chapter_1"], {"tension": 0.3})
        tree.store(["proj_001", "char_a", "chapter_2"], {"tension": 0.85})
        flat = tree.retrieve_subtree(["proj_001", "char_a"])
        # Should have flattened keys from both child nodes
        self.assertTrue(any("tension" in k for k in flat))

    def test_independent_paths_do_not_interfere(self):
        tree = NodeMemoryTree()
        tree.store(["proj_001", "char_a"], {"role": "hero"})
        tree.store(["proj_001", "char_b"], {"role": "villain"})
        self.assertEqual("hero", tree.retrieve(["proj_001", "char_a"])["role"])
        self.assertEqual("villain", tree.retrieve(["proj_001", "char_b"])["role"])


# ===========================================================================
# 3. DIALECT ENGINE (Seed Inspiration 2)
# ===========================================================================

class TestDialectEngine(unittest.TestCase):

    def setUp(self):
        self.engine = DialectEngine()

    # --- Basic rule application ---

    def test_simple_substitution(self):
        rules = {"cannot": "can't", "peril": "danger", "mate": "friend"}
        result = self.engine.apply_dialect_rules(
            "We cannot ignore this peril, mate!", rules
        )
        self.assertIn("can't", result)
        self.assertIn("danger", result)
        self.assertIn("friend", result)

    def test_no_partial_word_replacement(self):
        """'can' inside 'scanner' must not be replaced."""
        rules = {"can": "cannot"}
        result = self.engine.apply_dialect_rules("Use the scanner carefully.", rules)
        self.assertNotIn("cannotner", result)

    def test_empty_rules_returns_unchanged(self):
        text = "Nothing changes here."
        self.assertEqual(text, self.engine.apply_dialect_rules(text, {}))

    def test_multiple_occurrences_replaced(self):
        rules = {"yes": "solid"}
        result = self.engine.apply_dialect_rules("Yes, yes, yes!", rules)
        self.assertEqual(3, result.lower().count("solid"))

    # --- Case preservation ---

    def test_uppercase_term_preserved(self):
        rules = {"danger": "glitch"}
        result = self.engine.apply_dialect_rules("DANGER ahead!", rules)
        self.assertIn("GLITCH", result)

    def test_titlecase_term_preserved(self):
        rules = {"danger": "glitch"}
        result = self.engine.apply_dialect_rules("Danger is imminent.", rules)
        self.assertIn("Glitch", result)

    def test_lowercase_term_preserved(self):
        rules = {"danger": "glitch"}
        result = self.engine.apply_dialect_rules("stay away from danger.", rules)
        self.assertIn("glitch", result)

    # --- Contractions ---

    def test_apply_contractions_cannot(self):
        result = self.engine.apply_contractions("We cannot proceed further.")
        self.assertIn("can't", result)

    def test_apply_contractions_do_not(self):
        result = self.engine.apply_contractions("Do not engage the target.")
        self.assertIn("don't", result)

    # --- Register detection ---

    def test_register_casual_contractions(self):
        text = "I can't believe you're here already, we're running late!"
        self.assertEqual("casual", self.engine.detect_register(text))

    def test_register_terse_short_sentences(self):
        text = "Move! Now! Go!"
        self.assertEqual("terse", self.engine.detect_register(text))

    def test_register_formal_indicator(self):
        text = "Therefore, pursuant to our agreement, henceforth all data transfers are suspended."
        self.assertEqual("formal", self.engine.detect_register(text))

    # --- Full dialect line generation ---

    def test_generate_dialect_line_returns_dialogue_line(self):
        from core.schemas import DialogueLine
        char = _make_elena()
        dl = self.engine.generate_dialect_line(
            raw_text="We cannot ignore this peril, mate!",
            character=char,
            emotion="Urgent",
        )
        self.assertIsInstance(dl, DialogueLine)
        self.assertEqual("Elena", dl.speaker)
        self.assertTrue(dl.dialect_applied)
        self.assertIn("can't", dl.line)

    def test_generate_dialect_line_no_rules_still_returns(self):
        from core.schemas import DialogueLine
        char = CharacterProfile(
            id="char_plain", name="Marcus", archetype="Narrator",
            psychology_constraints=[], dialect_rules={},
        )
        dl = self.engine.generate_dialect_line(
            raw_text="We cannot stay here.", character=char, emotion="Calm"
        )
        self.assertIsInstance(dl, DialogueLine)
        self.assertEqual("Marcus", dl.speaker)


# ===========================================================================
# 4. BRANCHING PATH VALIDATOR (Seed Inspiration 1)
# ===========================================================================

class TestBranchingPathValidator(unittest.TestCase):

    def _make_validator(self, char: CharacterProfile) -> BranchingPathValidator:
        lore = LoreBible(project_id="proj_v")
        lore.register_character(char)
        tree = NodeMemoryTree()
        validator = BranchingPathValidator(lore, tree)
        validator.register_character_constraints(char, chapter_range=(1, 10))
        return validator

    # --- Single-chapter validation ---

    def test_valid_actions_pass(self):
        char = _make_elena()
        v = self._make_validator(char)
        result = v.validate_branch(
            chapter=2,
            character=char,
            proposed_actions=["Seek the hidden transmitter", "Confront the commissioner"],
        )
        self.assertTrue(result["valid"])
        self.assertEqual(0, len(result["violations"]))

    def test_violation_prefix_detected(self):
        char = _make_elena()
        v = self._make_validator(char)
        result = v.validate_branch(
            chapter=3,
            character=char,
            proposed_actions=["violate_never betray allies for money"],
        )
        self.assertFalse(result["valid"])
        self.assertGreater(len(result["violations"]), 0)

    def test_out_of_chapter_range_not_flagged(self):
        """Constraint registered for chapters 1-5 must not fire at chapter 7."""
        char = _make_elena()
        lore = LoreBible(project_id="proj_v")
        lore.register_character(char)
        tree = NodeMemoryTree()
        v = BranchingPathValidator(lore, tree)
        v.register_character_constraints(char, chapter_range=(1, 5))
        result = v.validate_branch(
            chapter=7,
            character=char,
            proposed_actions=["betray_never betray allies"],
        )
        self.assertTrue(result["valid"])   # out of range → no constraint active

    # --- Full 10-chapter arc validation ---

    def test_full_arc_all_valid(self):
        char = _make_elena()
        v = self._make_validator(char)
        chapter_actions = {c: ["Scout the perimeter", "Gather intel"] for c in range(1, 11)}
        result = v.validate_full_arc(char, chapter_actions)
        self.assertTrue(result["valid"])
        self.assertEqual(10, len(result["chapters_checked"]))

    def test_full_arc_detects_mid_arc_violation(self):
        char = _make_elena()
        v = self._make_validator(char)
        chapter_actions = {c: ["Scout perimeter"] for c in range(1, 11)}
        chapter_actions[5] = ["violate_value truth above safety to save time"]
        result = v.validate_full_arc(char, chapter_actions)
        self.assertFalse(result["valid"])
        violation_chapters = [vio["chapter"] for vio in result["violations"]]
        self.assertIn(5, violation_chapters)

    def test_soft_constraint_generates_warning_not_violation(self):
        char = _make_elena()
        lore = LoreBible(project_id="proj_v")
        lore.register_character(char)
        tree = NodeMemoryTree()
        v = BranchingPathValidator(lore, tree)
        v.register_constraint(
            BranchingConstraint(
                chapter_range=(1, 10),
                character_id=char.id,
                constraint_text="Value Truth Above Safety",
                is_hard_constraint=False,
            )
        )
        result = v.validate_branch(
            chapter=2,
            character=char,
            proposed_actions=["betray_value truth above safety"],
        )
        # Soft constraint → valid=True (no hard violations) but warnings present
        self.assertTrue(result["valid"])
        self.assertGreater(len(result["warnings"]), 0)

    def test_memory_tree_caches_validation_result(self):
        char = _make_elena()
        lore = LoreBible(project_id="proj_v")
        lore.register_character(char)
        tree = NodeMemoryTree()
        v = BranchingPathValidator(lore, tree)
        v.register_character_constraints(char)
        v.validate_branch(chapter=4, character=char, proposed_actions=["Safe action"])
        cached = tree.retrieve(["proj_v", char.id, "chapter_4", "validation"])
        self.assertIsNotNone(cached)
        self.assertIn("valid", cached)


# ===========================================================================
# 5. NPC BACKSTORY SANDBOX (Seed Inspiration 3)
# ===========================================================================

class TestNPCBackstorySandbox(unittest.TestCase):

    def _make_sandbox(self, project_id: str = "proj_npc"):
        lore = LoreBible(project_id=project_id)
        tree = NodeMemoryTree()
        sandbox = NPCBackstorySandbox(lore, tree)
        return sandbox, lore, tree

    def test_generate_returns_required_keys(self):
        sandbox, _, _ = self._make_sandbox()
        npc = sandbox.generate(
            npc_name="Riven Mox",
            relationship_to_protagonist="Informant",
            setting="Sub-level Tunnels",
        )
        for key in ["name", "relationship", "origin_setting", "faction",
                    "secret_motivation", "allegiance_level", "memory_tree_nodes"]:
            self.assertIn(key, npc)

    def test_allegiance_within_range(self):
        sandbox, _, _ = self._make_sandbox()
        npc = sandbox.generate("Dara Vex", "Rival", "Upper Deck")
        self.assertGreaterEqual(npc["allegiance_level"], 0.0)
        self.assertLessEqual(npc["allegiance_level"], 1.0)

    def test_memory_nodes_non_empty(self):
        sandbox, _, _ = self._make_sandbox()
        npc = sandbox.generate("Jax Orin", "Ally", "The Sump Yards")
        self.assertGreater(len(npc["memory_tree_nodes"]), 0)

    def test_canon_fact_registered_in_lore(self):
        sandbox, lore, _ = self._make_sandbox()
        sandbox.generate("Kai Serra", "Contact", "Neon Quarter")
        joined = " ".join(lore.canon_facts)
        self.assertIn("kai_serra", joined)

    def test_protagonist_relationship_edge_registered(self):
        sandbox, lore, _ = self._make_sandbox()
        lore.register_character(_make_elena())
        sandbox.generate(
            npc_name="Shadow Broker",
            relationship_to_protagonist="Handler",
            setting="Black Market",
            protagonist_id="char_elena",
        )
        self.assertIn("shadow_broker", lore.relationship_web.get("char_elena", {}))

    def test_deterministic_output(self):
        """Same NPC name + setting should always produce same faction."""
        sandbox1, _, _ = self._make_sandbox("p1")
        sandbox2, _, _ = self._make_sandbox("p2")
        r1 = sandbox1.generate("Ghost", "Spy", "City Central")
        r2 = sandbox2.generate("Ghost", "Spy", "City Central")
        self.assertEqual(r1["faction"], r2["faction"])
        self.assertAlmostEqual(r1["allegiance_level"], r2["allegiance_level"])

    def test_memory_tree_stores_npc(self):
        sandbox, _, tree = self._make_sandbox("proj_npc")
        sandbox.generate("Zara Flux", "Mentor", "Archive Tower")
        cached = tree.retrieve(["proj_npc", "npcs", "zara_flux"])
        self.assertIsNotNone(cached)
        self.assertEqual("Zara Flux", cached.get("name"))

    def test_relationship_web_nxn(self):
        sandbox, _, _ = self._make_sandbox()
        npcs = ["Alpha", "Beta", "Gamma"]
        web = sandbox.generate_relationship_web(npcs, "Central Hub")
        for a in npcs:
            self.assertIn(a, web)
            for b in npcs:
                if a != b:
                    self.assertIn(b, web[a])
                    self.assertIsInstance(web[a][b], str)

    def test_no_self_relationship_in_web(self):
        sandbox, _, _ = self._make_sandbox()
        npcs = ["Alpha", "Beta", "Gamma"]
        web = sandbox.generate_relationship_web(npcs, "Central Hub")
        for a in npcs:
            self.assertNotIn(a, web[a])


# ===========================================================================
# 6. NARRATIVE SCREENPLAY ENGINE (Integration)
# ===========================================================================

class TestNarrativeScreenplayEngine(unittest.TestCase):

    def setUp(self):
        self.engine = NarrativeScreenplayEngine()

    # --- Dialect rule wrapper ---

    def test_apply_dialect_rules_basic(self):
        rules = {"cannot": "can't", "peril": "danger", "mate": "friend"}
        adapted = self.engine.apply_dialect_rules(
            "We cannot ignore this peril, mate!", rules
        )
        self.assertIn("can't", adapted)
        self.assertIn("danger", adapted)
        self.assertIn("friend", adapted)

    # --- Psychology constraint (backward-compatible API) ---

    def test_validate_psychology_constraints_valid(self):
        char = _make_elena()
        valid = self.engine.validate_psychology_constraints(
            char,
            ["Seek the hidden transmitter", "Confront the commissioner"],
        )
        self.assertTrue(valid)

    def test_validate_psychology_constraints_invalid(self):
        char = _make_elena()
        invalid = self.engine.validate_psychology_constraints(
            char,
            ["violate_never betray allies for money"],
        )
        self.assertFalse(invalid)

    # --- Full branching arc validation ---

    def test_validate_branching_arc_all_clean(self):
        char = _make_elena()
        chapter_actions = {c: ["Gather intelligence", "Secure perimeter"] for c in range(1, 11)}
        result = self.engine.validate_branching_arc(char, chapter_actions)
        self.assertTrue(result["valid"])
        self.assertEqual(10, len(result["chapters_checked"]))

    def test_validate_branching_arc_violation_detected(self):
        char = _make_kael()
        chapter_actions = {c: ["Protect crew"] for c in range(1, 11)}
        chapter_actions[7] = ["betray_protective of crew members at all costs"]
        result = self.engine.validate_branching_arc(char, chapter_actions)
        self.assertFalse(result["valid"])

    # --- Reactive NPC backstory ---

    def test_generate_reactive_npc_backstory_keys(self):
        npc = self.engine.generate_reactive_npc_backstory(
            npc_name="Dex Morrow",
            relationship_to_protagonist="Double Agent",
            setting="Archive District 7",
        )
        self.assertIn("faction", npc)
        self.assertIn("secret_motivation", npc)
        self.assertIn("memory_tree_nodes", npc)

    def test_generate_npc_relationship_web(self):
        web = self.engine.generate_npc_relationship_web(
            ["Vex", "Riven", "Dara"], "Central Nexus"
        )
        self.assertIn("Vex", web)
        self.assertIn("Riven", web["Vex"])

    # --- Full screenplay pipeline ---

    def test_screenplay_generation_scene_count(self):
        char = _make_kael()
        brief = _make_brief(char)
        scenes = self.engine.generate_screenplay(brief)
        self.assertEqual(3, len(scenes))

    def test_tension_arc_rises_then_falls(self):
        char = _make_kael()
        brief = _make_brief(char)
        scenes = self.engine.generate_screenplay(brief)
        self.assertLess(scenes[0].tension_score, scenes[1].tension_score)
        self.assertGreater(scenes[1].tension_score, scenes[2].tension_score)

    def test_high_tension_scene_has_multiple_foley_cues(self):
        char = _make_kael()
        brief = _make_brief(char)
        scenes = self.engine.generate_screenplay(brief)
        climax = scenes[1]
        self.assertGreater(climax.tension_score, 0.7)
        self.assertGreaterEqual(len(climax.foley_cues), 2)

    def test_dialect_applied_in_dialogue(self):
        char = _make_kael()
        brief = _make_brief(char)
        scenes = self.engine.generate_screenplay(brief)
        first_line = scenes[0].dialogue[0].line
        self.assertIn("can't", first_line)

    def test_dialogue_speaker_matches_character(self):
        char = _make_elena()
        brief = _make_brief(char)
        scenes = self.engine.generate_screenplay(brief)
        self.assertEqual("Elena", scenes[0].dialogue[0].speaker)

    def test_multiple_characters_alternate_speakers(self):
        brief = _make_brief(_make_elena(), _make_kael())
        scenes = self.engine.generate_screenplay(brief)
        speakers = [s.dialogue[0].speaker for s in scenes if s.dialogue]
        # With 2 characters, speaker rotates: Elena → Kael → Elena
        self.assertEqual("Elena", speakers[0])
        self.assertEqual("Kael", speakers[1])
        self.assertEqual("Elena", speakers[2])

    def test_lore_bible_populated_after_generation(self):
        brief = _make_brief(_make_elena(), _make_kael())
        self.engine.generate_screenplay(brief)
        self.assertIsNotNone(self.engine.lore)
        self.assertGreater(len(self.engine.lore.canon_facts), 0)

    def test_memory_tree_stores_chapter_states(self):
        char = _make_elena()
        brief = _make_brief(char)
        self.engine.generate_screenplay(brief)
        node = self.engine.memory_tree.retrieve(
            ["proj_test_001", "char_elena", "chapter_1"]
        )
        self.assertIsNotNone(node)
        self.assertIn("tension", node)

    def test_scene_beats_are_valid_pydantic_models(self):
        from core.schemas import SceneBeat
        brief = _make_brief(_make_elena())
        scenes = self.engine.generate_screenplay(brief)
        for scene in scenes:
            self.assertIsInstance(scene, SceneBeat)
            self.assertGreaterEqual(scene.tension_score, 0.0)
            self.assertLessEqual(scene.tension_score, 1.0)

    def test_no_characters_generates_scenes_without_dialogue(self):
        brief = ProjectBrief(
            project_id="proj_empty",
            title="Silent World",
            genre="Ambient",
            logline="A world without voices.",
            characters=[],
        )
        scenes = self.engine.generate_screenplay(brief)
        self.assertEqual(3, len(scenes))
        for scene in scenes:
            self.assertEqual(0, len(scene.dialogue))

    def test_event_bus_receives_scenes_generated_event(self):
        from core.event_bus import EventBus
        received: list = []
        bus = EventBus()
        bus.subscribe("narrative.scenes_generated", received.append)

        engine = NarrativeScreenplayEngine(event_bus=bus)
        brief = _make_brief(_make_elena())
        engine.generate_screenplay(brief)

        self.assertEqual(1, len(received))
        self.assertEqual(3, received[0]["count"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
