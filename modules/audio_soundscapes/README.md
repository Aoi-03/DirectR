# Module 3: Music & Audio Studios (Soundscapes & Composition)

**Assigned Collaborator:** Friend 3 (You)  
**Feature Branch:** `feature/audio-studio`  

---

## 🎯 Track Mission

Independent indie game developers, filmmakers, and podcast producers lack real-time adaptive soundscapes tailored to dynamic emotional pacing. DirectR's Audio Studio solves this with an intelligent, tension-adaptive sound design and composition engine.

---

## 🏗️ Architecture & Sub-Engines

```text
modules/audio_soundscapes/
├── engine.py                   # Central unified facade for the Core Orchestrator
├── stems/                      # Dynamic Tension-Adaptive Stems
│   ├── stem_definitions.py     # Stems catalog (pads, 808s, leads, risers, drums)
│   ├── arranger.py             # Continuous BPM curve & dynamic stem cross-fading
│   └── generator.py            # Procedural WAV waveform synthesizer (PCM 16-bit)
├── foley/                      # Zero-Shot Cinematic Foley Synthesizer
│   ├── sound_library.py        # Acoustic resonance & material physical profiles
│   └── synthesizer.py          # Action text cues -> synthesized audio waveforms
├── harmony/                    # AI Microtonal Scale & Chord Builder
│   ├── microtonal.py           # 24-EDO (quarter-tone) cents & pitch bend calculator
│   └── chord_progressions.py   # Psychological chord presets (eerie, paranoia, crisis)
├── mixer/                      # Real-time DSP & Spatializer
│   ├── ducking.py              # Dialogue sidechain attenuation (-12dB)
│   ├── spatializer.py          # Acoustic reverb & room impulse calculation
│   └── dsp_mixer.py            # Multi-track master mixdown manifest
├── web_audio/                  # Interactive Browser Preview
│   └── player.html             # Interactive Web Audio API studio player
└── test_audio.py               # Full test suite (10 unit tests)
```

---

## 🎛️ Interactive Web Audio Studio Player

An interactive HTML5 Web Audio API studio player is included directly inside this module at:
[`modules/audio_soundscapes/web_audio/player.html`](file:///D:/AOI_ABHIJIT/My%20study/Programming/DirectR/modules/audio_soundscapes/web_audio/player.html)

**Features:**
- **Real-time Tension Slider (0.00 – 1.00):** Modulates tempo (65 – 150 BPM), cross-fades multi-channel synthesizer oscillators, and automates low-pass filter cutoff in real-time.
- **Zero-Shot Foley Soundboard:** Real-time procedural audio synthesis for Electric Sparks, Heavy Rain, Footsteps on Gravel, Metallic Clangs, Sub Shockwaves, and Sirens.
- **24-EDO Micro-Tonal Chords:** Audition quarter-tone harmony presets (neutral thirds, sub-minor intervals, crisis clusters) live.
- **Sidechain Ducking Simulation:** Demonstrates dialogue gain ducking (-12dB) under active music beds.
- **Live Oscilloscope Spectrum:** Visualizes waveform and frequency dynamics on an HTML5 canvas.

---

## 🤝 Cross-Module Relationship & Data Contracts

- **From Module 1 (Narrative):**
  - Reads `SceneBeat.tension_score` to determine musical tempo BPM and stem layers.
  - Reads `SceneBeat.dialogue` to calculate sidechain ducking start and end timestamps.
  - Reads `SceneBeat.foley_cues` for zero-shot sound effect synthesis.
- **From Module 2 (Visuals):**
  - Uses visual environment setting to infer acoustic room reverb (Cathedral vs Vault vs Open space).
- **To Module 4 (Creator Distribution):**
  - Provides tension peak timestamps and separated dialogue/music stem mixes for 9:16 vertical reel extraction.
- **To Core Swarm:**
  - Emits `audio.stems_arranged` and `audio.foley_synthesized` events.
  - Populates `StemArrangement` and `FoleyAsset` in `ProductionPackage`.

---

## 🧪 Testing

Run the full test suite for Module 3:
```bash
python -m unittest modules/audio_soundscapes/test_audio.py
```

Run all project tests across all modules:
```bash
python -m unittest discover -s . -p "test_*.py"
```
