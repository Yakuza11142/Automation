import os
import sys
import time
import json
import ctypes
from core.agent_logic import AIAgentBrain
from core.audio_stream import AudioStreamHandler
from core.voice_synth import VoiceSynthesizer
from telephony.voice_listener import VoiceCommandListener

class LocalAIVoiceAgent:
    def __init__(self, config_path: str = "config/settings.json"):
        print("[Agent System] Booting local offline AI voice architecture...")
        self.config_path = config_path
        
        # Load configuration file
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
            
        self.brain = AIAgentBrain(config_path=config_path)
        self.audio_stream = AudioStreamHandler(config_path=config_path)
        self.voice_synth = VoiceSynthesizer(config_path=config_path)
        self.listener = VoiceCommandListener()
        
        # Verify native .so library status on initialization
        self.so_path = self.config.get("libs_path", "libs/libTessSDK.so")
        self._verify_native_binary()

    def _verify_native_binary(self):
        """Verifies binary existence and dynamic loading via ctypes."""
        if os.path.exists(self.so_path):
            try:
                # Dynamic C-runtime loading of the shared object binary
                self.loaded_so = ctypes.CDLL(self.so_path)
                print(f"[Agent System] Native library successfully loaded into RAM: {self.so_path}")
            except Exception as e:
                print(f"[Agent System Warning] Native library found at {self.so_path} but ctypes failed to load: {e}")
                self.loaded_so = None
        else:
            print(f"[Agent System Notice] {self.so_path} not detected on disk. Place libTessSDK.so in libs/.")
            self.loaded_so = None

    def process_query_dynamically(self, raw_audio_or_text: str) -> bytes:
        """
        Receives input dynamically, routes binary queries to libTessSDK.so, 
        and converts generated answers into your cloned voice.
        """
        if not raw_audio_or_text or not raw_audio_or_text.strip():
            return b""

        print(f"[Agent System Input] Received query: '{raw_audio_or_text}'")

        # 1. Ask AI Brain to evaluate query (handles .so queries dynamically via ctypes)
        response_text = self.brain.generate_response(raw_audio_or_text)
        print(f"[Agent System Brain Output] {response_text}")

        # 2. Convert text response into voice audio using PTT-20260405-WA0001.opus voice clone
        speech_audio_bytes = self.voice_synth.synthesize(response_text)
        return speech_audio_bytes

    def run(self):
        """Main execution loop for listening and managing telephony events."""
        print("[Agent System] Agent active. Listening for physical SIM calls & voice commands...")
        try:
            # Start background microphone and telephony service
            self.listener.start_listening()
        except KeyboardInterrupt:
            print("\n[Agent System] Terminating agent gracefully...")
            self.listener.stop_listening()
            sys.exit(0)

if __name__ == "__main__":
    agent = LocalAIVoiceAgent()
    agent.run()
