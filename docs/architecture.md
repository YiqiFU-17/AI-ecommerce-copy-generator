# Architecture Document: E-commerce Copywriting Tool (MVP)

**Version:** 1.1
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

*   **UI Layer (Streamlit):** Responsible for rendering the user interface, capturing user input from web forms, handling file uploads, displaying results, and managing file downloads. It orchestrates the application flow.
*   **Copy Generation Service Layer:** The core business logic. This layer takes raw input from the UI (including optional image data), uses the Gemini API Client to get a response from the LLM, and then parses and formats that response into the final data structure for display. It is also responsible for base64 encoding image data.
*   **Gemini API Client Layer:** A dedicated module responsible for all communication with the `gemini-2.5-flash` API. It handles multimodal request formatting, authentication, error handling, and response parsing.

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

This model represents the structured text data collected from the UI.

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

### 3.3. Image Input Schema (Internal Model)

This model represents the optional uploaded image data.

```python
# In src/core.py
@dataclass
class ImageInput:
    mime_type: str
    data: bytes
```

## 4. UI, Data Flow, and Client Design

### 4.1. UI and Data Flow for Image Upload

The UI will be updated to support an optional image upload, which triggers a multimodal request to the Gemini API.

*   **UI Component (`app.py`):**
    *   A `st.file_uploader` widget will be added to the input form, configured to accept only `.jpg` and `.png` files.
*   **Validation (`app.py`):**
    *   After a file is uploaded, the application will check its size. If it exceeds the 5MB limit, an error message is displayed using `st.error`, and the generation process is halted.
    *   The file uploader's `type` argument inherently handles file type validation.
*   **Preview (`app.py`):**
    *   Upon successful validation, a thumbnail of the uploaded image will be displayed using `st.image` so the user can confirm their selection.
*   **Data Flow:**
    1.  The user uploads a file via the `st.file_uploader`.
    2.  The Streamlit `UploadedFile` object is retrieved.
    3.  The file's MIME type (e.g., `image/jpeg`) is accessed via the `.type` attribute.
    4.  The raw image bytes are accessed via the `.getvalue()` method.
    5.  Both `mime_type` and `data` (bytes) are passed to the **Copy Generation Service Layer (`core.py`)**.
    6.  The service layer is responsible for **base64 encoding** the raw `data` bytes.
    7.  The encoded data and MIME type are passed to the `GeminiClient`.

### 4.2. Gemini Client Design

The `src/client.py` module will be updated to handle multimodal requests.

**1. `build_request_payload(data: ProductInput, image_input: Optional[ImageInput]) -> list:`**
    *   This function replaces the previous `build_prompt` and constructs the `parts` array for the `generateContent` API call.
    *   **Part 1 (Text):** The first element is always the text prompt, constructed from the `ProductInput` data.
    *   **Part 2 (Image, Optional):** If an `ImageInput` is provided, a second dictionary is appended to the list. This dictionary contains the `inline_data` with the `mime_type` and the **base64-encoded** image data.
    *   **Example Payload Structure (Multimodal):**
        ```json
        [
          { "text": "You are an expert copywriter... Product Details: ..." },
          {
            "inline_data": {
              "mime_type": "image/jpeg",
              "data": "iVBORw0KGgoAAAANSUhEUgAA..."
            }
          }
        ]
        ```

**2. `class GeminiClient:`**
    *   **`__init__(self)`:** No changes.
    *   **`generate(self, payload: list) -> dict:`:**
        *   The method signature is updated to accept the `payload` list generated by `build_request_payload`.
        *   It sends this payload directly as the `contents` in the POST request to the Gemini API.
        *   Error handling and retry logic remain the same.

## 5. Security & Privacy

*   **API Key Management:** The `GEMINI_API_KEY` **must not** be hardcoded.
*   **No Data Storage:** The application remains stateless. No user-provided data, uploaded files, or generated content will be saved to disk or a database.
*   **File Upload Validation:** The application performs server-side validation of the file size (<= 5MB) and type (`image/jpeg`, `image/png`) to prevent abuse of the upload endpoint.
*   **Prompt Injection:** The primary mitigation remains user review.

## 6. Test Plan

*   **Unit Tests (`tests/test_core.py`):**
    *   Update tests for the prompt builder to check the new `build_request_payload` function. Test cases should cover both text-only and multimodal scenarios, verifying the base64 encoding is correctly applied.
    *   Test the response parsing logic remains unchanged.
*   **Integration Test (`tests/test_client.py`):**
    *   Update tests for `GeminiClient.generate` to pass a sample multimodal payload.
    *   Use `pytest-mock` to simulate API responses and ensure the client correctly sends the multimodal payload.

## 7. Failure Modes

*   **Invalid File Upload:** If a user uploads a file that is not a `.png` or `.jpg`, or if the file is over 5MB, the UI will display a clear error message via `st.error`, and the "Generate" button will not proceed with an API call.
*   **API Error:** If the Gemini API returns an error (e.g., it cannot process the image, or a server error occurs), the `APIError` from the client will be caught by the service layer, and a user-friendly error message will be displayed in the Streamlit UI.

## 8. Unchanged Functionality

Because the output schema (`GeneratedCopy`) remains the same, the existing features for displaying, copying, and exporting the generated captions, hashtags, and CTAs **are not affected and require no changes.**

## 9. `requirements.txt` Contents

No changes are required to the dependencies for this update.
```
streamlit
python-dotenv
requests
pytest
pytest-mock
```