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
    """Raised when the response body is not valid JSON."""
    pass


class GeminiClient:
    """
    A client for interacting with the Google Gemini API.
    """
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/"
    
    def __init__(self):
        """
        Initializes the GeminiClient.
        
        Reads configuration from environment variables.
        
        Raises:
            ConfigurationError: If the GEMINI_API_KEY environment variable is not set.
        """
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ConfigurationError("GEMINI_API_KEY environment variable not set.")
        
        # Default MODEL must be "gemini-2.5-flash" as per hard requirement.
        # Allow overriding via env var GEMINI_MODEL.
        model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
        
        # Make client robust if GEMINI_MODEL is provided as "models/xxx"
        if model_name.startswith("models/"):
            model_name = model_name[len("models/"):]
            
        self.api_url = f"{self.BASE_URL}{model_name}:generateContent"
        
        self.headers = {
            'Content-Type': 'application/json',
            'x-goog-api-key': self.api_key
        }

    def generate(self, prompt: str, image_b64_data: str = None, image_mime_type: str = None, timeout: int = 15) -> dict:
        """
        Sends a prompt (and optional image) to the Gemini API and gets a response.

        Args:
            prompt: The text prompt to send to the model.
            image_b64_data: Optional base64-encoded string of the image data.
            image_mime_type: Optional MIME type of the image (e.g., "image/jpeg").
            timeout: The request timeout in seconds.

        Returns:
            The parsed JSON response from the API as a dictionary.

        Raises:
            APITimeoutError: If the request times out.
            APIError: For non-200 responses from the API, including the status code and error message.
            ResponseParseError: If the response body is not valid JSON.
        """
        parts = [{"text": prompt}]
        if image_b64_data and image_mime_type:
            parts.append({
                "inline_data": {
                    "mime_type": image_mime_type,
                    "data": image_b64_data
                }
            })

        payload = {
            "contents": [{"parts": parts}]
        }

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=timeout
            )
            # Raise an HTTPError for bad responses (4xx or 5xx)
            response.raise_for_status()

        except requests.exceptions.Timeout:
            raise APITimeoutError(f"Request timed out after {timeout} seconds.")
        except requests.exceptions.HTTPError as e:
            # Extract more detail from the HTTP error response if possible
            error_details = e.response.text
            raise APIError(f"API returned a non-200 status: {e.response.status_code}. Details: {error_details}")
        except requests.exceptions.RequestException as e:
            raise APIError(f"An unexpected error occurred during the request: {e}")

        try:
            return response.json()
        except json.JSONDecodeError:
            raise ResponseParseError("Failed to decode API response as JSON.")
