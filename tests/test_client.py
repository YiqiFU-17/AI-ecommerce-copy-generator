import pytest
import requests
import json  # Added missing import
from src.client import (
    GeminiClient,
    ConfigurationError,
    APIError,
    APITimeoutError,
    ResponseParseError,
)

# --- Initialization Tests ---

def test_client_initialization_success(mocker):
    """Tests successful client initialization when API key is present."""
    mocker.patch('os.getenv', return_value="test_api_key")
    client = GeminiClient()
    assert client.api_key == "test_api_key"
    assert "x-goog-api-key" in client.headers
    assert client.headers["x-goog-api-key"] == "test_api_key"

def test_client_initialization_raises_config_error(mocker):
    """Tests that ConfigurationError is raised if API key is missing."""
    mocker.patch('os.getenv', return_value=None)
    with pytest.raises(ConfigurationError, match="GEMINI_API_KEY environment variable not set"):
        GeminiClient()

def test_client_uses_default_model(mocker):
    """Tests that the client uses the 'gemini-2.5-flash' default model."""
    # This side effect simulates os.getenv finding the API key but not GEMINI_MODEL
    def getenv_side_effect(key, default=None):
        if key == 'GEMINI_API_KEY':
            return "test_api_key"
        return default
    mocker.patch('os.getenv', side_effect=getenv_side_effect)
    
    client = GeminiClient()
    expected_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    assert client.api_url == expected_url

def test_client_overrides_model_and_strips_prefix(mocker):
    """Tests that GEMINI_MODEL overrides the default and the 'models/' prefix is stripped."""
    def getenv_side_effect(key, default=None):
        if key == 'GEMINI_API_KEY':
            return "test_api_key"
        if key == 'GEMINI_MODEL':
            return "models/my-custom-model" # Provide the prefixed model name
        return default
    mocker.patch('os.getenv', side_effect=getenv_side_effect)

    client = GeminiClient()
    expected_url = "https://generativelanguage.googleapis.com/v1beta/models/my-custom-model:generateContent"
    assert client.api_url == expected_url


# --- Generate Method Tests ---

@pytest.fixture
def client(mocker):
    """Fixture to provide an initialized GeminiClient."""
    mocker.patch('os.getenv', return_value="test_api_key")
    return GeminiClient()

def test_generate_success(mocker, client):
    """Tests a successful generate call with a valid JSON response."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}
    mocker.patch('requests.post', return_value=mock_response)

    result = client.generate("test prompt")
    assert result == {"key": "value"}
    requests.post.assert_called_once()

def test_generate_raises_on_timeout(mocker, client):
    """Tests that APITimeoutError is raised on a request timeout."""
    mocker.patch('requests.post', side_effect=requests.exceptions.Timeout)
    
    with pytest.raises(APITimeoutError, match="Request timed out after 15 seconds."):
        client.generate("test prompt")

def test_generate_raises_on_http_error(mocker, client):
    """Tests that APIError is raised for a non-200 HTTP status."""
    mock_response = mocker.Mock()
    mock_response.status_code = 403
    mock_response.text = "Permission denied"
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
    mocker.patch('requests.post', return_value=mock_response)
    
    with pytest.raises(APIError, match="API returned a non-200 status: 403. Details: Permission denied"):
        client.generate("test prompt")

def test_generate_raises_on_json_decode_error(mocker, client):
    """Tests that ResponseParseError is raised for an invalid JSON response."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    # Use the imported 'json' module
    mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
    mocker.patch('requests.post', return_value=mock_response)

    with pytest.raises(ResponseParseError, match="Failed to decode API response as JSON."):
        client.generate("test prompt")