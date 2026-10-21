import os
import json
import requests

class AIAgentBrain:
    def __init__(self, config_path: str = "config/settings.json", prompt_path: str = "config/system_prompt.txt"):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
            
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

        # Connects to local on-device Ollama instance (no cloud API key needed)
        self.ollama_url = os.getenv("OLLAMA_HOST", "http://localhost:11434/api/generate")
        self.model_name = self.config.get("llm_model", "tinyllama")

    def generate_response(self, user_query: str) -> str:
        if not user_query.strip():
            return "Hello! I am your assistant. What can I do for you?"

        # Offline local inference query
        try:
            payload = {
                "model": self.model_name,
                "prompt": f"{self.system_prompt}\nUser: {user_query}\nAssistant:",
                "stream": False
            }
            response = requests.post(self.ollama_url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "").strip()
        except Exception as e:
            print(f"[AgentBrain Local] Local LLM notice: {e}")

        # Local dynamic response without cloud
        return f"I heard your request regarding '{user_query}'. Processing locally on your device."
