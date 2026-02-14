#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

from PIL import Image

from app.domain.services.image_processing import to_transparent

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp"}


def convert(inp: Path, out: Path, invert: bool = False) -> None:
    image = Image.open(inp)
    result = to_transparent(image, invert=invert)
    out.parent.mkdir(parents=True, exist_ok=True)
    result.save(out, format="PNG")


def needs_processing(img_path: Path, sketch_path: Path) -> bool:
    if not sketch_path.exists():
        return True
    return img_path.stat().st_mtime > sketch_path.stat().st_mtime


def git_commit_and_push(modified_files: list[Path]) -> None:
    if not modified_files:
        print("No new images processed. Nothing to commit.")
        return
    try:
        for file_path in modified_files:
            subprocess.run(["git", "add", str(file_path)], check=True)
        rel_paths = [str(path.relative_to(Path.cwd())) for path in modified_files]
        commit_msg = "Processed and added sketches:\n" + "\n".join(rel_paths)
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Changes committed and pushed.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert white background to transparent alpha.")
    parser.add_argument("--invert", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    images_dir = base_dir / "res" / "images"
    sketch_dir = base_dir / "res" / "sketch"

    processed = []
    for img_path in images_dir.rglob("*"):
        if img_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        relative_path = img_path.relative_to(images_dir)
        sketch_path = sketch_dir / relative_path.with_suffix(".png")
        if not args.force and not needs_processing(img_path, sketch_path):
            continue
        print(f"Processing: {img_path} -> {sketch_path}")
        convert(img_path, sketch_path, invert=args.invert)
        processed.append(sketch_path)

    git_commit_and_push(processed)


if __name__ == "__main__":
    main()
