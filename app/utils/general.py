"""General utility functions."""

import os
import urllib.parse

from dotenv import load_dotenv
import httpx

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


async def get_lat_long(city: str) -> tuple[float | None, float | None]:
    """
    Get latitude and longitude for a given city name using OpenWeather geocoding.

    :param city: City name
    :return: Tuple (latitude, longitude) or (None, None) if not found
    """
    city_param = urllib.parse.quote(city)
    url = (
        f"http://api.openweathermap.org/geo/1.0/direct"
        f"?q={city_param}&limit=1&appid={OPENWEATHER_API_KEY}"
    )
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            if data:
                lat = data[0].get("lat")
                lon = data[0].get("lon")
                return lat, lon
    except Exception:
        pass
    return None, None
