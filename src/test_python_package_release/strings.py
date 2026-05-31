def reverse_string(s: str) -> str:
    return s[::-1]


def snake_to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


def count_words(s: str) -> int:
    return len(s.split()) if s.strip() else 0


def camel_to_snake(s: str) -> str:
    result = []
    for i, ch in enumerate(s):
        if ch.isupper() and i > 0:
            result.append("_")
        result.append(ch.lower())
    return "".join(result)


def truncate(s: str, max_length: int, suffix: str = "...") -> str:
    if len(s) <= max_length:
        return s
    return s[: max_length - len(suffix)] + suffix
