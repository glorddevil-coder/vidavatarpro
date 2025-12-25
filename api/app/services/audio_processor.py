"""
Trickster Audio Processing Engine

Applies viral voice effect filters:
- Pitch Shift: +4 semitones
- Formant Shift: 0.65x scaling
- Tempo: 1.1x speedup
"""

import numpy as np
import librosa
import soundfile as sf
from typing import Optional, Tuple
from io import BytesIO
import asyncio

class TricksterAudioProcessor:
    def __init__(self):
        self.sr = 22050  # Sample rate
        self.default_pitch_shift = 4  # semitones
        self.default_formant_shift = 0.65
        self.default_tempo_rate = 1.1

    def load_audio(self, audio_path: str) -> Tuple[np.ndarray, int]:
        """Load audio file and return waveform and sample rate."""
        y, sr = librosa.load(audio_path, sr=self.sr)
        return y, sr

    def save_audio(self, y: np.ndarray, output_path: str, sr: int = 22050) -> None:
        """Save audio array to file."""
        sf.write(output_path, y, sr)

    def pitch_shift(self, y: np.ndarray, n_steps: float, sr: int) -> np.ndarray:
        """
        Apply pitch shifting using librosa.
        
        Args:
            y: Audio waveform
            n_steps: Number of semitones to shift (positive = higher)
            sr: Sample rate
        
        Returns:
            Pitch-shifted audio
        """
        return librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)

    def formant_shift(self, y: np.ndarray, shift_factor: float, sr: int) -> np.ndarray:
        """
        Apply formant shifting via resampling trick.
        Simulates vocal tract scaling.
        
        Args:
            y: Audio waveform
            shift_factor: Formant scaling factor (0.65 = lower formants)
            sr: Sample rate
        
        Returns:
            Formant-shifted audio
        """
        # Resample to apply formant shift
        n_samples = int(len(y) / shift_factor)
        shifted = librosa.resample(y, orig_sr=sr, target_sr=int(sr / shift_factor))
        
        # Pad or trim to original length
        if len(shifted) < len(y):
            shifted = np.pad(shifted, (0, len(y) - len(shifted)))
        else:
            shifted = shifted[:len(y)]
        
        return shifted

    def time_stretch(self, y: np.ndarray, rate: float) -> np.ndarray:
        """
        Apply time stretching (tempo change without pitch change).
        
        Args:
            y: Audio waveform
            rate: Time stretch rate (1.1 = 10% faster)
        
        Returns:
            Time-stretched audio
        """
        return librosa.effects.time_stretch(y, rate=rate)

    def apply_trickster_effect(
        self,
        audio_path: str,
        pitch_shift: float = None,
        formant_shift: float = None,
        tempo_rate: float = None,
    ) -> np.ndarray:
        """
        Apply the complete Trickster effect pipeline.
        
        Args:
            audio_path: Path to input audio file
            pitch_shift: Semitones to shift (default: +4)
            formant_shift: Formant scaling factor (default: 0.65)
            tempo_rate: Tempo speedup rate (default: 1.1)
        
        Returns:
            Processed audio waveform
        """
        # Use defaults if not specified
        pitch_shift = pitch_shift or self.default_pitch_shift
        formant_shift = formant_shift or self.default_formant_shift
        tempo_rate = tempo_rate or self.default_tempo_rate

        # Load audio
        y, sr = self.load_audio(audio_path)

        # Apply effects in sequence
        print(f"Applying pitch shift: +{pitch_shift} semitones")
        y = self.pitch_shift(y, pitch_shift, sr)

        print(f"Applying formant shift: {formant_shift}x")
        y = self.formant_shift(y, formant_shift, sr)

        print(f"Applying tempo stretch: {tempo_rate}x")
        y = self.time_stretch(y, tempo_rate)

        return y

    async def process_async(
        self,
        audio_path: str,
        output_path: str,
        pitch_shift: float = None,
        formant_shift: float = None,
        tempo_rate: float = None,
    ) -> dict:
        """
        Asynchronously process audio with Trickster effect.
        
        Returns:
            Dict with processing results
        """
        loop = asyncio.get_event_loop()
        try:
            y = await loop.run_in_executor(
                None,
                self.apply_trickster_effect,
                audio_path,
                pitch_shift,
                formant_shift,
                tempo_rate,
            )
            
            await loop.run_in_executor(None, self.save_audio, y, output_path)
            
            return {
                "success": True,
                "output_path": output_path,
                "samples_processed": len(y),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }


# Singleton instance
processor = TricksterAudioProcessor()
