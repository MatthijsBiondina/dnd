# app/cli/menu.py

import os
from pathlib import Path

from app.cli.handlers import handle_scale_monster, process_images


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def handle_process_images():
    base_dir = Path(__file__).parent.parent.parent
    images_dir = base_dir / "res" / "images"
    sketch_dir = base_dir / "res" / "sketch"

    force = input("Force reprocess all? (y/N) > ").lower() == "y"
    invert = input("Invert colors? (y/N) > ").lower() == "y"

    processed = process_images(images_dir, sketch_dir, force=force, invert=invert)
    if processed:
        for path in processed:
            print(f"  Processed: {path}")
        print(f"\n✅ {len(processed)} images processed.")
    else:
        print("No new images to process.")

    input("\nPress Enter to continue...")


def main():
    # in app/cli/menu.py

    # in main()
    actions = {
        "1": ("Scale monster", handle_scale_monster),
        "2": ("Process sketch images", handle_process_images),
        "0": ("Exit", None),
    }

    while True:
        clear()
        print("=== Iradeh Campaign Tools ===\n")
        for key, (label, _) in actions.items():
            print(f"  {key}. {label}")

        choice = input("\n> ")
        if choice == "0":
            break
        if choice in actions:
            _, handler = actions[choice]
            handler()
        else:
            input("Invalid choice. Press Enter to continue...")


if __name__ == "__main__":
    main()
