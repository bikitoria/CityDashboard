import requests

BASE_URL = "https://data.calgary.ca/resource/uc4c-6kbd.json"

buildings_data_list = []

def simplify_building(building):
    try:
        mp = building.get("multipolygon")

        if not mp or mp.get("type") != "MultiPolygon":
            raise ValueError("Missing or invalid multipolygon")

        coords = mp.get("coordinates")
        if not coords or not isinstance(coords, list):
            raise ValueError("Invalid coordinates")

        return {
            "id": building.get("bldg_code"),
            "desc": building.get("bldg_code_desc"),
            "area": float(building.get("shape__area", 0)),
            "length": float(building.get("shape__length", 0)),
            "coordinates": coords
        }

    except Exception as e:
        print(f"Error simplifying building: {e}")
        return None

def load_all_buildings():
    global buildings_data_list

    params = {
        "$limit": 500
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        raw_buildings = response.json()

        buildings_data_list = [b for b in (simplify_building(b) for b in raw_buildings) if b]

        print(f"Loaded {len(buildings_data_list)} buildings")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

load_all_buildings()