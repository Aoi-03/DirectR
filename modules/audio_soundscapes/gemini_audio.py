"""
Gemini AI Audio & Soundscape Engine
Uses Google Gemini API to generate dynamic soundscape composition prompts,
zero-shot Foley sound design specs, and microtonal harmonic structures.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger("DirectR.GeminiAudio")

# Load environment variables from .env file in project root
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env")


class GeminiAudioEngine:
    """
    Intelligent Audio & Soundscape generation client powered by Google Gemini.
    """

    SUPPORTED_MODELS = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
    ]

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "").strip()
        self._client = None
        self._active_model = None

    def is_configured(self) -> bool:
        """Checks if a valid, non-empty Gemini API key is configured."""
        if not self.api_key:
            # Re-check env in case .env was recently saved
            load_dotenv(ROOT_DIR / ".env", override=True)
            self.api_key = os.getenv("GEMINI_API_KEY", "").strip()

        return bool(self.api_key and not self.api_key.startswith("your_"))

    def _get_client(self):
        """Initializes google.genai Client if installed and key is available."""
        if not self.is_configured():
            raise ValueError(
                "Gemini API Key not found. Please set GEMINI_API_KEY in your .env file."
            )

        if self._client is None:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize google.genai Client ({e}), will use REST fallback.")
                self._client = "REST_FALLBACK"

        return self._client

    def _call_gemini_raw(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """
        Executes a prompt against Gemini using google.genai SDK or REST API fallback.
        """
        client = self._get_client()

        # Method 1: Official google.genai SDK
        if client != "REST_FALLBACK":
            for model_name in self.SUPPORTED_MODELS:
                try:
                    config = {}
                    if system_instruction:
                        config["system_instruction"] = system_instruction

                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=config if config else None,
                    )
                    if response and response.text:
                        self._active_model = model_name
                        return response.text
                except Exception as e:
                    logger.debug(f"Model {model_name} failed: {e}. Trying next...")

        # Method 2: Direct REST fallback via requests
        import requests
        headers = {"Content-Type": "application/json"}
        for model_name in self.SUPPORTED_MODELS:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
            payload: Dict[str, Any] = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            if system_instruction:
                payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

            try:
                res = requests.post(url, headers=headers, json=payload, timeout=25)
                if res.status_code == 200:
                    data = res.json()
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    self._active_model = model_name
                    return text
            except Exception as ex:
                logger.debug(f"REST call to {model_name} failed: {ex}")

        raise RuntimeError(
            "Failed to generate content from Gemini API across all supported models. Please check your API key and network connection."
        )

    # -------------------------------------------------------------------------
    # 1. AI Cinematic Score & Stems Prompt Generator
    # -------------------------------------------------------------------------
    def generate_soundscape_composition(
        self,
        scene_title: str,
        tension_score: float,
        visual_mood: str,
        location: str,
        action_description: str,
    ) -> Dict[str, Any]:
        """
        Uses Gemini to generate high-fidelity dynamic stem arrangement instructions,
        Lyria/MusicLM generation prompts, and acoustic timbre specifications.
        """
        system_prompt = (
            "You are an elite Hollywood AI Film Composer and Music Director for DirectR. "
            "You translate screenplay dramatic beats and visual pacing into precise musical stem instructions "
            "and generative music prompts for Lyria/MusicLM. Output valid JSON only."
        )

        user_prompt = f"""
Analyze this cinematic scene and produce a complete musical stem arrangement:

SCENE CONTEXT:
- Title: {scene_title}
- Location: {location}
- Dramatic Tension: {tension_score:.2f} / 1.00
- Visual Mood: {visual_mood}
- Action: {action_description}

