# app/domain/services/image_processing.py

import numpy as np
from PIL import Image, ImageOps


def to_transparent(
    image: Image.Image, invert: bool = False, threshold: float = 0.10
) -> Image.Image:
    gray = image.convert("L")
    if invert:
        gray = ImageOps.invert(gray)

    alpha = np.array(ImageOps.invert(gray), dtype=np.float64) / 255.0

    mask = alpha >= threshold
    alpha[~mask] = 0.0
    if mask.any():
        lo = alpha[mask].min()
        hi = alpha[mask].max()
        if hi > lo:
            alpha[mask] = (alpha[mask] - lo) / (hi - lo)
        else:
            alpha[mask] = 1.0

    alpha_img = Image.fromarray((alpha * 255).astype(np.uint8), mode="L")
    rgba = Image.new("RGBA", gray.size, (0, 0, 0, 0))
    rgba.putalpha(alpha_img)
    return rgba
