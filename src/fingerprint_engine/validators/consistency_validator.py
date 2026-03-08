def validate(fp: dict) -> bool:
    """Ensures fingerprint doesn't mix incompatible traits."""
    platform = fp.get("platform", "").lower()
    ua = fp.get("userAgent", "").lower()

    if "win" in platform and "mac" in ua:
        return False
    if "mac" in platform and "win" in ua:
        return False
    if "linux" in platform and ("win" in ua or "mac" in ua):
        return False

    return True
