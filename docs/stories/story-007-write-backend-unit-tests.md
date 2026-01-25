# Story: Write Backend Unit Tests

- **User Story:** As a Developer, I want unit tests for the core service logic, so that I can verify its correctness and prevent regressions.
- **Linked Epic:** Epic 5: MVP Testing & Validation
- **Linked Requirements:** Architecture Document, Section 6 (Test Plan)

### Acceptance Criteria
- A `tests/test_core.py` file is created.
- A unit test for the `build_prompt` function is implemented. It asserts that given a sample `ProductInput`, the output string matches the expected prompt format.
- Unit tests for the response parsing logic within the core service are implemented. They test both valid and malformed/empty JSON inputs.
- All tests pass when `pytest` is run from the root directory.

### Tests / Definition of Done
- **Scenario:** Running the test suite.
- **Given:** The `pytest` library is installed.
- **When:** The developer runs `pytest tests/test_core.py`.
- **Then:** All tests pass without error.
- **Scenario:** A change breaks the prompt format.
- **Given:** A developer modifies the `build_prompt` function incorrectly.
- **When:** They run the test suite.
- **Then:** The `test_build_prompt` test fails, identifying the regression.

### Implementation Notes
- Use the `pytest` framework.
- Create mock `ProductInput` objects in the test file to use as test data.
- For response parsing, create sample JSON strings that mimic what the Gemini API would return.