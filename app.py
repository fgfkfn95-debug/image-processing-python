from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


@dataclass
class ProcessingOptions:
    grayscale: bool = False
    resize_width: Optional[int] = None
    resize_height: Optional[int] = None
    rotate: int = 0
    brightness: float = 1.0
    contrast: float = 1.0
    blur: float = 0.0
    sharpen: bool = False
    edge: bool = False
    threshold: Optional[int] = None


class ImageProcessor:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_image(self, image_path: str | Path) -> Image.Image:
        image = Image.open(image_path)
        if image.mode not in {"RGB", "L", "RGBA", "CMYK"}:
            image = image.convert("RGB")
        return image.convert("RGB")

    def save_image(self, image: Image.Image, output_name: str) -> Path:
        path = self.output_dir / output_name
        image.save(path)
        return path

    def _resize_image(self, image: Image.Image, width: Optional[int], height: Optional[int]) -> Image.Image:
        if width is None and height is None:
            return image

        if width is not None and height is not None:
            return image.resize((width, height), Image.Resampling.LANCZOS)

        original_width, original_height = image.size
        if width is None:
            ratio = height / original_height
            width = max(1, int(original_width * ratio))
        else:
            ratio = width / original_width
            height = max(1, int(original_height * ratio))
        return image.resize((width, height), Image.Resampling.LANCZOS)

    def process(self, image: Image.Image, options: ProcessingOptions) -> Image.Image:
        processed = image.copy()

        if options.grayscale:
            processed = ImageOps.grayscale(processed).convert("RGB")

        if options.resize_width is not None or options.resize_height is not None:
            processed = self._resize_image(processed, options.resize_width, options.resize_height)

        if options.rotate not in (0, 360):
            processed = processed.rotate(options.rotate, expand=True, fillcolor=(255, 255, 255))

        if options.brightness != 1.0:
            processed = ImageEnhance.Brightness(processed).enhance(options.brightness)

        if options.contrast != 1.0:
            processed = ImageEnhance.Contrast(processed).enhance(options.contrast)

        if options.blur > 0:
            processed = processed.filter(ImageFilter.GaussianBlur(radius=options.blur))

        if options.sharpen:
            processed = processed.filter(ImageFilter.SHARPEN)

        if options.edge:
            grayscale = np.array(processed.convert("L"))
            edges = cv2.Canny(grayscale, 100, 200)
            processed = Image.fromarray(edges).convert("RGB")

        if options.threshold is not None:
            gray = np.array(processed.convert("L"))
            _, thresholded = cv2.threshold(gray, options.threshold, 255, cv2.THRESH_BINARY)
            processed = Image.fromarray(thresholded)

        return processed

    def process_file(
        self,
        input_path: str | Path,
        output_name: str,
        options: ProcessingOptions,
    ) -> Path:
        image = self.load_image(input_path)
        processed = self.process(image, options)
        return self.save_image(processed, output_name)
