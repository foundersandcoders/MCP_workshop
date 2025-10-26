import requests


def get_coordinates(city: str) -> dict:
    """
    Fetch geographical coordinates for a city using Open-Meteo Geocoding API
    Args:
        city (str): Name of the city
    Returns:
        Dictionary with longitude and latitude
    """
    base_url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {"name": city, "count": 1}

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {"longitude": result["longitude"], "latitude": result["latitude"]}
        else:
            return {"error": "City not found"}
    except requests.RequestException as e:
        return {"error": f"Failed to fetch coordinates: {str(e)}"}


def get_weather(lat: float, long: float) -> dict:
    """
    Fetch current weather data for a Geographical coordinates using Open-Meteo API
    Args:
        Longitude and Latitude
    Returns:
        Dictionary with weather information
    """
    base_url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": long,
        "current": "temperature_2m",
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            "temperature": data["current"]["temperature_2m"],
            "units": data["current_units"]["temperature_2m"],
        }
    except requests.RequestException as e:
        return {"error": f"Failed to fetch weather: {str(e)}"}
