import random
from mapping import char_to_value, generate_mapping
from config import IMAGE_SIZE

def find_coordinates_for_value(img, target_value):
    pixels = img.load()
    width, height = IMAGE_SIZE

    matches = []

    for x in range(width):
        for y in range(height):
            if pixels[x, y] == target_value:
                matches.append((x, y))

    if not matches:
        raise ValueError(f"No pixel found for value {target_value}")

    return random.choice(matches)


def encode_message(img, message):
    mapping = generate_mapping()
    coords = []

    for char in message:
        char = char.lower()

        value = char_to_value(char, mapping)
        coord = find_coordinates_for_value(img, value)

        coords.append(coord)

    return coords