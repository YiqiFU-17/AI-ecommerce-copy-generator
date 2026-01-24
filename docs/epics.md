# MVP Epics: E-commerce Copywriting Tool

**Version:** 1.0
**Status:** Ready for Development

This document breaks down the MVP into major themes of work (Epics). Each epic represents a significant chunk of user value and is aligned with the approved PRD and Architecture documents. The scope is locked per `docs/irr.md`.

---

### Epic 1: Core Application Setup & UI Shell

*   **Goal:** Establish the foundational project structure and a running, empty Streamlit application shell. This is the technical backbone for all subsequent features.
*   **Maps to:** FR-1, NFR-1, NFR-2, NFR-3, NFR-4
*   **In Scope:**
    *   Creating the repository structure as defined in `architecture.md`.
    *   Initializing `requirements.txt` with all specified libraries.
    *   Creating a basic `app.py` that runs and displays a title and placeholder text.
    *   Setting up the `.env` file for local environment variable management.
*   **Out of Scope:**
    *   Any business logic for copy generation.
    *   Any user input fields or output displays.
*   **Definition of Done:**
    *   The project structure exists on disk.
    *   `pip install -r requirements.txt` runs successfully.
    *   `streamlit run app.py` starts the application without errors.
    *   A basic title is visible in the browser.

---

### Epic 2: Product Input & Configuration

*   **Goal:** Enable users to input all necessary product details through a simple and intuitive web form.
*   **Maps to:** FR-2
*   **In Scope:**
    *   Implementing all text input fields specified in PRD section 6.1 (Title, Category, Features, etc.).
    *   Implementing the "Brand Tone" dropdown with the predefined options.
    *   Laying out the fields in a logical order on the Streamlit UI.
    *   Storing the user's input in the `ProductInput` dataclass in memory on submission.
*   **Out of Scope:**
    *   The "Generate Copy" button's functionality (it can exist but will be disabled or do nothing).
    *   File uploads for images or CSVs.
*   **Definition of Done:**
    *   All required text and dropdown input fields are rendered in the UI.
    *   User can type into all fields.
    *   When a "Submit" (or "Generate") button is pressed, the app correctly populates the `ProductInput` data object with the form data.

---

### Epic 3: AI Copy Generation Service

*   **Goal:** Build the core backend engine that communicates with the Gemini API to generate marketing copy based on user input.
*   **Maps to:** FR-4, FR-5 (parsing), NFR-5, NFR-6
*   **In Scope:**
    *   Implementing the `GeminiClient` class as specified in `architecture.md`.
    *   Implementing API key retrieval from environment variables.
    *   Implementing the `build_prompt` function to create the precise prompt for the LLM.
    *   Implementing the service logic to call the client, handle responses (success and errors), and parse the returned JSON into the `GeneratedCopy` data model.
    *   Implementing timeout and basic retry logic.
*   **Out of Scope:**
    *   Integrating this service with the Streamlit UI. This epic can be developed and tested independently.
*   **Definition of Done:**
    *   The `GeminiClient` can successfully send a request to the real API endpoint and get a response.
    *   The client correctly handles API errors, timeouts, and JSON parsing errors.
    *   A service-level function can take a `ProductInput` object and return a populated `GeneratedCopy` object or raise an appropriate exception.
    *   Unit and Integration tests for this service (as defined in the Test Plan) are passing.

---

### Epic 4: Display & Export Results

*   **Goal:** Wire the UI to the generation service, display the results to the user, and provide the core export and copy-paste functionality.
*   **Maps to:** FR-3, FR-5 (display), FR-6, FR-7
*   **In Scope:**
    *   Activating the "Generate Copy" button to trigger the `CopyGenerationService`.
    *   Displaying a loading indicator while the service is running.
    *   Rendering the `captions`, `hashtags`, and `ctas` from the `GeneratedCopy` object in a clean, readable format in the UI.
    *   Implementing a "Copy to Clipboard" button for each distinct piece of content.
    *   Implementing the "Download All" button that generates and downloads a `.txt` file with all results, formatted as specified in the PRD.
*   **Out of Scope:**
    *   Any export format other than `.txt`.
    *   Saving or viewing a history of results.
*   **Definition of Done:**
    *   Clicking "Generate Copy" with valid inputs displays formatted results in the UI.
    *   Error messages from the service layer are displayed to the user in a friendly format.
    *   The "Copy to Clipboard" buttons work as expected.
    *   The "Download All" button successfully downloads a correctly formatted `.txt` file.

---

### Epic 5: MVP Testing & Validation

*   **Goal:** Ensure the application is robust, reliable, and meets requirements by implementing the defined testing strategy.
*   **Maps to:** Architecture Document, Section 6 (Test Plan)
*   **In Scope:**
    *   Writing and passing all unit tests for the `build_prompt` function and response parsing logic.
    *   Writing and passing all integration tests for the `GeminiClient`, using a mocked API to simulate various success and failure scenarios.
    *   Creating a `tests` directory and configuring `pytest`.
*   **Out of Scope:**
    *   End-to-end UI testing (e.g., using Selenium or Playwright). This is out of scope for the MVP.
    *   Performance or load testing.
*   **Definition of Done:**
    *   All tests in the `tests` directory pass when `pytest` is run.
    *   Test coverage for `src/client.py` and `src/core.py` is established.
    *   The `requirements.txt` file is updated with `pytest` and `pytest-mock`.
