def reverse_string(s: str) -> str:
    return s[::-1]


def snake_to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])
