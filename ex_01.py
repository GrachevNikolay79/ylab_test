def domain_name(url: str) -> str:
    parts_url = url.split('.', 2)
    c = parts_url[0][-1]
    if c == 'w' or c == 'W':
        return parts_url[1]
    parts_url = parts_url[0].split('//')
    return parts_url[1]
