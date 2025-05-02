import weatherapi as w
from weatherapi.rest import ApiException as exc

from app.config import WEATHER_API_KEY, WEATHER_SYSTEM_INSTRUCTION
from app.utils.helpers import synch_call_ollama_api
from app.utils.logger import log

conf = w.Configuration()
conf.api_key["key"] = WEATHER_API_KEY
w_api = w.APIsApi(w.ApiClient(conf))


def get_weather_info(prompt: str) -> str:
    """
    Extracts weather-related information from the prompt.
    """
    messages = [
        ("system", WEATHER_SYSTEM_INSTRUCTION),
        ("user", prompt),
    ]
    # Call the Ollama API to get the location information
    resp = synch_call_ollama_api(messages)
    log("INFO", f"Response from Weather Filter: {resp}")
    if resp != "Unknown":
        # Call the weather API to get the weather information for the location
        weather_info = load_climate_info(resp)
        return weather_info
    else:
        return ""


def format_forecast(forecast):
    # Formats the weather forecast data for display
    days = forecast["forecast"]["forecastday"]
    if not days:
        return "No forecast data available."

    date_taken = days[0]["date"]
    location = forecast["location"]["name"]
    formatted_forecast = f"Weather Forecast for {date_taken} in {location}:\n"
    for day in days:
        date = day["date"]
        day_data = day["day"]
        condition = day_data["condition"]["text"]
        avg_temp = day_data["avgtemp_c"]
        max_temp = day_data["maxtemp_c"]
        min_temp = day_data["mintemp_c"]
        humidity = day_data["avghumidity"]
        precipitation = day_data["totalprecip_mm"]
        rain_chance = day_data["daily_chance_of_rain"]

        formatted_forecast += (
            f"**Date:** {date}\n"
            f"**Condition:** {condition}\n"
            f"**Avg Temp:** {avg_temp}°C\n"
            f"**Max Temp:** {max_temp}°C\n"
            f"**Min Temp:** {min_temp}°C\n"
            f"**Humidity:** {humidity}%\n"
            f"**Precipitation:** {precipitation}mm\n"
            f"**Chance of Rain:** {rain_chance}%\n\n"
        )

    return formatted_forecast


def load_climate_info(query: str) -> str:
    """
    Loads climate information based on the query.
    """
    # Calls weather api for weather forecast
    # q = "Marsabit"
    try:
        log("INFO", f"Loading climate info for query: {query}")
        forecast = w_api.forecast_weather(
            q=query,
            days=3,
        )
        f = format_forecast(forecast)
        return f
    except exc as e:
        log("ERROR", f"Exception in load_climate_info: {e}\nQuery: {query}")
        return ""
