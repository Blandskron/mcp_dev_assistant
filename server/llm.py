import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_code_from_prompt(prompt: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4",  # o "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "Eres un asistente experto en desarrollo de software."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1000
    )
    return response.choices[0].message.content
