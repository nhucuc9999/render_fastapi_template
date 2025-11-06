"""
Service layer for Request Amazon module.

Handles the actual HTTP request to Amazon using httpx.
"""

import asyncio
from typing import Optional

import httpx

from utils.random_useragent import get_random_user_agent


def parse_cookies(cookie_string: Optional[str]) -> dict:
    """
    Parse cookie string into dictionary.

    Args:
        cookie_string: Cookie string in format "key1=value1; key2=value2"

    Returns:
        Dictionary of cookies
    """
    if not cookie_string:
        return {}

    cookies = {}
    for cookie in cookie_string.split(";"):
        cookie = cookie.strip()
        if "=" in cookie:
            key, value = cookie.split("=", 1)
            cookies[key.strip()] = value.strip()

    return cookies


def parse_proxy(proxy_string: Optional[str]) -> Optional[dict]:
    """
    Parse proxy string into httpx-compatible proxy dictionary.

    Args:
        proxy_string: Proxy URL (e.g., "socks5://user:pass@host:port")

    Returns:
        Dictionary with "http://" and "https://" keys, or None if no proxy
    """
    if not proxy_string:
        return None

    # Remove trailing slash if present
    proxy_string = proxy_string.rstrip("/")

    # Return dict with both http and https using the same proxy
    return {
        "http://": proxy_string,
        "https://": proxy_string,
    }


async def fetch_amazon_page(
    url: str,
    cookies: Optional[str] = None,
    proxy: Optional[str] = None,
    max_retries: int = 3,
) -> dict:
    """
    Fetch Amazon page content using httpx with browser-like headers.

    Args:
        url: The Amazon URL to fetch
        cookies: Optional cookie string in format "key1=value1; key2=value2"
        proxy: Optional proxy URL (supports http, https, socks5)
        max_retries: Maximum number of retry attempts (default: 3)

    Returns:
        Dictionary with status, url, page_source (on success)
        or status, message (on error)
    """
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.amazon.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
        "DNT": "1",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    timeout = httpx.Timeout(30.0, connect=10.0)

    # Parse cookies if provided
    cookies_dict = parse_cookies(cookies) if cookies else {}

    # Parse proxy if provided
    proxies_dict = parse_proxy(proxy)

    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(
                timeout=timeout,
                follow_redirects=True,
                verify=False,
                http2=True,
                proxies=proxies_dict,
            ) as client:
                # Add small delay between retries (except first attempt)
                if attempt > 0:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff

                response = await client.get(url, headers=headers, cookies=cookies_dict)

                # Retry on 503 Service Unavailable
                if response.status_code == 503:
                    if attempt < max_retries - 1:
                        continue
                    return {
                        "status": "error",
                        "message": (
                            f"Amazon returned 503 Service Unavailable "
                            f"(attempted {max_retries} times). "
                            "Amazon may be blocking the request or the service is temporarily unavailable."
                        ),
                    }

                response.raise_for_status()

                return {
                    "status": "success",
                    "url": str(url),
                    "page_source": response.text,
                }

        except httpx.TimeoutException:
            if attempt < max_retries - 1:
                continue
            return {
                "status": "error",
                "message": (
                    f"Request timeout: Amazon did not respond within {timeout.timeout} seconds "
                    f"(attempted {max_retries} times)"
                ),
            }
        except httpx.HTTPStatusError as e:
            # Retry on 5xx errors (except 503 which is handled above)
            if e.response.status_code >= 500 and attempt < max_retries - 1:
                continue
            return {
                "status": "error",
                "message": f"HTTP error {e.response.status_code}: {e.response.reason_phrase}",
            }
        except httpx.RequestError as e:
            if attempt < max_retries - 1:
                continue
            return {
                "status": "error",
                "message": f"Request failed: {str(e)}",
            }
        except Exception as e:
            if attempt < max_retries - 1:
                continue
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
            }

    # Should not reach here, but just in case
    return {
        "status": "error",
        "message": f"Failed after {max_retries} attempts",
    }

