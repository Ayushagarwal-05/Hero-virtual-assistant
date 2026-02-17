import os
from openai import OpenAI
import memory

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

SYSTEM_PROMPT = (
    "You are Hero, a helpful AI assistant. "
    "You must NEVER invent or assume personal information. "
    "You may only use memory provided explicitly. "
    "For general questions, math, fun facts, explanations, answer normally."
)


def build_memory_context():
    facts = memory.list_facts()
    if not facts:
        return "User memory is empty."
    return "User memory:\n" + "\n".join(f"{k}: {v}" for k, v in facts.items())


def think(prompt: str) -> str:
    if not prompt or client is None:
        return ""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "system", "content": build_memory_context()},
                {"role": "user", "content": prompt},
            ],
            max_output_tokens=200,
        )
        return response.output_text.strip()
    except Exception:
        return "I am having trouble thinking right now."
