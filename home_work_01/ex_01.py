def domain_name(url: str) -> str:
    return url.replace("www.", "").replace("https://", "").replace("http://", "").split(".")[0]
