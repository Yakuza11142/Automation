import os
import sys
import time
import json
import ctypes
import subprocess
from core.agent_logic import AIAgentBrain
from core.audio_stream import AudioStreamHandler
from core.voice_synth import VoiceSynthesizer
from telephony.voice_listener import VoiceCommandListener

class LocalAIVoiceAgent:
    def __init__(self, config_path: str = "config/settings.json"):
        print("[Agent System] Booting local offline AI voice architecture...")
        
        # Automatically acquire maximum mobile wake lock on startup to prevent sleep
        self._acquire_mobile_wake_lock()

        self.config_path = config_path
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
            
        self.brain = AIAgentBrain(config_path=config_path)
        self.audio_stream = AudioStreamHandler(config_path=config_path)
        self.voice_synth = VoiceSynthesizer(config_path=config_path)
        self.listener = VoiceCommandListener()
        
        self.so_path = self.config.get("libs_path", "libs/libTessSDK.so")
        self._verify_native_binary()

    def _acquire_mobile_wake_lock(self):
        """Forces Android/Termux to acquire a permanent wake lock at maximum system level."""
        try:
            print("[Mobile Power] Requesting maximum system wake lock...")
            subprocess.run(["termux-wake-lock"], check=True)
            print("[Mobile Power] Wake lock acquired successfully. CPU will remain active.")
        except Exception as e:
            print(f"[Mobile Power Warning] Could not set wake lock automatically: {e}. Run 'termux-wake-lock' manually in Termux.")

    def _verify_native_binary(self):
        if os.path.exists(self.so_path):
            try:
                self.loaded_so = ctypes.CDLL(self.so_path)
                print(f"[Agent System] Native library successfully loaded into RAM: {self.so_path}")
            except Exception as e:
                print(f"[Agent System Warning] Native library found at {self.so_path} but ctypes failed to load: {e}")
                self.loaded_so = None
        else:
            print(f"[Agent System Notice] {self.so_path} not detected on disk.")
            self.loaded_so = None

    def process_query_dynamically(self, raw_audio_or_text: str) -> bytes:
        if not raw_audio_or_text or not raw_audio_or_text.strip():
            return b""

        print(f"[Agent System Input] Received query: '{raw_audio_or_text}'")
        response_text = self.brain.generate_response(raw_audio_or_text)
        print(f"[Agent System Brain Output] {response_text}")

        speech_audio_bytes = self.voice_synth.synthesize(response_text)
        return speech_audio_bytes

    def run(self):
        print("[Agent System] Agent active 24/7. Listening for voice commands...")
        try:
            self.listener.start_listening()
        except KeyboardInterrupt:
            print("\n[Agent System] Terminating agent gracefully...")
            # Release wake lock on safe shutdown
            try:
                subprocess.run(["termux-wake-unlock"])
            except:
                pass
            self.listener.stop_listening()
            sys.exit(0)

if __name__ == "__main__":
    agent = LocalAIVoiceAgent()
    agent.run()
