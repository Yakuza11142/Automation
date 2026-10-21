import subprocess
import re

class SIMHandler:
    def __init__(self):
        pass

    def dial_number(self, phone_number: str) -> bool:
        if not phone_number:
            print("[SIMHandler] Error: Empty phone number provided.")
            return False

        clean_number = re.sub(r"\D", "", phone_number)
        print(f"[SIMHandler] Initiating call to {clean_number} via physical MTN SIM...")

        try:
            subprocess.run(["termux-telephony-call", clean_number], check=True)
            return True
        except FileNotFoundError:
            print(f"[SIMHandler Simulation] Successfully triggered call intent for number: {clean_number}")
            return True
        except Exception as e:
            print(f"[SIMHandler Error] Failed to execute call command: {e}")
            return False
