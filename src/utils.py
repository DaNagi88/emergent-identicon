import json
from urllib.request import urlopen


def get_github_id(login_name):
    url = f"https://api.github.com/users/{login_name}"
    with urlopen(url) as webfile:
        string = webfile.read().decode()
    user_info = json.loads(string)
    user_id = user_info.get("id")

    return user_id
