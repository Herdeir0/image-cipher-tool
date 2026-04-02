from mapping import value_to_char, generate_mapping
from image_utils import get_pixel_value

def decode_coordinates(img, coords):
    mapping = generate_mapping()
    decoded = ""

    for x, y in coords:
        value = get_pixel_value(img, x, y)
        decoded += value_to_char(value, mapping)

    return decoded