Return JSON with exact keys:
{{
    "scene_title": "{scene_title}",
    "tension_score": {tension_score:.2f},
    "tempo_bpm": (integer between 65 and 150),
    "time_signature": "4/4" or other,
    "key_signature": "e.g. D Minor or microtonal Dorian",
    "emotional_valence": "short description of psychological impact",
    "lyria_musiclm_prompt": "A detailed 2-3 sentence generative prompt for Lyria/MusicLM to render the full track",
    "active_stem_layers": [
        {{
            "name": "e.g. heavy_industrial_drums",
            "category": "percussion/bass/pad/lead/transition",
            "timbre_description": "sonic characteristics",
            "recommended_volume_db": -6.0
        }}
    ],
    "sound_design_notes": "direction for the mixing engineer"
}}
"""
        raw_text = self._call_gemini_raw(user_prompt, system_instruction=system_prompt)
        return self._clean_and_parse_json(raw_text)

    # -------------------------------------------------------------------------
    # 2. AI Zero-Shot Cinematic Foley Sound Designer
    # -------------------------------------------------------------------------
    def design_zero_shot_foley(
        self,
        cue_name: str,
        cue_description: str,
        scene_location: str,
    ) -> Dict[str, Any]:
        """
        Uses Gemini to architect precise zero-shot Foley sound design specs
        and procedural synthesis parameters for text action cues.
        """
        system_prompt = (
            "You are a master Foley Sound Designer for cinematic films. "
            "Translate action and sound cues into detailed acoustic synthesis specs and physical material models. "
            "Output valid JSON only."
        )

        user_prompt = f"""
Design a zero-shot cinematic Foley sound effect for:

FOLEY CUE:
- Name: {cue_name}
- Description: {cue_description}
- Acoustic Environment: {scene_location}

Return JSON with exact keys:
{{
    "cue_name": "{cue_name}",
    "detected_material": "e.g. weathered metal, plasma, wet gravel, concrete",
    "kinetic_energy": "e.g. explosive impact, subtle scrape, rapid pulse",
    "fundamental_freq_hz": 440.0,
    "filter_resonance_q": 4.5,
    "envelope": {{
        "attack_ms": 5.0,
        "decay_ms": 400.0,
        "sustain_level": 0.2,
        "release_ms": 1200.0
    }},
    "reverb_profile": {{
        "space_type": "e.g. underground vault, cathedral",
        "decay_seconds": 2.5,
        "wet_dry_ratio": 0.35
    }},
    "sound_designer_recipe": "How to achieve this sound acoustically or procedurally in Web Audio / synthesizers"
}}
"""
        raw_text = self._call_gemini_raw(user_prompt, system_instruction=system_prompt)
        return self._clean_and_parse_json(raw_text)

    # -------------------------------------------------------------------------
    # 3. AI Microtonal Harmony & Voicing Designer
    # -------------------------------------------------------------------------
    def design_microtonal_harmony(
        self,
        scene_mood: str,
        character_psychology: str,
        root_note_hz: float = 220.0,
    ) -> Dict[str, Any]:
        """
        Uses Gemini to generate 24-EDO quarter-tone harmonic voicings and psychological dissonance curves.
        """
        system_prompt = (
            "You are an avant-garde film composer specializing in microtonal acoustics (24-EDO, Just Intonation, Xenharmonics). "
            "Map character psychological states to quarter-tone intervals and cents deviations. Output valid JSON only."
        )

        user_prompt = f"""
Design a 24-EDO micro-tonal chord voicing for:
- Scene Mood: {scene_mood}
- Character Psychology: {character_psychology}
- Root Frequency: {root_note_hz} Hz (A3)

Return JSON with exact keys:
{{
    "voicing_name": "e.g. Sub-quartertone Uncanny Cluster",
    "psychological_intent": "why this chord creates unease/wonder/tension",
    "intervals_cents": [0, 150, 350, 700],
    "computed_frequencies_hz": [220.0, 239.7, 269.2, 330.0],
    "quartertone_names": ["Root (A)", "Quarter-tone Sharp 2nd", "Neutral 3rd", "Perfect 5th"],
    "synthesizer_timbre_suggestion": "e.g. warm analog saw with slow chorus and gentle tape saturation"
}}
"""
        raw_text = self._call_gemini_raw(user_prompt, system_instruction=system_prompt)
        return self._clean_and_parse_json(raw_text)

    # -------------------------------------------------------------------------
    # Helper: Clean JSON responses from LLM (removing markdown ```json ... ```)
    # -------------------------------------------------------------------------
    @staticmethod
    def _clean_and_parse_json(raw_text: str) -> Dict[str, Any]:
        cleaned = raw_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {
                "raw_response": cleaned,
                "parse_error": "LLM response was not valid JSON, raw text preserved."
            }
