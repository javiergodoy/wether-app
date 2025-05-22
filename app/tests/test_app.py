import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json
import requests
import pytest
# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import validate_zip_code, fetch_weather_data, get_temperature_by_zip




def test_validate_zip_code_valid():
    # Should not raise any exception
    validate_zip_code("28001")

def test_validate_zip_code_invalid():
    with pytest.raises(ValueError) as excinfo:
        validate_zip_code("ABC12")
    assert "Invalid zip code" in str(excinfo.value)

@patch('app.requests.get')
def test_fetch_weather_data_success(mock_get):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {"main": {"temp": 20}, "name": "Madrid"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Call the function
    result = fetch_weather_data("28001,ES", "fake_api_key")
    
    # Verify the result
    assert result == {"main": {"temp": 20}, "name": "Madrid"}
    mock_get.assert_called_once()

@patch('app.fetch_weather_data')
def test_get_temperature_by_zip_success(mock_fetch):
    # Setup mock response
    mock_fetch.return_value = {"main": {"temp": 20}, "name": "Madrid"}
    
    # Call the function
    result, city = get_temperature_by_zip("28001,ES", "fake_api_key")
    
    # Verify the result
    assert "20°C" in result
    assert city == "Madrid"

@patch('app.fetch_weather_data')
def test_get_temperature_by_zip_request_exception(mock_fetch):
    # Setup mock to raise exception
    mock_fetch.side_effect = requests.exceptions.RequestException("Test error")
    
    # Call the function
    result = get_temperature_by_zip("28001,ES", "fake_api_key")
    
    # Verify the result
    assert "An error occurred" in result[0]

@patch('app.fetch_weather_data')
def test_get_temperature_by_zip_key_error(mock_fetch):
    # Setup mock to return data missing required keys
    mock_fetch.return_value = {"weather": []}
    
    # Call the function
    result = get_temperature_by_zip("28001,ES", "fake_api_key")
    
    # Verify the result
    assert "Invalid response" in result[0]

@patch('app.fetch_weather_data')
def test_get_temperature_by_zip_connection_error(mock_fetch):
    # Setup mock to raise connection error
    mock_fetch.side_effect = requests.exceptions.ConnectionError()
    
    # Call the function
    result = get_temperature_by_zip("28001,ES", "fake_api_key")
    
    # Verify the result
    assert "Connection error" in result[0]