from typing import Optional

from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.head("/health")
async def health_check():
    """Health check endpoint for monitoring services like UptimeRobot"""
    return Response(status_code=200)