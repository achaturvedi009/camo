import requests
import json
import packaging.version

res = requests.get("https://pypi.org/pypi/camoufox/json")
releases = list(res.json().get("releases", {}).keys())

sorted_versions = sorted(releases, key=packaging.version.parse, reverse=True)
print(sorted_versions[:10])
