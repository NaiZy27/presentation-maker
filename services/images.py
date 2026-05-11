import httpx
from core.config import config
from core.logger import get_logger

logger = get_logger(__name__)

_SEARCH_URL = "https://api.unsplash.com/search/photos"
_HEADERS = {"Authorization": f"Client-ID {config.unsplash_access_key.get_secret_value()}"}

_cache: dict[str, bytes] = {}


async def search_image(query: str) -> bytes | None:
    if query in _cache:
        logger.info("Unsplash cache hit: %r", query)
        return _cache[query]

    logger.info("Unsplash search: %r", query)
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            search_resp = await client.get(
                _SEARCH_URL,
                headers=_HEADERS,
                params={"query": query, "per_page": 1, "orientation": "landscape"},
            )
            search_resp.raise_for_status()
            results = search_resp.json().get("results", [])

            if not results:
                logger.warning("Unsplash: no results for %r", query)
                return None

            image_url = results[0]["urls"]["regular"]
            img_resp = await client.get(image_url, timeout=30.0)
            img_resp.raise_for_status()

            image_bytes = img_resp.content
            _cache[query] = image_bytes
            logger.info("Unsplash: downloaded %d bytes for %r", len(image_bytes), query)
            return image_bytes

    except Exception as e:
        logger.warning("Unsplash error for %r: %s", query, e)
        return None
