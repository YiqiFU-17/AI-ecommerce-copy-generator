# Story: Implement Gemini API Client

- **User Story:** As a Developer, I need a robust and isolated client to handle all communication with the Gemini API, so that the core application logic is decoupled from the external service.
- **Linked Epic:** Epic 3: AI Copy Generation Service
- **Linked Requirements:** NFR-5, NFR-6

### Acceptance Criteria
- A `GeminiClient` class is created in `src/client.py`.
- The client's constructor reads the `GEMINI_API_KEY` from environment variables and raises a `ConfigurationError` if it's missing.
- A `generate` method exists that takes a prompt string as input.
- The `generate` method sends a POST request to the `gemini-2.5-flash` API endpoint using the `requests` library.
- The request includes a 15-second timeout.
- The method returns the parsed JSON response as a dictionary on success.
- The method raises custom exceptions (`APITimeoutError`, `APIError`, `ResponseParseError`) for failure cases (timeout, non-200 status, invalid JSON).

### Tests / Definition of Done
- **Scenario:** The client is used to call the API.
- **Given:** A valid prompt string.
- **When:** The `generate` method is called.
- **Then:** It successfully returns a dictionary (tested with a mocked API).
- **Scenario:** The API is slow or returns an error.
- **Given:** The mocked API simulates a timeout or a 500 error.
- **When:** The `generate` method is called.
- **Then:** The appropriate custom exception is raised.

### Implementation Notes
- Use the `requests` library for HTTP calls.
- Use `os.getenv()` to retrieve the API key.
- Define custom exception classes in `src/client.py`.
- Refer to the Gemini API documentation for the exact request payload structure.
