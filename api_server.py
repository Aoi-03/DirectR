"""
DirectR Local API Server
Serves Narrative (Module 1), Visual Art (Module 2), and Audio Studio (Module 3)
processes to the Web Frontend.
Built with Python's standard library (http.server + json) - zero extra dependencies required!
"""

import sys
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any

# Ensure root workspace is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, ".env"))

from core.schemas import ProjectBrief, CharacterProfile
from modules.narrative_screenplay.engine import NarrativeScreenplayEngine
from modules.visual_art_design.engine import VisualArtEngine
from modules.audio_soundscapes.engine import AudioStudioEngine

narrative_engine = NarrativeScreenplayEngine()
visual_engine = VisualArtEngine()
audio_engine = AudioStudioEngine()

PORT = int(os.getenv("DIRECTR_API_PORT", 8000))


class DirectRAPIHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def _send_json(self, status: int, data: Dict[str, Any]):
        response_bytes = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self._set_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_GET(self):
        if self.path == "/api/status" or self.path == "/":
            self._send_json(200, {
                "status": "online",
                "service": "DirectR Full Studio API",
                "modules": ["narrative_screenplay", "visual_art_design", "audio_soundscapes"],
                "nvidia_nemotron_available": narrative_engine.nemotron.is_available,
            })
        else:
            self._send_json(404, {"error": "Endpoint not found"})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            body = json.loads(post_data.decode("utf-8")) if post_data else {}
        except json.JSONDecodeError:
            body = {}

        if self.path == "/api/narrative/generate":
            # Module 1: Screenplay Generation from User Input Prompt / Brief
            title = body.get("title", "Chronicles of Neo-Aethel")
            genre = body.get("genre", "Cyberpunk Sci-Fi Fantasy")
            logline = body.get("logline", "In a submerged neon metropolis, a lone archivist and a rogue pilot uncover a sentient AI code.")
            characters_input = body.get("characters", [])

            char_objs = []
            if characters_input:
                for c in characters_input:
                    char_objs.append(CharacterProfile(
                        id=c.get("id", f"char_{len(char_objs)}"),
                        name=c.get("name", "Operative"),
                        archetype=c.get("archetype", "Rebel"),
                        psychology_constraints=c.get("psychology_constraints", ["Preserve core integrity"]),
                        dialect_rules=c.get("dialect_rules", {"cannot": "can't"}),
                        backstory=c.get("backstory", ""),
                    ))
            else:
                char_objs = [
                    CharacterProfile(
                        id="char_lyra",
                        name="Lyra Vance",
                        archetype="Sub-surface Archivist",
                        psychology_constraints=["Never destroy historical records", "Distrust central governance authorities"],
                        dialect_rules={"cannot": "can't", "danger": "glitch", "friend": "anchor"},
                        backstory="Former data curator who survived the Great Pulse flood."
                    ),
                    CharacterProfile(
                        id="char_kael",
                        name="Kaelen Cross",
                        archetype="Hovercraft Rogue",
                        psychology_constraints=["Protective of crew members at all costs"],
                        dialect_rules={"understand": "copy", "yes": "solid"},
                        backstory="Ex-military escort pilot navigating the sunken lower levels."
                    )
                ]

            brief = ProjectBrief(
                project_id=body.get("project_id", "project_live_001"),
                title=title,
                genre=genre,
                logline=logline,
                characters=char_objs,
            )

            scenes = narrative_engine.generate_screenplay(brief)
            scenes_dicts = [s.model_dump() for s in scenes]
            self._send_json(200, {
                "brief": brief.model_dump(),
                "scenes": scenes_dicts,
                "lore_facts": narrative_engine.lore.canon_facts if narrative_engine.lore else [],
            })

        elif self.path == "/api/narrative/npc":
            # Module 1: Reactive NPC Backstory Sandbox (Nemotron AI / Procedural)
            name = body.get("name", "Iona 'Switch' Marrow")
            relationship = body.get("relationship", "Reluctant Informant / Memory Broker")
            setting = body.get("setting", "District 9 Lower Slums")
            protagonist_id = body.get("protagonist_id", "char_lyra")
            use_llm = body.get("use_llm", True)

            npc = narrative_engine.generate_reactive_npc_backstory(
                npc_name=name,
                relationship_to_protagonist=relationship,
                setting=setting,
                protagonist_id=protagonist_id,
                use_llm=use_llm,
            )
            self._send_json(200, {"npc": npc})

        elif self.path == "/api/visual/generate":
            # Module 2: Visual Art & Design Assist (Layered SVGs, Character Turnarounds, Storyboards)
            prompt = body.get("prompt", "Neon cityscape with rain and cybernetic architecture")
            scene_number = int(body.get("scene_number", 1))
            char_name = body.get("character_name", "Lyra Vance")
            char_archetype = body.get("character_archetype", "Sub-surface Archivist")
            layers = body.get("layers", ["background_plate", "midground_structures", "foreground_characters", "lighting_overlays"])

            svg_result = visual_engine.generate_layered_svg(
                prompt=prompt,
                scene_number=scene_number,
                layers=layers,
            )

            char_profile = CharacterProfile(
                id="char_active",
                name=char_name,
                archetype=char_archetype,
                psychology_constraints=[],
                dialect_rules={},
            )
            turnaround = visual_engine.generate_character_turnaround(char_profile)

            self._send_json(200, {
                "svg_markup": svg_result["svg_markup"],
                "anchor_nodes_count": svg_result["anchor_nodes_count"],
                "layer_names": svg_result["layer_names"],
                "turnaround": turnaround.model_dump(),
            })

        elif self.path == "/api/audio/arrange":
            # Module 3: Audio Studio Stems, BPM, and Foley synthesis
            tension = float(body.get("tension", 0.72))
            stems = audio_engine.map_tension_to_stems(tension)
            bpm = audio_engine.stem_arranger.calculate_scene_bpm(tension)
            harmony = audio_engine.compute_microtonal_harmony(440.0)

            foley_cues = [
                {"cue_name": "ElectricSparks", "description": "High tension electrical discharge", "trigger_beat_second": 2.5},
                {"cue_name": "RainOnRoof", "description": "Persistent rain on metal roof", "trigger_beat_second": 0.5},
                {"cue_name": "VaultHum", "description": "Resonant sub-bass drone from ancient vault", "trigger_beat_second": 1.0},
            ]

            self._send_json(200, {
                "tension": tension,
                "bpm": bpm,
                "active_stems": stems,
                "harmony_frequencies": harmony[:5],
                "foley_cues": foley_cues,
            })

        elif self.path == "/api/studio/run":
            # End-to-end swarm execution across all modules based on user brief
            prompt = body.get("prompt", "In a submerged neon metropolis, a lone archivist and a rogue pilot uncover a sentient AI code.")
            title = body.get("title", "Chronicles of Neo-Aethel")
            genre = body.get("genre", "Cyberpunk Sci-Fi Fantasy")
            tension = float(body.get("tension", 0.72))

            brief = ProjectBrief(
                project_id="studio_exec_live",
                title=title,
                genre=genre,
                logline=prompt,
                characters=[
                    CharacterProfile(
                        id="char_lyra",
                        name="Lyra Vance",
                        archetype="Sub-surface Archivist",
                        psychology_constraints=["Never destroy historical records"],
                        dialect_rules={"cannot": "can't", "danger": "glitch"}
                    ),
                    CharacterProfile(
                        id="char_kael",
                        name="Kaelen Cross",
                        archetype="Hovercraft Rogue",
                        psychology_constraints=["Protective of crew members"],
                        dialect_rules={"understand": "copy", "yes": "solid"}
                    )
                ]
            )

            # Module 1
            scenes = narrative_engine.generate_screenplay(brief)
            npc = narrative_engine.generate_reactive_npc_backstory(
                npc_name="Iona 'Switch' Marrow",
                relationship_to_protagonist="Underground Signal Broker",
                setting="District 09 Slums",
                protagonist_id="char_lyra",
            )

            # Module 2
            visual_assets = visual_engine.produce_visual_package(brief, scenes)

            # Module 3
            stems = audio_engine.arrange_soundscapes(scenes)
            foley = audio_engine.synthesize_foley_cues(scenes)

            self._send_json(200, {
                "success": True,
                "brief": brief.model_dump(),
                "narrative": {
                    "scenes": [s.model_dump() for s in scenes],
                    "npc": npc,
                },
                "visual": {
                    "assets": [v.model_dump() for v in visual_assets],
                },
                "audio": {
                    "stems": [s.model_dump() for s in stems],
                    "foley": [f.model_dump() for f in foley],
                    "master_bpm": audio_engine.stem_arranger.calculate_scene_bpm(tension),
                }
            })

        else:
            self._send_json(404, {"error": f"Unknown endpoint: {self.path}"})


def run():
    server_address = ("127.0.0.1", PORT)
    httpd = HTTPServer(server_address, DirectRAPIHandler)
    print(f"🎬 DirectR Backend API Server running at http://127.0.0.1:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping DirectR API Server...")
        httpd.server_close()


if __name__ == "__main__":
    run()
