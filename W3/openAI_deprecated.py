
import os
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

# trial_model = "gpt-4"
# trial_model = "gpt-6.2-astra"
trial_model = "gpt-6-luna"

class OpenAI_REST:
    def __init__(self, model="gpt-6-luna"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing; add it to your .env file.")
        self.api_key = api_key
        self.url = "https://api.openai.com/v1/chat/completions"
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def get_openai_chat_completions(self, prompt):
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("\n✅ Connection Successful!")
                pprint(data)
            else:
                print(f"❌ Failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

openai_r = OpenAI_REST(model=trial_model)
openai_r.get_openai_chat_completions(prompt="What is the capital of Egypt?")
