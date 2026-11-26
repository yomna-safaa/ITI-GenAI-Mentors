'''
pip install openai
# Successfully installed annotated-types-0.8.0 anyio-4.16.0 h11-0.16.0 httpcore2-2.16.2 httpx2-2.16.2 jiter-0.19.0 openai-3.57.0 pydantic-2.14.4 pydantic-core-2.50.5 sniffio-1.3.1 truststore-0.10.5 typing-extensions-4.16.0 typing-inspection-0.4.5

python openAI_correct.py
'''
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# trial_model = "gpt-6.2-astra"
trial_model = "gpt-6-luna"

# Rates in USD per 1,000,000 tokens: (input, cached_input, output)
MODEL_PRICING = {
    "gpt-6.2-astra": (8.00, 0.40, 40.00),
    "gpt-6.2-sol":   (2.00, 0.10, 10.00),
    "gpt-6.1-terra": (1.00, 0.05,  5.00),
    "gpt-6-luna":    (0.10, 0.01,  0.50),
}

class OpenAI_Client:
    def __init__(self, model="gpt-6-luna"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing; add it to your .env file.")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def call_via_chat_completions(self, prompt):
        # https://developers.openai.com/api/reference/python/resources/chat/subresources/completions/methods/create
        messages = [
            {"role": "user", "content": prompt}
        ]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        # print(completion.choices[0].message)
        # # ChatCompletionMessage(content='..........', refusal=None, role='assistant', annotations=[], 
        # audio=None, function_call=None, tool_calls=None)
        return completion.choices[0].message.content

    def call_via_responses(self, prompt):
        # https://developers.openai.com/api/docs/guides/migrate-to-responses?api-mode=responses&lang=python
        response = self.client.responses.create(
            model=self.model,
            input=prompt
        )
        # print(response.output_text)
        # # Log token usage
        # usage = response.usage
        # print(
        #     f"Tokens used | Input: {usage.input_tokens} | "
        #     f"Output: {usage.output_tokens} | Total: {usage.total_tokens}"
        # ) # Tokens used | Input: 10 | Output: 38 | Total: 48
        return response

    def estimate_cost(self, usage) -> float:
        print( "================================")
        # print(
        #     f"Tokens used | Input: {usage.input_tokens} | "
        #     f"Output: {usage.output_tokens} | Total: {usage.total_tokens}"
        # )
        if self.model not in MODEL_PRICING:
            raise ValueError(f"Model {self.model} not found in pricing information.")

        input_rate, cached_rate, output_rate = MODEL_PRICING[self.model]
        # Safely access cached_tokens inside input_tokens_details
        cached_tokens = getattr(usage.input_tokens_details, "cached_tokens", 0) or 0
        uncached_input_tokens = max(0, usage.input_tokens - cached_tokens)
        
        total_cost = (
            (uncached_input_tokens / 1_000_000) * input_rate
            + (cached_tokens / 1_000_000) * cached_rate
            + (usage.output_tokens / 1_000_000) * output_rate
        )
        print(
            f"Model: {self.model} | "
            f"Input tokens: {usage.input_tokens} | "
            f"Output tokens: {usage.output_tokens} | "
            f"Est. Cost: ${total_cost:.6f}"
        )

if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ").strip()

    openai_client = OpenAI_Client(model=trial_model)

    # print('------------------------------')
    # output_text = openai_client.call_via_chat_completions(user_prompt)
    # print(output_text)

    print('------------------------------')
    response = openai_client.call_via_responses(user_prompt)
    print(response.output_text)
    openai_client.estimate_cost(response.usage)
    