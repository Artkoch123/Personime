from xml.etree.ElementInclude import include

import requests

def get_character_image(character_name, anime_name):
    url = "https://kitsu.io/api/edge/characters"

    params = {
        "filter[name]": character_name,
        "page[limit]": 1,
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()["data"]

    if not data:
        return None

    image = data[0].get("attributes", {}).get("image")
    return image["original"] if image else None