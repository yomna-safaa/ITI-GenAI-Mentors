'''
pip install openai
# Successfully installed annotated-types-0.8.0 anyio-4.16.0 h11-0.16.0 httpcore2-2.16.2 httpx2-2.16.2 jiter-0.19.0 openai-3.57.0 pydantic-2.14.4 pydantic-core-2.50.5 sniffio-1.3.1 truststore-0.10.5 typing-extensions-4.16.0 typing-inspection-0.4.5

python openAI.py
'''
import os
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

class OpenAI:
    def __init__(self, model="gpt-4"):
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

    def get_openai_chat_completions(self, prompt="What is the capital of France?"):
        # ??

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

openai = OpenAI() # "gpt-3.5-turbo"
openai.get_openai_chat_completions()
