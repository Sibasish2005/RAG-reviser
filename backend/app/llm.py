import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "openai/gpt-oss-120b"


def generate_answer(query, context):

    prompt = f"""
You are an AI revision assistant.

Answer the user's question using the provided lecture context.

Rules:
- Use the lecture context as your primary source.
- Do not invent information that is not present in the context.
- Explain the answer clearly and accurately.
- If the context does not contain enough information, say so.

LECTURE CONTEXT:
{context}

USER QUESTION:
{query}
"""

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
        stream=True,
    )

    for chunk in stream:

        content = chunk.choices[0].delta.content

        if content:
            yield content