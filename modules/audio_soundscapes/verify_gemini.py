"""
DirectR Module 3 — Gemini API Live Verification Script
Run this script to immediately test your Gemini API Key:
    python modules/audio_soundscapes/verify_gemini.py
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))
load_dotenv(ROOT_DIR / ".env", override=True)

from modules.audio_soundscapes.gemini_audio import GeminiAudioEngine


def main():
    print("=" * 70)
    print("🎧 DIRECTR MODULE 3: GEMINI AUDIO ENGINE VERIFICATION")
    print("=" * 70)

    engine = GeminiAudioEngine()

    if not engine.is_configured():
        print("\n❌ GEMINI_API_KEY NOT FOUND!")
        print("\nTo activate Gemini in your Audio Studio:")
        print("  1. Open the file: DirectR/.env")
        print("  2. Paste your Gemini API Key:")
        print("     GEMINI_API_KEY=AIzaSyYourActualKeyHere...")
        print("  3. Save the file and run this script again:\n")
        print("     python modules/audio_soundscapes/verify_gemini.py\n")
        sys.exit(1)

    key = engine.api_key
    masked_key = f"{key[:6]}...{key[-4:]}" if len(key) > 10 else "***"
    print(f"\n🔑 Gemini API Key Detected: {masked_key}")
    print("⏳ Contacting Google Gemini API for live soundscape synthesis...\n")

    try:
        # Test 1: Soundscape Composition
        print("--- [TEST 1/2] Generating Cinematic Stem Composition & Lyria Prompt ---")
        composition = engine.generate_soundscape_composition(
            scene_title="Neon Vault Breach",
            tension_score=0.88,
            visual_mood="Cyberpunk Noir / High Tension",
            location="Subterranean Server Citadel",
            action_description="Laser security alarms trip as drones descend from the shadowed ceiling",
        )

        print(f"  • Tempo: {composition.get('tempo_bpm', 'N/A')} BPM")
        print(f"  • Key Signature: {composition.get('key_signature', 'N/A')}")
        print(f"  • Emotional Valence: {composition.get('emotional_valence', 'N/A')}")
        print(f"  • Lyria/MusicLM Prompt:\n    \"{composition.get('lyria_musiclm_prompt', 'N/A')}\"")

        # Test 2: Zero-Shot Foley Design
        print("\n--- [TEST 2/2] Generating Zero-Shot Foley Sound Design ---")
        foley = engine.design_zero_shot_foley(
            cue_name="LaserTripwireSpark",
            cue_description="High-voltage plasma beam cut by boot with metallic echo",
            scene_location="Subterranean Citadel",
        )
        print(f"  • Cue: {foley.get('cue_name')}")
        print(f"  • Detected Material: {foley.get('detected_material')}")
        print(f"  • Fundamental Frequency: {foley.get('fundamental_freq_hz')} Hz")
        print(f"  • Sound Designer Recipe:\n    \"{foley.get('sound_designer_recipe', 'N/A')}\"")

        print("\n" + "=" * 70)
        print("🎉 SUCCESS! Your Gemini API Key is active and working perfectly in DirectR!")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error calling Gemini API: {e}")
        print("Please verify your internet connection and that the API key is active on Google AI Studio.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
