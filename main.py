import argparse

from image_utils import load_image
from encoder import encode_message
from decoder import decode_coordinates


def find_image_in_assets():
    import os

    ASSETS_FOLDER = "assets"
    VALID_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")

    files = os.listdir(ASSETS_FOLDER)

    images = [
        f for f in files
        if f.lower().endswith(VALID_EXTENSIONS)
    ]

    if len(images) == 0:
        raise FileNotFoundError("Error! No images found in assets folder.")

    if len(images) > 1:
        raise ValueError("Error! Multiple images found in assets folder.")

    return os.path.join(ASSETS_FOLDER, images[0])


def main():
    parser = argparse.ArgumentParser(description="Image Cryptography Tool")

    parser.add_argument("mode", choices=["encode", "decode"])
    parser.add_argument("data", help="Message or coordinates depending on mode")

    args = parser.parse_args()

    image_path = find_image_in_assets()
    print(f"Using image: {image_path}")

    img = load_image(image_path)

    if args.mode == "encode":
        coords = encode_message(img, args.data)

        coord_string = ";".join(f"{x},{y}" for x, y in coords)
        print(coord_string)

    elif args.mode == "decode":
        coords = [
            tuple(map(int, p.split(",")))
            for p in args.data.split(";")
        ]

        message = decode_coordinates(img, coords)
        print(message)


if __name__ == "__main__":
    main()