def normalize_phone(phone: str) -> str:
    return "".join(character for character in phone if character.isdigit())
