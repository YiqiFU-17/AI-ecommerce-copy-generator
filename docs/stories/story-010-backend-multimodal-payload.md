# Story: Update Service and Client for Multimodal Payload

- **User Story:** As a developer, I need to update the backend service and Gemini client to handle multimodal (text and image) inputs, so that the model can generate content based on both.
- **Linked Epic:** Epic 6: Multimodal Content Generation (Image + Text)
- **Linked Requirements:** FR-8, Story 5

### Acceptance Criteria
- The `GeminiClient` in `src/client.py` is updated to handle a new `generate_from_multimodal` method.
- This method constructs a payload suitable for multimodal input using the project's default `gemini-2.5-flash` model, combining the text prompt and a Base64-encoded image with its MIME type (e.g., `{"inline_data": {"mime_type": "image/jpeg", "data": "..."}}`). The `generateContent` endpoint will be used, with `GEMINI_MODEL` possibly overridden if specific multimodal handling is required at the client level.
- The `generate_copy_from_input` service function in `src/core.py` is updated:
    - It now accepts optional image bytes and a MIME type.
    - If an image is provided, it calls the new `generate_from_multimodal` method on the client.
    - If no image is provided, it calls the existing text-only generation method, ensuring backward compatibility.
- The output schema of the service remains unchanged (3 captions, hashtags, 2 CTAs).
- Unit tests in `tests/test_client.py` are added to verify that the multimodal payload is constructed correctly.
- Unit tests in `tests/test_core.py` are updated or added to test the service layer's branching logic (i.e., calling the correct client method based on whether an image is provided).

### Tests / Definition of Done
- **Automated Tests (DoD):**
    - **`test_client.py`:**
        - A new test confirms that `generate_from_multimodal` correctly formats the `inline_data` with the right MIME type and Base64-encoded data.
    - **`test_core.py`:**
        - A test verifies that calling the service with image data results in a call to the client's `generate_from_multimodal` method.
        - A test verifies that calling the service with *only* text data results in a call to the client's original text-generation method.
        - All existing tests for the service must continue to pass.

### Files Likely to Change
- `src/client.py`: To add the new multimodal generation method.
- `src/core.py`: To update the service function to handle image data and call the correct client method.
- `tests/test_client.py`: To add unit tests for the new client functionality.
- `tests/test_core.py`: To add/update unit tests for the service logic.
