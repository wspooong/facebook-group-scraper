def extract_digits(input: str) -> int:
    """Extract digits from string."""
    return int("".join([x for x in input if x.isdigit()]))
