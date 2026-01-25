# Story: Streamlit UI Image Upload & Validation

- **User Story:** As a user, I want to optionally upload an image to provide more context for content generation, with clear validation rules so I know my input is correct.
- **Linked Epic:** Epic 6: Multimodal Content Generation (Image + Text)
- **Linked Requirements:** FR-8, Story 5

### Acceptance Criteria
- The Streamlit UI (`app.py`) includes a new `st.file_uploader` component allowing users to upload an image.
- The uploader is configured to accept only `.jpg`, `.jpeg`, and `.png` file types.
- If a user attempts to upload a file that is not a JPG, JPEG, or PNG, a clear error message is displayed in the UI (e.g., "Invalid file type. Please upload a JPG, JPEG, or PNG.").
- If a user uploads an image larger than 5MB, a clear error message is displayed (e.g., "Image is too large. Please upload an image under 5MB.").
- When an image is successfully uploaded, a small preview of the image is displayed in the UI.
- The image upload is optional; the "Generate" button remains active even if no image is provided.
- On form submission, the uploaded image's file bytes and MIME type are extracted and passed as new arguments to the content generation service call.
- The system supports image-only generation, where the user provides only an image without filling the product text fields, and the generation proceeds successfully.

### Tests / Definition of Done
- **Manual Tests:**
    - Verify that the file uploader appears in the UI.
    - Verify that uploading a valid JPG/JPEG/PNG under 5MB shows a preview and allows generation.
    - Verify that uploading a non-JPG/JPEG/PNG file displays the correct file type error.
    - Verify that uploading a JPG/JPEG/PNG larger than 5MB displays the correct size error.
    - Verify that generation can be triggered with text-only input (no image).
- **Automated Tests:**
    - New or updated tests in `tests/test_core.py` and `tests/test_client.py` to cover:
        - Image-only generation path (providing only an image, no text prompt).
        - Text-only generation path (ensuring backward compatibility).
        - Correct construction of the multimodal payload parts (text and `inline_data` for images) when both are provided.

### Files Likely to Change
- `app.py`: To add the `st.file_uploader` and associated validation and preview logic.
- `src/core.py`: The service function signature will be updated to accept optional image data.
