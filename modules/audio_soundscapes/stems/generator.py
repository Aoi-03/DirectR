"""
Procedural WAV Audio Synthesizer
Generates real audible WAV audio data in pure Python using standard library math, struct, and wave.
No external heavy C-libraries or ffmpeg required.
"""

import math
import struct
import wave
import io
from typing import List, Dict, Any


class ProceduralWavSynthesizer:
    """
    Synthesizes multi-oscillator acoustic waveforms (sine, saw, square, noise)
    into standard 16-bit PCM WAV audio streams.
    """

    SAMPLE_RATE = 44100

    @staticmethod
    def generate_sine_tone(
        frequency_hz: float, duration_sec: float, amplitude: float = 0.5
    ) -> bytes:
        """Generates pure sine wave audio bytes."""
        num_samples = int(ProceduralWavSynthesizer.SAMPLE_RATE * duration_sec)
        raw_samples = []

        for i in range(num_samples):
            t = i / ProceduralWavSynthesizer.SAMPLE_RATE
            # Sine wave with gentle attack/release envelope
            envelope = min(1.0, i / 2000) * min(1.0, (num_samples - i) / 2000)
            sample = amplitude * envelope * math.sin(2.0 * math.pi * frequency_hz * t)
            # 16-bit signed integer clipping
            clamped = max(-1.0, min(1.0, sample))
            raw_samples.append(int(clamped * 32767))

        return ProceduralWavSynthesizer._wrap_wav_pcm(raw_samples)

    @staticmethod
    def generate_tension_riser(
        start_hz: float = 120.0,
        end_hz: float = 1800.0,
        duration_sec: float = 3.0,
        amplitude: float = 0.6,
    ) -> bytes:
        """
        Generates an exponential tension riser sweep with combined saw and noise textures.
        """
        num_samples = int(ProceduralWavSynthesizer.SAMPLE_RATE * duration_sec)
        raw_samples = []
        phase = 0.0

        for i in range(num_samples):
            fraction = i / num_samples
            # Exponential pitch increase
            current_hz = start_hz * math.pow(end_hz / start_hz, fraction)
            phase += 2.0 * math.pi * current_hz / ProceduralWavSynthesizer.SAMPLE_RATE

            saw = 2.0 * (phase / (2.0 * math.pi) - math.floor(phase / (2.0 * math.pi) + 0.5))
            sine = math.sin(phase)

            # Amplitude swell towards climax
            amp_swell = amplitude * (0.2 + 0.8 * fraction)
            combined = amp_swell * (0.6 * saw + 0.4 * sine)

            clamped = max(-1.0, min(1.0, combined))
            raw_samples.append(int(clamped * 32767))

        return ProceduralWavSynthesizer._wrap_wav_pcm(raw_samples)

    @staticmethod
    def generate_percussion_kick(duration_sec: float = 0.4, amplitude: float = 0.85) -> bytes:
        """
        Generates a punchy synth kick drum with pitch-drop envelope and sub-weight.
        """
        num_samples = int(ProceduralWavSynthesizer.SAMPLE_RATE * duration_sec)
        raw_samples = []
        phase = 0.0

        for i in range(num_samples):
            fraction = i / num_samples
            # Pitch drops rapidly from 160Hz to 40Hz
            current_hz = 40.0 + 120.0 * math.exp(-25.0 * fraction)
            phase += 2.0 * math.pi * current_hz / ProceduralWavSynthesizer.SAMPLE_RATE

            # Fast exponential amplitude decay
            decay = amplitude * math.exp(-8.0 * fraction)
            sample = decay * math.sin(phase)

            clamped = max(-1.0, min(1.0, sample))
            raw_samples.append(int(clamped * 32767))

        return ProceduralWavSynthesizer._wrap_wav_pcm(raw_samples)

    @staticmethod
    def _wrap_wav_pcm(samples: List[int], channels: int = 1) -> bytes:
        """Wraps 16-bit integer samples into valid RIFF WAV binary stream."""
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(ProceduralWavSynthesizer.SAMPLE_RATE)
            packed_frames = struct.pack(f"<{len(samples)}h", *samples)
            wav_file.writeframes(packed_frames)
        return buffer.getvalue()
