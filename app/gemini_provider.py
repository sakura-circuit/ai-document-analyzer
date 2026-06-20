import os

from google import genai

from app.prompt_builder import build_prompt

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def answer_question(question: str, context: str) -> str:

    prompt = build_prompt(question, context)

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    return response.text or ""
