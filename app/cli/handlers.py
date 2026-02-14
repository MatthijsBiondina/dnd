from pathlib import Path

from PIL import Image

from app.domain.models.monster import Monster, MonsterStats
from app.domain.services.image_processing import to_transparent
from app.domain.services.scale_monster import scale_monster

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp"}


def needs_processing(img_path: Path, sketch_path: Path) -> bool:
    if not sketch_path.exists():
        return True
    return img_path.stat().st_mtime > sketch_path.stat().st_mtime


def process_images(
    images_dir: Path, sketch_dir: Path, force: bool = False, invert: bool = False
) -> list[Path]:
    processed = []
    for img_path in images_dir.rglob("*"):
        if img_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        relative_path = img_path.relative_to(images_dir)
        sketch_path = sketch_dir / relative_path.with_suffix(".png")

        if not force and not needs_processing(img_path, sketch_path):
            continue

        image = Image.open(img_path)
        result = to_transparent(image, invert=invert)
        sketch_path.parent.mkdir(parents=True, exist_ok=True)
        result.save(sketch_path, format="PNG")
        processed.append(sketch_path)

    return processed


def handle_scale_monster():
    print("Enter monster stats:\n")
    cr = float(input("  Challenge Rating: "))
    ac = int(input("  Armor Class: "))
    hp = int(input("  Hit Points: "))
    atk = int(input("  Attack Bonus: "))
    damage = int(input("  Damage/Round: "))
    save_dc = input("  Save DC (or Enter to skip): ")
    save_dc = int(save_dc) if save_dc else None

    monster = Monster(
        stats=MonsterStats(
            challenge_rating=cr,
            armor_class=ac,
            hit_points=hp,
            attack_bonus=atk,
            damage=damage,
            save_dc=save_dc,
        )
    )

    target_cr = float(input("\n  Target CR: "))
    scaled = scale_monster(monster, target_cr)

    print(f"\n  Scaled to CR {scaled.cr}:")
    print(f"    AC:         {scaled.ac}")
    print(f"    HP:         {scaled.hp}")
    print(f"    Attack:     +{scaled.atk_bonus}")
    print(f"    Damage:     {scaled.damage}")
    print(f"    Save DC:    {scaled.save_dc}")
    print(f"    XP:         {scaled.xp}")

    input("\nPress Enter to continue...")
