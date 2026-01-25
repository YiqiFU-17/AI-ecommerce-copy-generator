# Story: Update Service and Client for Multimodal Payload

- **User Story:** As a developer, I need to update the backend service and Gemini client to handle multimodal (text and image) inputs, so that the model can generate content based on both.
- **Linked Epic:** Epic 6: Multimodal Content Generation (Image + Text)
- **Linked Requirements:** FR-8, Story 5

### Acceptance Criteria
- The `GeminiClient.generate` method in `src/client.py` is updated to accept optional `image_b64_data: str` and `image_mime_type: str` parameters.
- When `image_b64_data` and `image_mime_type` are provided, the `generate` method constructs a payload suitable for multimodal input, combining the text prompt and a Base64-encoded image with its MIME type (e.g., `{"inline_data": {"mime_type": "image/jpeg", "data": "..."}}`). The `generateContent` endpoint will be used.
- The `generate_copy_from_input` service function in `src/core.py` is updated:
    - It now accepts optional `image_bytes: bytes` and `image_mime_type: str`.
    - If `image_bytes` are provided, the service base64-encodes them and passes the `image_b64_data` and `image_mime_type` to the `GeminiClient.generate` method, along with the text prompt.
    - If no `image_bytes` are provided, it calls `GeminiClient.generate` with only the text prompt, ensuring backward compatibility.
- The system supports image-only generation, where the user provides only an image without providing product text fields, and the generation proceeds successfully.
- The output schema of the service remains unchanged (3 captions, hashtags, 2 CTAs).
- Unit tests in `tests/test_client.py` are added to verify that the multimodal payload is constructed correctly.
- Unit tests in `tests/test_core.py` are updated or added to test the service layer's branching logic (i.e., calling the correct client method based on whether an image is provided).

### Tests / Definition of Done
- **Automated Tests (DoD):**
    - **`test_client.py`:**
        - A new test confirms that `GeminiClient.generate` correctly formats the `inline_data` with the right MIME type and Base64-encoded data when `image_b64_data` and `image_mime_type` are provided.
        - Add tests for image-only generation path (without providing product text fields) through `GeminiClient.generate`.
    - **`test_core.py`:**
        - A test verifies that calling `generate_copy_from_input` with image data correctly base64-encodes the image and passes `image_b64_data` and `image_mime_type` to `GeminiClient.generate`.
        - A test verifies that calling `generate_copy_from_input` with *only* text data correctly calls `GeminiClient.generate` with only the prompt.
        - Add tests for image-only generation path (without providing product text fields) through `generate_copy_from_input`.
        - All existing tests for the service must continue to pass.

### Files Likely to Change
- `src/client.py`: To add the new multimodal generation method.
- `src/core.py`: To update the service function to handle image data and call the correct client method.
- `tests/test_client.py`: To add unit tests for the new client functionality.
- `tests/test_core.py`: To add/update unit tests for the service logic.
