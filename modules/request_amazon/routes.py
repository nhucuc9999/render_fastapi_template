"""
Routes for Request Amazon module.
"""

from fastapi import APIRouter

from .schemas import RequestAmazonInput, RequestAmazonResponse
from .services import fetch_amazon_page

router = APIRouter(prefix="/request_amazon", tags=["Request Amazon"])


@router.post("/fetch", response_model=RequestAmazonResponse)
async def fetch_page(payload: RequestAmazonInput) -> RequestAmazonResponse:
    """
    Fetch Amazon page content.

    Args:
        payload: Request body containing the Amazon URL

    Returns:
        RequestAmazonResponse with page source or error message
    """
    result = await fetch_amazon_page(str(payload.url))
    return RequestAmazonResponse(**result)

