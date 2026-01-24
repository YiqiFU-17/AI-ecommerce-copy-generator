import os
import requests
import json

# --- Custom Exceptions ---
class ConfigurationError(Exception):
    """Raised when a required configuration is missing."""
    pass

class APIError(Exception):
    """Raised for general API errors (e.g., non-200 status codes)."""
    pass

class APITimeoutError(APIError):
    """Raised when the API call times out."""
    pass

class ResponseParseError(APIError):
    """Raised when the API response is not valid JSON."""
    pass


class GeminiClient:
    """
    A client for interacting with the Google Gemini API.
    """
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    
    def __init__(self):
        """
        Initializes the GeminiClient.
        
        Raises:
            ConfigurationError: If the GEMINI_API_KEY environment variable is not set.
        """
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ConfigurationError("GEMINI_API_KEY environment variable not set.")
        self.headers = {'Content-Type': 'application/json'}
        self.params = {'key': self.api_key}

    def generate(self, prompt: str, timeout: int = 15) -> dict:
        """
        Sends a prompt to the Gemini API and gets a response.

        Args:
            prompt: The text prompt to send to the model.
            timeout: The request timeout in seconds.

        Returns:
            The parsed JSON response from the API as a dictionary.

        Raises:
            APITimeoutError: If the request times out.
            APIError: For non-200 responses from the API.
            ResponseParseError: If the response body is not valid JSON.
        """
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        try:
            response = requests.post(
                self.API_URL,
                headers=self.headers,
                params=self.params,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)

        except requests.exceptions.Timeout:
            raise APITimeoutError(f"Request timed out after {timeout} seconds.")
        except requests.exceptions.RequestException as e:
            raise APIError(f"An unexpected error occurred: {e}")

        try:
            return response.json()
        except json.JSONDecodeError:
            raise ResponseParseError("Failed to decode API response as JSON.")

