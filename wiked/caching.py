import json
import os
from os import path

CACHE_FILE_PREFIX = "cache_"
CACHE_FOLDER = "cache"
JKU_CS_PROFS_CACHE_FILE = "cache_jku_cs_profs.txt"


def save_contributions(contributions: list, ip_range: str):
    name = __ip_file_name(ip_range)
    with open(path.join(__cache_folder(), name), "w") as outfile:
        json.dump(contributions, outfile, indent=2)


def load_contributions(ip_range: str) -> list | None:
    name = __ip_file_name(ip_range)
    try:
        file = open(path.join(__cache_folder(), name), "r")
        contributions = json.loads(file.read())
        file.close()
        return contributions
    except FileNotFoundError:
        return None


def save_professors(prof_names: list):
    with open(path.join(__cache_folder(), JKU_CS_PROFS_CACHE_FILE), "w", encoding="utf-8") as file:
        for name in prof_names:
            file.write(name + "\n")


def load_professors() -> list | None:
    try:
        file = open(path.join(__cache_folder(), JKU_CS_PROFS_CACHE_FILE), "r")
        prof_names = file.readlines()
        prof_names = [name.strip() for name in prof_names]
        file.close()
        return prof_names
    except FileNotFoundError:
        return None


def __ip_file_name(ip_range: str) -> str:
    return CACHE_FILE_PREFIX + ip_range.replace("/", "_") + ".json"


def __cache_folder() -> str:
    if not os.path.exists(CACHE_FOLDER):
        os.makedirs(CACHE_FOLDER)

    return CACHE_FOLDER
