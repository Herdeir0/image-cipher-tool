import numpy as np
from PIL import Image

def load_image(path):
    """
    Load image and automatically:
    - Resize to 256x256
    - Convert to grayscale
    """
    img = Image.open(path)

    # Convert to grayscale
    img = img.convert("L")

    # Resize to 256x256
    img = img.convert("L").resize((256, 256), Image.Resampling.LANCZOS)
    pixels = np.array(img)
    pixels[-1, :] = np.arange(256, dtype=np.uint8)
    img = Image.fromarray(pixels)

    return img

def get_pixel_value(img, x, y):
    """
    Get grayscale value at coordinate (x, y)
    """
    return img.getpixel((x, y))

def force_full_grayscale(img):
    """
    Ensures all grayscale values 0–255 exist
    by embedding a calibration strip.
    """

    img = img.convert("L").resize((256, 256), Image.Resampling.LANCZOS)

    pixels = np.array(img)

    # Create calibration strip (1x256)
    strip = np.arange(256, dtype=np.uint8)

    # Insert at bottom row
    pixels[-1, :] = strip

    return Image.fromarray(pixels)