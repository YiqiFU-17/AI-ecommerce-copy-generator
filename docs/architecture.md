# Architecture Document: E-commerce Copywriting Tool (MVP)

**Version:** 1.0
**Status:** Proposed
**Author:** Winston, Architect

---

## 1. High-Level Architecture

The architecture for this MVP is a simple, single-process web application composed of three logical layers. The design is stateless and prioritizes simplicity for a rapid ~1-week implementation.

```
+--------------------------------+
|      Browser (User)            |
+--------------------------------+
             |
             | HTTP
             v
+--------------------------------+
|    Web Application (Python)    |
|   +--------------------------+ |
|   |   UI Layer (Streamlit)   | |
|   +--------------------------+ |
|   | Copy Gen. Service Layer  | |
|   +--------------------------+ |
|   | Gemini API Client Layer  | |
|   +--------------------------+ |
+--------------------------------+
             |
             | HTTPS API Call
             v
+--------------------------------+
|  Third-Party LLM Service       |
|  (e.g., Google AI Platform)    |
+--------------------------------+
```

*   **UI Layer (Streamlit):** Responsible for rendering the user interface, capturing user input from web forms, displaying results, and handling file downloads. It orchestrates the application flow.
*   **Copy Generation Service Layer:** The core business logic. This layer takes the raw input from the UI, uses the Gemini API Client to get a response from the LLM, and then parses and formats that response into the final data structure for display.
*   **Gemini API Client Layer:** A dedicated module responsible for all communication with the `gemini-2.5-flash` API. It handles request formatting, authentication, error handling, and response parsing.

## 2. Proposed Repository Structure

A standard Python application layout is proposed to maintain separation of concerns.

```
.
├── .env                  # For local development: GEMINI_API_KEY=...
├── .gitignore
├── app.py                # Main Streamlit application entry point
├── docs/
│   ├── prd.md
│   └── architecture.md
├── requirements.txt      # Project dependencies
├── src/
│   ├── __init__.py
│   ├── client.py         # Gemini API Client Layer
│   └── core.py           # Copy Generation Service Layer, Data Models
└── tests/
    ├── __init__.py
    ├── test_client.py    # Unit tests for the Gemini client
    └── test_core.py      # Unit/Integration tests for the service layer
```

## 3. Data Models

We will use simple Python classes or dataclasses for data modeling. They serve as a clear contract between layers.

### 3.1. Input Schema (Internal Model)

This model represents the structured data collected from the UI.

```python
# In src/core.py
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ProductInput:
    title: str
    category: str
    description: str
    brand_tone: str
    promotion: Optional[str] = None
    target_audience: Optional[str] = None
```

### 3.2. Output Schema (Internal Model)

This model represents the structured data returned by the LLM, after parsing.

```python
# In src/core.py
@dataclass
class GeneratedCopy:
    captions: List[str]
    hashtags: List[str]
    ctas: List[str]
```

## 4. Gemini Client Design

The `src/client.py` module will encapsulate all interactions with the Gemini API.

### Key Components:

1.  **`build_prompt(data: ProductInput) -> str`:**
    *   A dedicated function to construct the final text prompt sent to the LLM.
    *   It will take the `ProductInput` dataclass and assemble a structured prompt that instructs the model to generate the desired output in a specific JSON format.
    *   **Example Prompt Structure:**
        ```
        You are an expert Instagram copywriter. Given the following product details, generate 3 unique Instagram captions, 10 relevant hashtags, and 2 calls-to-action. Return the output as a single, minified JSON object with keys: "captions" (list of strings), "hashtags" (list of strings), and "ctas" (list of strings).

        Product Details:
        - Title: {data.title}
        - Category: {data.category}
        - Description: {data.description}
        - Brand Tone: {data.brand_tone}
        - Promotion: {data.promotion}
        ```

2.  **`class GeminiClient:`**
    *   **`__init__(self)`:** Initializes the client. Retrieves the API key using `os.getenv('GEMINI_API_KEY')`. If the key is not found, it should raise a specific `ConfigurationError`.
    *   **`generate(self, prompt: str) -> dict:`:**
        *   Accepts the text prompt.
        *   Sets a reasonable **timeout** (e.g., 15 seconds) for the request.
        *   Implements a simple **retry** mechanism (e.g., 1 retry on a 5xx server error).
        *   Sends the request to the `gemini-2.5-flash` endpoint via HTTPS POST.
        *   **Error Handling:**
            *   Catches `requests.Timeout` and raises a `ServiceTimeoutError`.
            *   Checks for non-200 HTTP status codes and raises a generic `APIError`.
            *   Attempts to parse the JSON response. If parsing fails, raises a `ResponseParseError`.
        *   Returns the parsed JSON dictionary on success.

## 5. Security & Privacy

Adhering to the stateless nature of the application is paramount.

*   **API Key Management:** The `GEMINI_API_KEY` **must not** be hardcoded. It will be loaded from an environment variable using `python-dotenv` for local development and set directly in the production environment.
*   **No Data Storage:** The application is stateless. No user-provided data, uploaded files, or generated content will be saved to disk or a database. All data is processed in memory per-request and then discarded.
*   **Prompt Injection:** For the MVP, the primary mitigation is user review. The UI must contain the disclaimer from the PRD ("*AI-generated content. Please review all claims for accuracy before posting.*"). No server-side sanitization will be implemented for the initial MVP to keep complexity low, as the user is the final gatekeeper.

## 6. Test Plan

Testing will focus on the logic layers, not the Streamlit UI itself. We will use `pytest` and `pytest-mock`.

*   **Unit Tests (`tests/test_core.py`):**
    *   Test the `build_prompt` function: ensure it correctly formats the prompt string from a sample `ProductInput` object.
    *   Test the response parsing logic: given a sample valid/invalid JSON string from the LLM, does the service layer correctly create the `GeneratedCopy` object or handle the error?
*   **Integration Test (`tests/test_client.py`):**
    *   Test the `GeminiClient.generate` method.
    *   Use a mocker (like `pytest-mock`'s `mocker`) to patch the `requests.post` call.
    *   Simulate different API responses: a successful 200 with valid JSON, a 500 server error, a timeout, and a 200 with malformed JSON.
    *   Assert that the client handles each case correctly (returns data or raises the expected custom exception).

## 7. `requirements.txt` Contents

The following libraries are required for the MVP.

```
streamlit
python-dotenv
requests
pytest
pytest-mock
```
