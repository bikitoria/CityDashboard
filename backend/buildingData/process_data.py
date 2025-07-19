def simplify_building(building):
    try:
        geom = building.get("the_geom")
        if not geom or geom.get("type") != "MultiPolygon":
            raise ValueError("Missing or invalid 'the_geom'")

        coords = geom.get("coordinates")
        if not coords or not isinstance(coords, list):
            raise ValueError("Invalid coordinates")

        return {
            "id": building.get("building_id"),
            "name": building.get("building_name"),
            "height": float(building.get("height", 10)),  # default height if missing
            "coordinates": coords,
        }
    except Exception as e:
        print(f"Error simplifying building: {e}")
        return None
