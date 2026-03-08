import requests

def get_location_for_ip(ip: str):
    """
    Fetch geolocation details for an IP.
    """
    try:
        if not ip:
            return {"country": "US", "timezone": "America/New_York"}
        res = requests.get(f"https://ipapi.co/{ip}/json/", timeout=2)
        data = res.json()
        if "error" in data:
            return {"country": "US", "timezone": "America/New_York"}
        return {
            "country": data.get("country_code", "US"),
            "timezone": data.get("timezone", "America/New_York"),
            "city": data.get("city", "New York")
        }
    except:
        return {"country": "US", "timezone": "America/New_York"}
