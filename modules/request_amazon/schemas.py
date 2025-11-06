"""
Pydantic schemas for Request Amazon module.
"""

from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class RequestAmazonInput(BaseModel):
    """Input schema for Amazon URL request."""

    url: HttpUrl
    cookies: Optional[str] = Field(
        default=None,
        description="Cookie string in format 'key1=value1; key2=value2'",
        examples=["session-id=123-456; session-token=abc123"],
    )
    proxy: Optional[str] = Field(
        default=None,
        description="Proxy URL (supports http, https, socks5). Example: socks5://user:pass@host:port",
        examples=["socks5://aa:bbb@11.41.169.235:111"],
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "url": "https://www.amazon.com/",
                "cookies": "session-id=123-456; session-token=abc123",
                "proxy": "socks5://aa:bbb@11.41.169.235:111",
            }
        }
    }


class RequestAmazonResponse(BaseModel):
    """Response schema for Amazon page fetch."""

    status: str
    url: Optional[str] = None
    page_source: Optional[str] = None
    message: Optional[str] = None

