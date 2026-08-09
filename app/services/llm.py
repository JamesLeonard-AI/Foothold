import json
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


def ask_llm_json(prompt: str, schema: dict) -> dict:
    """
    Send a prompt to OpenAI and return structured JSON.
    """

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "structured_response",
                "schema": schema,
                "strict": True,
            }
        },
    )

    return json.loads(response.output_text)