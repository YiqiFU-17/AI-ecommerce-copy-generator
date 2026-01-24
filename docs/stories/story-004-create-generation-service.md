# Story: Create Copy Generation Service

- **User Story:** As a Developer, I need a service layer that orchestrates the copy generation process, so that UI logic is separated from the core business logic.
- **Linked Epic:** Epic 3: AI Copy Generation Service
- **Linked Requirements:** FR-4, FR-5 (parsing)

### Acceptance Criteria
- A function `generate_copy_from_input(data: ProductInput) -> GeneratedCopy` is created in `src/core.py`.
- This function calls a `build_prompt(data: ProductInput)` function to construct the precise LLM prompt.
- It instantiates the `GeminiClient` and calls its `generate` method with the prompt.
- It safely parses the dictionary response from the client.
- It populates and returns a `GeneratedCopy` dataclass instance on success.
- It catches exceptions from the client and propagates them or raises a higher-level `GenerationError`.

### Tests / Definition of Done
- **Scenario:** Generate copy from valid input.
- **Given:** A valid `ProductInput` object.
- **When:** The `generate_copy_from_input` function is called.
- **Then:** It returns a valid `GeneratedCopy` object (tested with a mocked client).
- **Scenario:** The underlying client fails.
- **Given:** The `GeminiClient` mock is configured to raise an exception.
- **When:** `generate_copy_from_input` is called.
- **Then:** The function catches the client exception and raises a `GenerationError`.

### Implementation Notes
- The `build_prompt` function is critical. It must create the exact prompt structure defined in `architecture.md`, including the JSON output instructions.
- All data models (`ProductInput`, `GeneratedCopy`) should be defined in `src/core.py` as well.
