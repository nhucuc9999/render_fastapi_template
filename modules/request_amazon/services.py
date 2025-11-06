"""
Service layer for Request Amazon module.

Handles the actual HTTP request to Amazon using httpx.
"""

import httpx


async def fetch_amazon_page(url: str) -> dict:
    """
    Fetch Amazon page content using httpx with browser-like headers.

    Args:
        url: The Amazon URL to fetch

    Returns:
        Dictionary with status, url, page_source (on success)
        or status, message (on error)
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,image/apng,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.amazon.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    try:
        async with httpx.AsyncClient(
            timeout=15.0,
            follow_redirects=True,
            verify=False,
        ) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            return {
                "status": "success",
                "url": str(url),
                "page_source": response.text,
            }

    except httpx.TimeoutException:
        return {
            "status": "error",
            "message": "Request timeout: Amazon did not respond within 15 seconds",
        }
    except httpx.HTTPStatusError as e:
        return {
            "status": "error",
            "message": f"HTTP error {e.response.status_code}: {e.response.reason_phrase}",
        }
    except httpx.RequestError as e:
        return {
            "status": "error",
            "message": f"Request failed: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
        }

