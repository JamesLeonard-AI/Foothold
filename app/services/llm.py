import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def ask_llm(prompt: str) -> str:
    """
    Send a prompt to OpenAI and return the response.
    """

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    return response.output_text