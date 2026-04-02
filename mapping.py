from config import CHARSET

def generate_mapping():
    range_size = 256 // len(CHARSET)
    mapping = {}

    for i, char in enumerate(CHARSET):
        start = i * range_size
        end = start + range_size - 1
        mapping[(start, end)] = char

    return mapping


def value_to_char(value, mapping):
    for (start, end), char in mapping.items():
        if start <= value <= end:
            return char
    return "?"


def char_to_value(char, mapping):
    for (start, end), c in mapping.items():
        if c == char:
            return (start + end) // 2
    raise ValueError(f"Character {char} not in mapping")