# Story: Implement Export Features

- **User Story:** As a user, I want to easily copy or download the generated text, so I can use it in other applications or save it for later.
- **Linked Epic:** Epic 4: Display & Export Results
- **Linked Requirements:** FR-6, FR-7

### Acceptance Criteria
- A "Copy" button is displayed next to each individual caption, the block of hashtags, and the block of CTAs.
- Clicking a "Copy" button copies the corresponding text to the user's clipboard.
- A "Download All as TXT" button is displayed after results are generated.
- Clicking the download button prompts the user to save a `.txt` file.
- The downloaded `.txt` file is formatted exactly as specified in the PRD (section 6.2).

### Tests / Definition of Done
- **Scenario:** User wants to copy content.
- **Given:** Results are displayed in the UI.
- **When:** The user clicks a "Copy" button.
- **Then:** The correct text is available on their clipboard (manual verification).
- **Scenario:** User wants to download content.
- **Given:** Results are displayed.
- **When:** The user clicks "Download All as TXT".
- **Then:** A file named `copy-results.txt` is downloaded.
- **And:** The content and formatting of the file match the PRD specification.

### Implementation Notes
- Streamlit does not have a native clipboard function. A simple third-party library like `streamlit-copy-button` might be needed, or a custom component. For MVP, if a library is not simple, providing the text in a box for manual copy is acceptable. Let's assume a library like `streamlit-extras` provides this.
- Use `st.download_button` to implement the download feature. The `data` parameter will be a string formatted according to the PRD.
