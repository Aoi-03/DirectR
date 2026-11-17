"""
DirectR Local API Server
Serves Narrative (Module 1) and Audio Studio (Module 3) processes to the Web Frontend.
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
from modules.audio_soundscapes.engine import AudioStudioEngine

narrative_engine = NarrativeScreenplayEngine()
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
                "service": "DirectR Narrative & Audio Engine API",
                "modules": ["narrative_screenplay", "audio_soundscapes"],
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
            # Generate screenplay & dialogue
            brief_data = body.get("brief", {})
            brief = ProjectBrief(
                project_id=brief_data.get("project_id", "web_project_001"),
                title=brief_data.get("title", "Chronicles of Neo-Aethel"),
                genre=brief_data.get("genre", "Cyberpunk Sci-Fi Fantasy"),
                logline=brief_data.get("logline", "In a submerged neon metropolis, a lone archivist and a rogue pilot uncover a sentient AI code."),
                characters=[
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
            )
            scenes = narrative_engine.generate_screenplay(brief)
            scenes_dicts = [s.model_dump() for s in scenes]
            self._send_json(200, {
                "scenes": scenes_dicts,
                "lore_facts": narrative_engine.lore.canon_facts if narrative_engine.lore else [],
            })

        elif self.path == "/api/narrative/npc":
            # Generate reactive NPC backstory with Nemotron / Procedural
            name = body.get("name", "Iona 'Switch' Marrow")
            relationship = body.get("relationship", "Reluctant Informant / Memory Broker")
            setting = body.get("setting", "District 9 Lower Slums")
            use_llm = body.get("use_llm", True)

            npc = narrative_engine.generate_reactive_npc_backstory(
                npc_name=name,
                relationship_to_protagonist=relationship,
                setting=setting,
                protagonist_id="char_lyra",
                use_llm=use_llm,
            )
            self._send_json(200, {"npc": npc})

        elif self.path == "/api/audio/arrange":
            # Process tension to stems & arrange soundscapes
            tension = float(body.get("tension", 0.72))
            stems = audio_engine.map_tension_to_stems(tension)
            bpm = audio_engine.stem_arranger.calculate_scene_bpm(tension)

            # Microtonal harmony calculation
            harmony = audio_engine.compute_microtonal_harmony(440.0)

            # Foley cues synthesis
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
            # End-to-end run combining Module 1 & Module 3
            tension = float(body.get("tension", 0.72))
            brief = ProjectBrief(
                project_id="studio_run_001",
                title="Chronicles of Neo-Aethel",
                genre="Cyberpunk Sci-Fi Fantasy",
                logline="In a submerged neon metropolis, a lone archivist and a rogue pilot uncover a sentient AI code.",
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
            scenes = narrative_engine.generate_screenplay(brief)
            stems = audio_engine.arrange_soundscapes(scenes)
            foley = audio_engine.synthesize_foley_cues(scenes)
            npc = narrative_engine.generate_reactive_npc_backstory(
                npc_name="Iona 'Switch' Marrow",
                relationship_to_protagonist="Underground Signal Broker",
                setting="District 09 Slums",
                protagonist_id="char_lyra",
            )

            self._send_json(200, {
                "success": True,
                "narrative": {
                    "scenes": [s.model_dump() for s in scenes],
                    "npc": npc,
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
