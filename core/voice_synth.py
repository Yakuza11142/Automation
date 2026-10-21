import os
import json

class VoiceSynthesizer:
    def __init__(self, config_path: str = "config/settings.json"):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        
        self.engine = None
        self._init_engine()

    def _init_engine(self):
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 160)
        except Exception as e:
            print(f"[VoiceSynth Offline] Local TTS engine notice: {e}")

    def synthesize(self, text: str) -> bytes:
        if not text:
            return b""
        
        try:
            import pyttsx3
            output_file = "temp_response.wav"
            engine = pyttsx3.init()
            engine.save_to_file(text, output_file)
            engine.runAndWait()
            
            if os.path.exists(output_file):
                with open(output_file, "rb") as f:
                    data = f.read()
                os.remove(output_file)
                return data
        except Exception as e:
            print(f"[VoiceSynth Offline Error] {e}")
            
        return text.encode("utf-8")
