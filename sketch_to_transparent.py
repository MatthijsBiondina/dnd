#!/usr/bin/env python3
"""
white_to_transparent.py

Treat luminance as alpha:
- white (255) -> alpha 0 (transparent)
- black (0)   -> alpha 255 (opaque)
RGB is set to pure black.

Requires: pillow
Install:  python3 -m pip install --user pillow
"""

import argparse
from PIL import Image, ImageOps


def convert(inp: str, out: str, invert: bool = False) -> None:
    # Load and convert to grayscale
    gray = Image.open(inp).convert("L")
    if invert:
        gray = ImageOps.invert(gray)

    # Alpha = 255 - gray (so white -> 0, black -> 255)
    alpha = ImageOps.invert(gray)

    # Create RGBA: black RGB + computed alpha
    rgba = Image.new("RGBA", gray.size, (0, 0, 0, 0))
    rgba.putalpha(alpha)

    rgba.save(out, format="PNG")


def main() -> None:
    p = argparse.ArgumentParser(description="Convert white background to transparent alpha.")
    p.add_argument("input", help="Input image (png/jpg/etc.)")
    p.add_argument("output", help="Output PNG (RGBA)")
    p.add_argument(
        "--invert",
        action="store_true",
        help="Invert input first (useful if your lines are white-on-black)",
    )
    args = p.parse_args()
    convert(args.input, args.output, invert=args.invert)


if __name__ == "__main__":
    main()

