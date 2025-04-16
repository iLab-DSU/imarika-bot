import asyncio
import random
import time

import streamlit as st
import weatherapi as w
import websockets
from weatherapi.rest import ApiException as exc

from app.config import WEATHER_API_KEY, WS_ENDPOINT
from chain.memory import MemoryManager

conf = w.Configuration()
conf.api_key["key"] = WEATHER_API_KEY
w_api = w.APIsApi(w.ApiClient(conf))


def init_session():
    # Initialize session state variables if they don't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_activity" not in st.session_state:
        st.session_state.last_activity = time.time()
    if "memory" not in st.session_state:
        st.session_state.memory = MemoryManager()
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = random.randint(
            1, 2147483647
        )  # get a better replacement for this
    if "climate_set" not in st.session_state:
        st.session_state.climate_set = False


def get_user_id():
    # Returns the user ID from session state
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = random.randint(1, 2147483647)
    return st.session_state["user_id"]


def display_chat_history():
    # Displays all messages stored in session state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def clear_chat():
    # Clears the chat history and resets session state
    st.session_state.messages = []
    st.session_state.last_activity = time.time()
    st.session_state.climate_set = False
    if "memory" in st.session_state:
        st.session_state.memory.clear()
    else:
        st.session_state.memory = MemoryManager()


def check_inactivity(timeout: int = 600):
    # Clears chat if inactive for the specified timeout in seconds
    if time.time() - st.session_state.last_activity > timeout:
        clear_chat()


async def send_message(user_input: str, forecast: str = "") -> str:
    # Sends a message via WebSocket and returns the response
    try:
        async with websockets.connect(
            f"{WS_ENDPOINT}/{st.session_state['user_id']}"
        ) as websocket:
            await websocket.send(forecast + user_input)
            return await websocket.recv()
    except Exception as e:
        return f"Connection error: {e}"


async def api_send_message(user_input: str, id: int) -> str:
    # Sends a message via WebSocket and returns the response
    try:
        async with websockets.connect(f"{WS_ENDPOINT}/{id}") as websocket:
            await websocket.send(user_input)
            return await websocket.recv()
    except Exception as e:
        return f"Connection error: {e}"


def handle_user_input():
    # Handles user input, sends message, receives response, and updates session
    if user_input := st.chat_input("Enter your message..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        # Append climate information to the user input only once per session
        # to provide context for the assistant's responses. The `climate_set`
        # flag ensures this operation is not repeated unnecessarily.

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.memory.add_message(role="user", content=user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if not st.session_state.climate_set:
                    response = asyncio.run(
                        send_message(user_input, load_climate_info())
                    )
                    st.session_state.climate_set = True
                else:
                    response = asyncio.run(send_message(user_input))
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.memory.add_message(role="assistant", content=response)

        st.session_state.last_activity = time.time()


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


def load_climate_info():
    # Calls weather api for weather forecast
    q = "Marsabit"
    try:
        forecast = w_api.forecast_weather(
            q=q,
            days=14,
        )
        f = format_forecast(forecast)
        return f
    except exc as e:
        st.error(f"Error fetching weather data: {e}")
        return ""
