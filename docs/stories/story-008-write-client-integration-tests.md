# Story: Write Client Integration Tests

- **User Story:** As a Developer, I want integration tests for the API client that mock the external service, so that I can verify its behavior under various conditions without making real API calls.
- **Linked Epic:** Epic 5: MVP Testing & Validation
- **Linked Requirements:** Architecture Document, Section 6 (Test Plan)

### Acceptance Criteria
- A `tests/test_client.py` file is created.
- Tests are implemented for the `GeminiClient.generate` method.
- The `requests.post` call is mocked using `pytest-mock`.
- Test cases are created to simulate:
  - A successful API call (200 OK with valid JSON).
  - An API call that times out.
  - An API call that returns a server error (e.g., 500).
  - An API call that returns a non-JSON response.
- Each test asserts that the client either returns the correct data or raises the specific custom exception.

### Tests / Definition of Done
- **Scenario:** Running the test suite.
- **Given:** `pytest` and `pytest-mock` are installed.
- **When:** The developer runs `pytest tests/test_client.py`.
- **Then:** All tests pass.
- **Scenario:** A change breaks error handling in the client.
- **Given:** A developer incorrectly changes the exception handling in `GeminiClient`.
- **When:** They run the test suite.
- **Then:** The relevant test case for that error condition fails.

### Implementation Notes
- Use `pytest` and the `mocker` fixture from `pytest-mock`.
- The `mocker.patch('requests.post', ...)` will be the primary tool.
- For each test, configure the mock's `return_value` or `side_effect` to simulate the desired scenario.
