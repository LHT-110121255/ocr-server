import base64
import os
import re

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ocr_engine import OcrEngine

app = FastAPI(title="SpatialPay OCR Server")
engine = OcrEngine()

MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB


class OcrRequest(BaseModel):
    image_base64: str
    mime_type: str = "image/jpeg"


class OcrResponse(BaseModel):
    success: bool
    raw_text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ocr", response_model=OcrResponse)
async def ocr(body: OcrRequest):
    if not body.image_base64:
        raise HTTPException(status_code=400, detail="image_base64 is required")

    try:
        image_bytes = base64.b64decode(body.image_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64")

    if len(image_bytes) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=413, detail="Image too large (max 10MB)")

    try:
        raw_text = engine.recognize(image_bytes)
        if not raw_text.strip():
            return OcrResponse(success=False, raw_text="")
        return OcrResponse(success=True, raw_text=raw_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
