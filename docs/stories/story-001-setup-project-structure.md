# Story: Setup Project Structure

- **User Story:** As a Developer, I want a standardized project structure and all dependencies defined, so that I can start a runnable application shell without any setup friction.
- **Linked Epic:** Epic 1: Core Application Setup & UI Shell
- **Linked Requirements:** FR-1, NFR-1, NFR-2, NFR-3, NFR-4

### Acceptance Criteria
- A git repository can be initialized in the root directory.
- The folder structure (`docs/`, `src/`, `tests/`) exists as defined in `architecture.md`.
- A `requirements.txt` file exists with all specified libraries (`streamlit`, `python-dotenv`, `requests`, `pytest`, `pytest-mock`).
- An `app.py` file exists that runs a basic Streamlit app with a title.
- A `.env` file for local development is present and documented.

### Tests / Definition of Done
- **Scenario:** A new developer clones the repository.
- **Given:** They have Python and pip installed.
- **When:** They run `pip install -r requirements.txt`.
- **Then:** All dependencies install without error.
- **When:** They run `streamlit run app.py`.
- **Then:** The application starts and is accessible in a web browser, displaying a title.

### Implementation Notes
- Follow the repository structure in `architecture.md` exactly.
- The initial `app.py` can be a simple "Hello World" style app:
  ```python
  import streamlit as st
  st.title("E-commerce Copywriting Tool")
  ```
- Create an empty `.gitignore` file.
