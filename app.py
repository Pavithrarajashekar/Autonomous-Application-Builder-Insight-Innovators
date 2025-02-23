import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("❌ API Key not found. Set OPENAI_API_KEY environment variable.")
else:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello, AI!"}]
    )
    print(response["choices"][0]["message"]["content"])
