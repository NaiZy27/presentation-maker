import asyncio
from google import genai
from google.genai import types as genai_types

from core.config import config
from core.models import PresentationContent
from core.logger import get_logger
from prompts.system_prompt import build_prompt

logger = get_logger(__name__)

_client = genai.Client(api_key=config.gemini_api_key.get_secret_value())

_MODEL = "gemini-2.5-flash-lite"
_MAX_RETRIES = 3
_RETRY_DELAY = 2.0

_RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "slides": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "header": {"type": "STRING"},
                    "text": {"type": "STRING"},
                    "image_query": {"type": "STRING"},
                },
                "required": ["header", "text", "image_query"],
            },
        },
    },
    "required": ["slides"],
}


async def generate_content(topic: str, language: str, requirements: str) -> PresentationContent:
    prompt = build_prompt(topic, language, requirements)

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            logger.info("Gemini request: topic=%r language=%r attempt=%d", topic, language, attempt)
            response = await _client.aio.models.generate_content(
                model=_MODEL,
                contents=prompt,
                config=genai_types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=_RESPONSE_SCHEMA,
                ),
            )
            result = PresentationContent.model_validate_json(response.text)
            logger.info("Gemini response: %d slides received", len(result.slides))
            return result
        except Exception as e:
            logger.warning("Gemini attempt %d/%d failed: %s", attempt, _MAX_RETRIES, e)
            if attempt == _MAX_RETRIES:
                raise
            await asyncio.sleep(_RETRY_DELAY * attempt)

    raise RuntimeError("Unreachable")
