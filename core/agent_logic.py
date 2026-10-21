import os
import json

class AIAgentBrain:
    def __init__(self, config_path: str = "config/settings.json", prompt_path: str = "config/system_prompt.txt"):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
            
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

        self.api_key = os.getenv("OPENAI_API_KEY", self.config.get("openai_api_key", ""))

    def generate_response(self, user_query: str) -> str:
        if not user_query.strip():
            return "Hello! I am Peter's autonomous assistant. What would you like to discuss or accomplish today?"

        if not self.api_key or self.api_key == "YOUR_OPENAI_API_KEY":
            return f"I received your inquiry regarding '{user_query}'. I am processing this request dynamically on Peter's local system."

        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[AgentBrain Error] OpenAI call failed: {e}")
            return f"I processed your query ('{user_query}'), but encountered a temporary connection issue. Let me know how else I can assist!"
