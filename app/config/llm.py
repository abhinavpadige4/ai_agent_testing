import os
from dotenv import load_dotenv
from groq import Groq
from typing import Optional

load_dotenv()
# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Preferred models (priority order)
PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "gemma2-9b-it"


class LLMError(Exception):
    pass


def call_groq(
    prompt: str,
    model: str,
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> str:
    """
    Low-level Groq call
    """
    try:
        response = groq_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        raise LLMError(str(e))


def llm_generate(
    prompt: str,
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> str:
    """
    High-level LLM function with fallback logic
    """

    # 1️⃣ Try primary model (LLaMA)
    try:
        return call_groq(
            prompt=prompt,
            model=PRIMARY_MODEL,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception as primary_error:
        print(f"[WARN] Primary model failed: {primary_error}")

    # 2️⃣ Fallback to Gemma
    try:
        return call_groq(
            prompt=prompt,
            model=FALLBACK_MODEL,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception as fallback_error:
        print(f"[ERROR] Fallback model failed: {fallback_error}")
        raise LLMError("All LLM models failed")


# Simple test
if __name__ == "__main__":
    test_prompt = "Explain what an AI web testing agent is in 3 lines."
    output = llm_generate(test_prompt)
    print(output)
