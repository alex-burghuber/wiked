import json
import os
from os import path

CACHE_FILE_PREFIX = "cache_"
CACHE_FOLDER = "cache"


def save_contributions(contributions: list, ip_range: str):
    name = __file_name(ip_range)
    with open(path.join(__cache_folder(), name), "w") as outfile:
        json.dump(contributions, outfile, indent=2)


def load_contributions(ip_range: str) -> list | None:
    name = __file_name(ip_range)
    try:
        file = open(path.join(__cache_folder(), name), "r")
        contributions = json.loads(file.read())
        file.close()
        return contributions
    except FileNotFoundError:
        return None


def __file_name(ip_range: str) -> str:
    return CACHE_FILE_PREFIX + ip_range.replace("/", "_") + ".json"


def __cache_folder() -> str:
    if not os.path.exists(CACHE_FOLDER):
        os.makedirs(CACHE_FOLDER)

    return CACHE_FOLDER
