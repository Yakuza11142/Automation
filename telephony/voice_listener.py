import re
import time
from telephony.contacts_manager import ContactsManager
from telephony.sim_handler import SIMHandler

class VoiceCommandListener:
    def __init__(self):
        self.contacts_manager = ContactsManager()
        self.sim_handler = SIMHandler()
        self.running = False

    def start_listening(self):
        self.running = True
        print("[VoiceListener Offline] Service running locally.")

        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                while self.running:
                    try:
                        audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                        
                        # Offline recognition via local Sphinx/Vosk engine
                        try:
                            text = recognizer.recognize_sphinx(audio).lower()
                        except Exception:
                            text = ""

                        if "call" in text:
                            match = re.search(r"call\s+([a-zA-Z0-9\s]+)", text)
                            if match:
                                target_name = match.group(1).strip()
                                number = self.contacts_manager.search_contact(target_name)
                                if number:
                                    self.sim_handler.dial_number(number)
                    except sr.WaitTimeoutError:
                        continue
                    except Exception as e:
                        time.sleep(1)
        except Exception as e:
            print(f"[VoiceListener Local Standby] {e}")

    def stop_listening(self):
        self.running = False
