"""
Pydantic schemas for Request Amazon module.
"""

from typing import Optional

from pydantic import BaseModel, HttpUrl


class RequestAmazonInput(BaseModel):
    """Input schema for Amazon URL request."""

    url: HttpUrl


class RequestAmazonResponse(BaseModel):
    """Response schema for Amazon page fetch."""

    status: str
    url: Optional[str] = None
    page_source: Optional[str] = None
    message: Optional[str] = None

