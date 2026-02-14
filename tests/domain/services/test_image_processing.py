from PIL import Image

from app.domain.services.image_processing import to_transparent


def test_white_background_becomes_transparent():
    white = Image.new("L", (10, 10), 255)
    result = to_transparent(white)
    assert result.mode == "RGBA"
    assert result.getpixel((5, 5))[3] == 0


def test_black_foreground_becomes_opaque():
    black = Image.new("L", (10, 10), 0)
    result = to_transparent(black)
    assert result.getpixel((5, 5))[3] == 255


def test_invert_flips_transparency():
    white = Image.new("L", (10, 10), 255)
    result = to_transparent(white, invert=True)
    assert result.getpixel((5, 5))[3] == 255


def test_below_threshold_becomes_fully_transparent():
    # Very light gray — just barely visible, should be clipped to transparent
    almost_white = Image.new("L", (10, 10), 250)
    result = to_transparent(almost_white)
    assert result.getpixel((5, 5))[3] == 0
