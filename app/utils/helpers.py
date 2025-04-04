import json
from typing import AsyncIterator

import aiohttp

from app.config import DEFAULT_MODEL, OLLAMA_API_URL
from app.utils.logger import log


async def call_ollama_api(messages: list) -> AsyncIterator[str]:
    """
    Calls the Ollama API to generate a response for the given prompt.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "stream": True,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                OLLAMA_API_URL, headers=headers, json=payload
            ) as response:
                if response.status != 200:  # Changed status_code to status
                    error_text = await response.text()
                    log(
                        "ERROR",
                        f"Ollama API streaming error {response.status}: {error_text}",
                    )
                    yield f"API error: {response.status}"
                    return

                async for line in response.content:
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            content_chunk = data["message"]["content"]
                            if content_chunk:
                                yield content_chunk
                    except json.JSONDecodeError:
                        log("WARNING", f"Failed to parse JSON from Ollama API: {line}")
                    except Exception as e:
                        log("ERROR", f"Error processing streaming response: {e}")
    except Exception as e:
        log("ERROR", f"Exception in streaming Ollama API call: {e}")
        yield f"API Error: {e}"


def format_message(message: str) -> str:
    """
    Helper to format messages.
    """
    return message.strip()
