import requests

def test_proxy(proxy_type: str, host: str, port: int, username: str = None, password: str = None) -> bool:
    try:
        url = f"{proxy_type}://"
        if username and password:
            url += f"{username}:{password}@"
        url += f"{host}:{port}"

        proxies = {
            "http": url,
            "https": url,
        }

        resp = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        print(f"Proxy test failed: {e}")
        return False
