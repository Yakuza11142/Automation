import os
import json

class AudioStreamHandler:
    def __init__(self, config_path: str = "config/settings.json"):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        self.model = None
        self._init_vosk()

    def _init_vosk(self):
        try:
            from vosk import Model
            model_path = "models/vosk-model-small-en-us"
            if os.path.exists(model_path):
                self.model = Model(model_path)
                print("[AudioStream] Local Vosk offline STT model loaded.")
        except Exception as e:
            print(f"[AudioStream Offline] Vosk init notice: {e}")

    def process_incoming_audio(self, audio_bytes: bytes) -> str:
        if not audio_bytes:
            return ""

        try:
            from vosk import KaldiRecognizer
            if self.model:
                rec = KaldiRecognizer(self.model, 16000)
                if rec.AcceptWaveform(audio_bytes):
                    res = json.loads(rec.Result())
                    return res.get("text", "")
        except Exception as e:
            print(f"[AudioStream Offline Error] {e}")

        return ""
