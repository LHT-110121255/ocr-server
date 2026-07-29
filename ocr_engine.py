import io
import logging
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR

logging.getLogger("ppocr").setLevel(logging.ERROR)
logging.getLogger("paddleocr").setLevel(logging.ERROR)
logging.getLogger("paddle").setLevel(logging.ERROR)


class OcrEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        print("[OCR] Initializing PaddleOCR...")
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang="ch",
        )
        print("[OCR] PaddleOCR ready")

    def recognize(self, image_bytes: bytes) -> str:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(image)
        result = self.ocr.ocr(img_array, cls=True)
        if not result:
            return ""
        lines = []
        for page in result:
            for line in page:
                text = line[1][0].strip()
                if text:
                    lines.append(text)
        return "\n".join(lines)
