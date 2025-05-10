import requests
from app.utils import get_env_var

def find_best_food_nearby(query, location="12.9716,77.5946", radius=2000):
    api_key = get_env_var("GOOGLE_API_KEY")
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "location": location,
        "radius": radius,
        "key": api_key
    }
    response = requests.get(url, params=params)
    results = response.json().get("results", [])
    if results:
        top = results[0]
        return f"{top['name']} - {top['formatted_address']}"
    return "No food places found nearby."