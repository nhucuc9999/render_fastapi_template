<!-- 088ef19d-93a7-48dc-899a-2abab921368b 8eebb80f-ce14-4792-ba85-6b379c9904c8 -->
# Create request_amazon Module

## Overview

Create a complete module-based FastAPI module at `api/app/modules/request_amazon/` that provides an endpoint to fetch Amazon page content using httpx with browser-like headers.

## Files to Create

### 1. Directory Structure

- Create `api/app/modules/request_amazon/` directory
- Create all required module files following the standard pattern

### 2. `api/app/modules/request_amazon/schemas.py`

- Define `RequestAmazonInput` Pydantic model with `url: str` field
- Define `RequestAmazonResponse` Pydantic model with:
- `status: str` (success/error)
- `url: Optional[str]` (for success case)
- `page_source: Optional[str]` (HTML content for success)
- `message: Optional[str]` (error message for error case)

### 3. `modules/request_amazon/services.py`

- Implement `async def fetch_amazon_page(url: str) -> dict` function
- Use `httpx.AsyncClient` with:
- Browser-like headers (User-Agent, Accept, Accept-Language, Referer, Accept-Encoding, Connection)
- `timeout=15`
- `follow_redirects=True`
- `verify=False`
- Handle exceptions (timeout, connection errors, etc.)
- Return dict with status and appropriate fields

### 4. `api/app/modules/request_amazon/routes.py`

- Create FastAPI router with prefix `/request_amazon` and tag `["Request Amazon"]`
- Define POST endpoint `/fetch` that:
- Accepts `RequestAmazonInput` as payload
- Calls `fetch_amazon_page()` service
- Returns `RequestAmazonResponse`

### 5. `api/app/modules/request_amazon/repositories.py`

- Create placeholder `RequestAmazonRepository` class (for future DB logging)

### 6. `api/app/modules/request_amazon/models.py`

- Create placeholder file (for future DB models if needed)

### 7. `api/app/modules/request_amazon/__init__.py`

- Add module docstring and export router

### 8. `api/app/__init__.py`

- Create if doesn't exist for package structure

### 9. `api/app/modules/__init__.py`

- Create if doesn't exist for package structure

### 10. Update `requirements.txt`

- Add `httpx` dependency

### 11. Update `main.py`

- Import router from `app.modules.request_amazon.routes`
- Include router in FastAPI app using `app.include_router()`

## Implementation Details

- All code uses async/await patterns
- Headers configured to mimic real browser (including User-Agent rotation capability)
- Proper error handling with try/except blocks
- Pydantic v2 compatible models
- Code follows Python best practices (black/flake8 compatible)

### To-dos

- [ ] Create api/app/modules/request_amazon/ directory structure and package __init__.py files
- [ ] Create schemas.py with RequestAmazonInput and RequestAmazonResponse Pydantic models
- [ ] Create services.py with fetch_amazon_page async function using httpx.AsyncClient
- [ ] Create routes.py with FastAPI router and POST /fetch endpoint
- [ ] Create repositories.py with placeholder RequestAmazonRepository class
- [ ] Create models.py placeholder file
- [ ] Add httpx to requirements.txt
- [ ] Update main.py to include the request_amazon router