from dotenv import load_dotenv
import os
import requests
import json

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
UNITS = "metric"

def load_api_key():
    load_dotenv()
    return os.getenv("API_KEY")

api_key = load_api_key()  # Fetch the API key

def validate_zip_code(zip_code):
    if not zip_code.isdigit():
        raise ValueError("Invalid zip code. Please enter a numeric zip code.")

def fetch_weather_data(zip_code, api_key):
    params = {
        "zip": zip_code,
        "appid": api_key,
        "units": UNITS
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def get_temperature_by_zip(zip_code: str, api_key: str) -> tuple[str, str]:
    """
    Fetches the temperature for a given zip code using the OpenWeatherMap API.

    Args:
        zip_code (str): The zip code for which to fetch the temperature.
        api_key (str): Your OpenWeatherMap API key.

    Returns:
        tuple[str, str]: A message about the temperature or an error, and the city name (if available).
    """
    try:
        data = fetch_weather_data(zip_code, api_key)
        temperature = round(data["main"]["temp"])  # Round the temperature
        city = data["name"]
        return f"The temperature for zip code {zip_code} is {temperature}°C.", city
    except requests.exceptions.ConnectionError:
        return "Connection error. Please check your internet connection.", ""
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}", ""
    except KeyError:
        return "Invalid response from the API. Please check the zip code and try again.", ""

def main():
    zip_code = input("Please enter a zip code in Spain: ")
    zip_code_with_country = f"{zip_code},ES"
    result, city = get_temperature_by_zip(zip_code_with_country, api_key)
    if "°C" in result:
        temperature = result.split("is ")[1]
        print(f"The temperature for {city} is {temperature}")
    else:
        print(result)

if __name__ == "__main__":
    main()
