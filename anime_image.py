from tarfile import data_filter

import requests

ANILIST_URL = "https://graphql.anilist.co"


def get_character_image(character_name: str) -> str | None:
    query = """
    query ($search: String!) {
        Page(page: 1, perPage: 5) {
            characters(search: $search){
                id
                name {
                    full
                    native
                }
                image {
                    large
                    medium
                }
            }
        }
    }
    """

    variables = {
        "search": character_name
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.post(
            ANILIST_URL,
            json={
                "query": query,
                "variables": variables
            },
            headers=headers,
            timeout=10
        )

        print(response.text)
        response.raise_for_status()


        data = response.json()
        print(data)
        characters = data["data"]["Page"]["characters"]

        if not characters:
            return None

        character = characters[0]

        return {
            "image": character["image"]["large"],
        }
    except (requests.RequestException, TypeError) as e:
        print(f"Ошибка AniList: {e}")
        return None