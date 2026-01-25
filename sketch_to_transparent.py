#!/usr/bin/env python3
"""
sketch_to_transparent.py

Converts images from res/images/ to res/sketch/ by treating luminance as alpha:
- white (255) -> alpha 0 (transparent)
- black (0)   -> alpha 255 (opaque)
RGB is set to pure black.

Preserves folder structure from res/images/ into res/sketch/.

Processes only images that do not yet exist in res/sketch/.

At the end, automatically adds, commits, and pushes changes to Git.

Usage:
    python3 sketch_to_transparent.py [--invert]
"""

import argparse
import os
import subprocess
from pathlib import Path
from PIL import Image, ImageOps


def convert(inp: Path, out: Path, invert: bool = False) -> None:
    gray = Image.open(inp).convert("L")
    if invert:
        gray = ImageOps.invert(gray)

    alpha = ImageOps.invert(gray)
    rgba = Image.new("RGBA", gray.size, (0, 0, 0, 0))
    rgba.putalpha(alpha)

    out.parent.mkdir(parents=True, exist_ok=True)
    rgba.save(out, format="PNG")


def git_commit_and_push(modified_files: list[Path]) -> None:
    if not modified_files:
        print("No new images processed. Nothing to commit.")
        return

    try:
        # Stage only the modified files
        for file_path in modified_files:
            subprocess.run(["git", "add", str(file_path)], check=True)

        # Build commit message
        rel_paths = [str(path.relative_to(Path.cwd())) for path in modified_files]
        commit_msg = "Processed and added sketches:\n" + "\n".join(rel_paths)

        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Changes committed and pushed.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert white background to transparent alpha.")
    parser.add_argument(
        "--invert",
        action="store_true",
        help="Invert input first (useful for white-on-black sketches)",
    )
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    images_dir = base_dir / "res" / "images"
    sketch_dir = base_dir / "res" / "sketch"

    supported_exts = {".png", ".jpg", ".jpeg", ".bmp"}

    processed = []

    for img_path in images_dir.rglob("*"):
        if img_path.suffix.lower() not in supported_exts:
            continue

        relative_path = img_path.relative_to(images_dir)
        sketch_path = sketch_dir / relative_path.with_suffix(".png")

        if sketch_path.exists():
            continue

        print(f"Processing: {img_path} -> {sketch_path}")
        convert(img_path, sketch_path, invert=args.invert)
        processed.append(sketch_path)

    git_commit_and_push(processed)


if __name__ == "__main__":
    main()

