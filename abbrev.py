def abbrev_name(name: str) -> str:
    name_parts = name.split()
    last_name = name_parts[0]
    initials = ''.join([f'{part[0]}.' for part in name_parts[1:]])
    return f'{last_name} {initials}'

