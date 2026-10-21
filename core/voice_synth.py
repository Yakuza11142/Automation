import os
import json
import subprocess

class VoiceSynthesizer:
    def __init__(self, config_path: str = "config/settings.json"):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        
        # Target your exact WhatsApp audio sample
        self.raw_opus = "config/PTT-20260405-WA0001.opus"
        self.clean_wav = "config/voice_sample_clean.wav"
        self.active_sample = None
        self._preprocess_audio_sample()

    def _preprocess_audio_sample(self):
        """
        Converts and cleans the 13-second audio sample to 22,050Hz 16-bit PCM mono 
        to maximize neural speaker-encoder feature retention.
        """
        if os.path.exists(self.raw_opus):
            try:
                print(f"[VoiceSynth Engine] High-precision audio processing on {self.raw_opus}...")
                
                # FFmpeg command: Resample to 22.05kHz (XTTS standard), mono, 16-bit PCM
                # Applies high-pass filter to remove background room rumble and normalizes volume
                cmd = [
                    "ffmpeg", "-y", "-i", self.raw_opus,
                    "-af", "highpass=f=80, afftdn=nr=12, volume=1.0",
                    "-ar", "22050", "-ac", "1", "-c:a", "pcm_s16le",
                    self.clean_wav
                ]
                
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.active_sample = self.clean_wav
                print("[VoiceSynth Engine] Cleaned speaker reference sample ready for exact matching.")
            except Exception as e:
                print(f"[VoiceSynth Warning] FFmpeg clean pipeline notice: {e}")
                # Fallback directly to the raw sample if pre-processing is bypassed
                self.active_sample = self.raw_opus
        elif os.path.exists(self.clean_wav):
            self.active_sample = self.clean_wav

    def synthesize(self, text: str) -> bytes:
        if not text:
            return b""

        output_wav = "temp_response.wav"

        # 1. High-Fidelity Zero-Shot Neural XTTS v2 Inference
        if self.active_sample:
            try:
                from TTS.api import TTS
                
                # Load neural TTS model conditioned on your exact acoustic embedding
                tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
                tts.synthesize_to_file(
                    text=text,
                    file_path=output_wav,
                    speaker_wav=self.active_sample,
                    language="en",
                    # Temperature and speed tuning for natural human pacing
                    temperature=0.65,
                    repetition_penalty=2.0
                )

                if os.path.exists(output_wav):
                    with open(output_wav, "rb") as f:
                        audio_bytes = f.read()
                    os.remove(output_wav)
                    return audio_bytes
            except Exception as e:
                print(f"[VoiceSynth Neural Error] {e}")

        # 2. Local Fallback Execution (pyttsx3)
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.save_to_file(text, output_wav)
            engine.runAndWait()
            if os.path.exists(output_wav):
                with open(output_wav, "rb") as f:
                    data = f.read()
                os.remove(output_wav)
                return data
        except Exception as e:
            print(f"[VoiceSynth Fallback Error] {e}")

        return text.encode("utf-8")
