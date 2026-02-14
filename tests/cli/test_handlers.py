from app.cli.handlers import process_images


def test_process_images_skips_up_to_date(tmp_path):
    images_dir = tmp_path / "images"
    sketch_dir = tmp_path / "sketch"
    images_dir.mkdir()
    sketch_dir.mkdir()

    # Create a source image and a newer sketch (already processed)
    src = images_dir / "test.png"
    dst = sketch_dir / "test.png"
    src.write_bytes(b"fake image")
    dst.write_bytes(b"fake sketch")

    # Make sketch newer than source
    dst.touch()

    results = process_images(images_dir, sketch_dir, force=False)
    assert len(results) == 0


def test_process_images_processes_new_file(tmp_path):
    images_dir = tmp_path / "images"
    sketch_dir = tmp_path / "sketch"
    images_dir.mkdir()
    sketch_dir.mkdir()

    # Create a small valid white PNG
    from PIL import Image

    src = images_dir / "test.png"
    Image.new("L", (10, 10), 255).save(src)

    results = process_images(images_dir, sketch_dir, force=False)
    assert len(results) == 1
    assert (sketch_dir / "test.png").exists()
