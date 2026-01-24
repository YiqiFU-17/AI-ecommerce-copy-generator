# Story: Build Product Input Form

- **User Story:** As a user, I want a clear and simple form where I can input all my product details, so that I can provide the AI with the context it needs.
- **Linked Epic:** Epic 2: Product Input & Configuration
- **Linked Requirements:** FR-2

### Acceptance Criteria
- The Streamlit UI displays a form with the following inputs:
  - Text input for "Product Title".
  - Text input for "Product Category".
  - A larger text area for "Key Features/Description".
  - Text input for "Promotion/Discount" (optional).
  - A dropdown select box for "Brand Tone" with options: `Playful`, `Luxurious`, `Professional`, `Witty`, `Eco-conscious`.
  - Text input for "Target Audience" (optional).
- A "Generate Copy" button is visible below the form.
- The form is enclosed within a `with st.form(...)` block to allow single submission.

### Tests / Definition of Done
- **Scenario:** User fills out the form.
- **Given:** The application is running.
- **When:** The user enters text into each input field and selects an option from the dropdown.
- **Then:** The UI retains the entered values.
- **When:** The user clicks the "Generate Copy" button.
- **Then:** The app correctly reads and stores all the input values into the `ProductInput` dataclass defined in `src/core.py`.

### Implementation Notes
- Use `st.text_input` for single-line fields.
- Use `st.text_area` for the description.
- Use `st.selectbox` for the brand tone.
- The "Generate Copy" button (`st.form_submit_button`) should be inside the form block.
- For now, clicking the button will only handle form data; it does not need to trigger the AI service yet.
