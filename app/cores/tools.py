"""City information retrieval tools."""

import logging
import os

import httpx
from agents import function_tool
from dotenv import load_dotenv

from app.schemas.schemas import CityInput
from app.utils.general import get_lat_long

# Setup logger
logger = logging.getLogger("cityassistant.tools")

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TIMEZONEDB_API_KEY = os.getenv("TIMEZONEDB_API_KEY")


@function_tool
async def weather_tool(city_input: CityInput) -> str:
    """
    Get the current weather for a city using OpenWeatherMap API.

    :param city_input: CityInput with the city name.
    :return: Weather description string, or error message if unavailable.
    """
    city = city_input.city
    lat, lon = await get_lat_long(city)
    if lat is None or lon is None:
        logger.warning(f"WeatherTool: Coordinates not found for {city}")
        return f"Sorry, I couldn't find the coordinates for {city}."

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].capitalize()
            logger.info(f"WeatherTool: Got weather for {city} - {temp}°C, {desc}")
            return f"The weather in {city} is {temp}°C with {desc}."
    except Exception as e:
        logger.error(f"WeatherTool error for {city}: {e}")
        return "Weather information is currently unavailable."


@function_tool
async def time_tool(city_input: CityInput) -> str:
    """
    Get the current local time in a city using TimeZoneDB API.

    :param city_input: CityInput with the city name.
    :return: Time as 'HH:MM', or error message if unavailable.
    """
    city = city_input.city
    lat, lon = await get_lat_long(city)
    if lat is None or lon is None:
        logger.warning(f"TimeTool: Coordinates not found for {city}")
        return f"Sorry, I couldn't find the coordinates for {city}."

    tz_url = (
        f"http://api.timezonedb.com/v2.1/get-time-zone"
        f"?key={TIMEZONEDB_API_KEY}&format=json&by=position&lat={lat}&lng={lon}"
    )
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            tz_resp = await client.get(tz_url)
            tz_resp.raise_for_status()
            tz_data = tz_resp.json()
            formatted = tz_data.get("formatted")
            if formatted and len(formatted) >= 16:
                logger.info(f"TimeTool: Got local time for {city} - {formatted[11:16]}")
                return f"The local time in {city} is {formatted[11:16]}."
            logger.warning(f"TimeTool: Time not found in response for {city}")
            return "Time information is currently unavailable."
    except Exception as error:
        logger.error(f"TimeTool error for {city}: {error}")
        return "Time information is currently unavailable."


@function_tool
async def city_facts_tool(city_input: CityInput) -> str:
    """
    Get a brief fact about a city using Wikipedia API.

    :param city_input: CityInput with the city name.
    :return: One-sentence fact about the city, or error message if unavailable.
    """
    city = city_input.city
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{city.replace(' ', '_')}"
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            desc = data.get("extract")
            if desc:
                summary = desc.split(".")[0] + "."
                logger.info(f"CityFactsTool: Found fact for {city}")
                return summary
            logger.warning(f"CityFactsTool: No fact found for {city}")
            return f"No facts found for {city}."
    except Exception as error:
        logger.error(f"CityFactsTool error for {city}: {error}")
        return "City facts are currently unavailable."
