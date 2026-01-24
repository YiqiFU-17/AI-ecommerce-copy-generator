# Story: Display Results in UI

- **User Story:** As a user, I want to see the generated copy clearly displayed in the UI after I click "Generate", so I can review the results of my request.
- **Linked Epic:** Epic 4: Display & Export Results
- **Linked Requirements:** FR-3, FR-5 (display)

### Acceptance Criteria
- Clicking the "Generate Copy" button in the UI now triggers the `generate_copy_from_input` service function.
- While the function is running, an `st.spinner("Generating copy...")` message is displayed.
- On success, the spinner disappears and the generated content is displayed.
- The 3 captions, the list of hashtags, and the 2 CTAs are each displayed under clear subheadings (e.g., `st.subheader("Captions")`).
- If the service raises an error, a user-friendly error message is displayed in the UI using `st.error()`.

### Tests / Definition of Done
- **Scenario:** Successful generation.
- **Given:** The user has filled the form and clicks "Generate".
- **When:** The backend service returns a valid `GeneratedCopy` object.
- **Then:** The UI updates to show the formatted captions, hashtags, and CTAs.
- **Scenario:** Failed generation.
- **Given:** The user clicks "Generate".
- **When:** The backend service raises an error.
- **Then:** The UI displays an error message (e.g., "Sorry, something went wrong. Please try again.").

### Implementation Notes
- In `app.py`, the call to the service function should be wrapped in a `try...except` block to handle errors gracefully.
- Use `st.session_state` to store the results, so they persist across re-runs unless the form is re-submitted.
- Use `st.markdown` or `st.write` to display the content.
