import requests

SEARCH_TERM = "building"
API_URL = f"https://data.calgary.ca/api/views.json?limit=1000"

try:
    response = requests.get(API_URL)
    response.raise_for_status()
    datasets = response.json()

    for entry in datasets:
        if SEARCH_TERM.lower() in entry.get("name", "").lower():
            print("Title:", entry.get("name"))
            print("Description:", entry.get("description", "No description"))
            print("Link:", f"https://data.calgary.ca/d/{entry.get('id')}")
            print("---")

except requests.RequestException as e:
    print("Error fetching data:", e)