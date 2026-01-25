# Product Requirements Document: E-commerce Copywriting Tool (MVP)

**Version:** 1.0
**Status:** Scoped for MVP
**Author:** John, Product Manager
**Stakeholders:** yiqi (Project Lead)

---

## 1. The Opportunity: Problem Statement, Target Users, and Personas

### 1.1. Problem Statement

Small e-commerce business owners and freelance marketers **struggle to consistently create high-quality, on-brand Instagram copy**. This essential marketing task is time-consuming and creatively draining, often resulting in generic posts that fail to drive engagement or sales. The direct impact is lost revenue, wasted marketing effort, and an inability to compete with larger brands that have dedicated copywriting teams.

### 1.2. Our Solution

A lightweight, AI-powered tool that transforms basic product information into a complete, ready-to-post Instagram package (captions, hashtags, CTAs). The goal is to **drastically reduce the time and effort** required to create compelling social media content, freeing entrepreneurs to focus on growing their business.

### 1.3. Target Users & Personas

Our target users are individuals or small teams directly responsible for marketing e-commerce products on social media, who lack the time or budget for a dedicated copywriter.

*   **Persona 1: Sarah, The Solopreneur Seller.** She runs a handmade jewelry shop and *is* the entire company. She needs to create engaging posts in minutes, so she can get back to her primary job: making products.
*   **Persona 2: Ben, The Marketing Generalist.** He's the one-man marketing team for an online subscription box company. He needs to efficiently generate a large volume of unique copy for multiple new products each week.
*   **Persona 3: Maria, The Freelance Social Media Manager.** She juggles 5+ small business clients with different brand voices. She needs a tool to quickly switch context and generate on-brand copy without creative burnout.

## 2. User Experience: Journey and Use Cases

### 2.1. Primary User Journey

The user journey is designed for speed and simplicity:

1.  **Input:** User provides product information via a simple web form.
2.  **Configure:** User selects brand tone and other optional parameters.
3.  **Generate:** User clicks a "Generate" button. The tool sends a structured prompt to the LLM API.
4.  **Review:** The UI displays the generated copy (multiple caption variants, hashtags, CTAs).
5.  **Export:** User copies text directly or downloads the output as a `.txt` or `.csv` file.

### 2.2. Key Use Cases for MVP

1.  **Text-Only Input:** The user provides structured text details (product title, features, etc.) to generate copy. This is the core, most reliable use case.
2.  **Image-Only Input:** The user uploads a single product image. The tool uses a multimodal model to describe the image and generate copy. (This is a "Should-Have" and depends on the model's capabilities being easily accessible).
3.  **Text + Image Input:** The user provides both text fields and an image, giving the AI maximum context for the highest quality output.

## 3. MVP Scope: The MoSCoW Method

This scope is defined for a **~1-week implementation sprint**.

### 3.1. Must-Haves (Core MVP)

*   **M-1:** Simple web UI built with Python (Streamlit).
*   **M-2:** Form for structured text input (product title, description, features, brand tone).
*   **M-3:** Integration with a third-party LLM API (`gemini-2.5-flash`).
*   **M-4:** Core prompt engineering to generate 3 Instagram caption variants, 5-10 relevant hashtags, and 2 CTA options from text input.
*   **M-5:** Display generated results clearly in the UI.
*   **M-6:** "Copy to Clipboard" button for each generated asset.
*   **M-7:** "Download All" button that exports results into a single `.txt` file.
*   **M-8:** `requirements.txt` file listing all external libraries.

### 3.2. Should-Haves (High-Value additions, if time permits)

*   **S-1:** File upload for a single product image to use as input.
*   **S-2:** File upload for product data via a `.csv` file (mapping columns to input fields).
*   **S-3:** Export results in `.csv` and `.json` formats.
*   **S-4:** Generation of `alt-text` for the product image.

### 3.3. Could-Haves (Future Release Candidates)

*   **C-1:** User-configurable options (e.g., number of captions to generate).
*   **C-2:** Saving brand profiles (tone, target audience) for reuse.
*   **C-3:** History of generated content.
*   **C-4:** Support for multiple images.

### 3.4. Won't-Haves (Explicitly Out of Scope for MVP)

*   User accounts or authentication.
*   Direct posting or scheduling to Instagram.
*   A/B testing, performance analytics, or post tracking.
*   Team collaboration features.
*   Support for any platform other than Instagram.
*   Any form of image generation or editing.
*   A database for storing user data.

## 4. Requirements

### 4.1. Functional Requirements

Based on the Must-Haves:
*   **FR-1:** The system shall provide a web interface accessible via a browser.
*   **FR-2:** The UI must contain text input fields for: Product Title, Product Category, Key Features/Description, Promotion/Discount, Brand Tone, and Target Audience.
*   **FR-3:** The system must provide a "Generate Copy" button.
*   **FR-4:** On button click, the system shall construct a prompt and send it to the `gemini-2.5-flash` API endpoint.
*   **FR-5:** The system shall parse the API response and display the following in a structured format:
    *   3 distinct Instagram caption variants.
    *   A list of 5-10 suggested hashtags.
    *   A list of 2 suggested Call-to-Action (CTA) phrases.
*   **FR-6:** The UI must feature a "Copy" button next to each generated caption, hashtag list, and CTA list.
*   **FR-7:** The UI must feature a "Download Results" button that saves all currently displayed outputs into a single, formatted `.txt` file.
*   **FR-8:** The system shall allow the user to upload a single image (`.jpg`, `.jpeg`, `.png`) as an optional input for content generation.
    *   **Acceptance Criteria:**
        *   The UI must feature a file upload widget that accepts only `.jpg`, `.jpeg`, and `.png` file types.
        *   The system must enforce a maximum file size of 5MB.
        *   If a user attempts to upload an unsupported file type or a file larger than 5MB, a clear error message shall be displayed (e.g., "Invalid file. Please upload a JPG or PNG under 5MB.").
        *   The image upload is optional; generation can proceed with text-only inputs or with both image and text inputs.
        *   When both an image and text fields are provided, the model prompt should prioritize facts from the image and use text fields (like Brand Tone, Promotion) as supplemental constraints.
        *   The generated output structure (3 captions, hashtags, 2 CTAs) must remain identical to the text-only output.

### 4.2. Non-Functional Requirements

*   **NFR-1:** The application **must** be written in Python.
*   **NFR-2:** The user interface **must** be built using the Streamlit library.
*   **NFR-3:** All external Python dependencies **must** be listed in a `requirements.txt` file.
*   **NFR-4:** The application **must** be stateless. It will not store user data between sessions.
*   **NFR-5:** The API key for the LLM service must be configurable via an environment variable, not hardcoded.
*   **NFR-6:** The application should render a usable response within 15 seconds of the user clicking "Generate."

## 5. User Stories (MVP Must-Haves)

*   **Story 1: Product Details Input**
    *   **As a** user (Sarah the Solopreneur),
    *   **I want** to enter my product's details into simple text fields,
    *   **so that** I can provide the AI with the core information it needs to write copy.
    *   **Acceptance Criteria:**
        *   The UI displays input fields for all text inputs defined in FR-2.
        *   I can type freely into each field.
        *   A dropdown menu is provided for "Brand Tone" with predefined options (e.g., Playful, Luxurious, Professional, Witty, Eco-conscious).

*   **Story 2: Generate Copy**
    *   **As a** user (Ben the Marketer),
    *   **I want** to click a single button to generate all the copy I need,
    *   **so that** I can get results quickly without a complex process.
    *   **Acceptance Criteria:**
        *   A clearly labeled "Generate Copy" button is visible on the screen.
        *   Clicking the button triggers a call to the LLM backend.
        *   A loading indicator is displayed while the generation is in progress.

*   **Story 3: Review and Use Generated Content**
    *   **As a** user (Maria the Freelancer),
    *   **I want** to see all the generated captions, hashtags, and CTAs clearly laid out,
    *   **so that** I can easily review them, copy what I need, and paste it into my social media scheduler.
    *   **Acceptance Criteria:**
        *   The results are displayed in a dedicated output area, separate from the inputs.
        *   The 3 caption variants are clearly numbered or separated.
        *   A "Copy" button exists for each caption, for the block of hashtags, and for the block of CTAs.
        *   Clicking a "Copy" button copies the corresponding text to the system clipboard.

*   **Story 4: Export Results**
    *   **As a** user (Ben the Marketer),
    *   **I want** to download all the generated text content in a single file,
    *   **so that** I can save it for later or easily share it with a client.
    *   **Acceptance Criteria:**
        *   A "Download Results" button is available in the output area.
        *   Clicking it triggers the download of a `.txt` file.
        *   The file contains all 3 captions, the hashtags, and the CTAs, clearly labeled.

*   **Story 5: Generate Copy from an Image**
    *   **As a** user (Sarah the Solopreneur),
    *   **I want** to upload a photo of my product to generate copy,
    *   **so that** I can create marketing content quickly without having to describe the product in detail manually.
    *   **Acceptance Criteria:**
        *   The UI provides a clear "Upload Image" button or drag-and-drop area.
        *   After I select a valid image, a thumbnail preview is shown.
        *   If I upload an invalid file (not JPG/PNG or >5MB), an immediate error message appears.
        *   I can click "Generate Copy" with only an image uploaded and receive relevant results.
        *   The generated captions, hashtags, and CTAs are displayed in the same format as the text-only generation.

## 6. Input and Output Specifications

### 6.1. Input Details

*   **Product Title:** `text`, max 150 chars.
*   **Product Category:** `text`, max 100 chars.
*   **Key Features/Description:** `text`, max 1000 chars. Rich context for the AI.
*   **Promotion/Discount:** `text` (optional), max 100 chars. E.g., "20% off this week".
*   **Brand Tone:** `dropdown selection`. (See Story 1 AC).
*   **Target Audience:** `text` (optional), max 200 chars. E.g., "Yoga enthusiasts", "New parents".
*   **(Should-Have) Product Image:** `file upload`, `.jpg`, `.png`, max 5MB.
*   **(Should-Have) CSV Input:** `file upload`, `.csv`. Must contain headers matching the text input fields.

### 6.2. Output Details

The API call should return a structured object (e.g., JSON) that the UI will parse.

```json
{
  "captions": [
    "string 1",
    "string 2",
    "string 3"
  ],
  "hashtags": [
    "#hashtag1",
    "#hashtag2",
    ...
  ],
  "ctas": [
    "string 1",
    "string 2"
  ],
  "alt_text": "string" // (Should-Have)
}
```

*   **TXT Export Format:** A plain text file with clear headings.
    ```
    *** Generated Copy ***

    --- CAPTION 1 ---
    [Text of caption 1]

    --- CAPTION 2 ---
    [Text of caption 2]

    --- CAPTION 3 ---
    [Text of caption 3]

    --- HASHTAGS ---
    #hashtag1 #hashtag2 #hashtag3

    --- CTAs ---
    - CTA 1
    - CTA 2
    ```
*   **(Should-Have) CSV Export Format:** A CSV file with headers for each content type.

## 7. Risks and Mitigations

*   **Risk: Misleading or Inaccurate Claims.**
    *   **Mitigation:** The UI will include a clear disclaimer: "AI-generated content. Please review all claims for accuracy before posting." The core prompt will explicitly instruct the model not to invent features or benefits not present in the input.
*   **Risk: Brand Voice Drift.**
    *   **Mitigation:** Using a "Brand Tone" dropdown provides a strong guiding parameter. Prompt engineering will emphasize adherence to this tone.
*   **Risk: Privacy of Uploaded Images/Data.**
    *   **Mitigation:** The application will be stateless. No user data or images will be stored on the server. The UI will state: "Your data is processed and immediately discarded." We must also review the terms of the chosen LLM API for their data handling policies.
*   **Risk: Prompt Injection.**
    *   **Mitigation:** For the MVP, we will rely on basic input sanitization. Since the output is reviewed by the user before posting, the risk of a malicious actor hijacking their social media account is low. This is a higher concern for future versions with direct posting.
*   **Risk: Compliance/Legal (e.g., FTC disclosure rules).**
    *   **Mitigation:** Add a "Tip" in the UI: "Remember to add #ad or #sponsored if this is a paid promotion." We are a tool provider; the user is ultimately responsible for their posts.

## 8. Success Metrics for MVP

How we know if we've built something useful:

1.  **Task Completion Rate:** >90% of users who start a generation successfully export or copy their content.
2.  **Time to-Value:** The median time from landing on the page to first content export is < 90 seconds.
3.  **Qualitative Feedback (User Satisfaction):** A simple "Was this helpful? (Yes/No)" poll in the UI. We aim for >80% "Yes" responses.
4.  **Content Reuse Rate (Post-MVP):** In user interviews, determine the percentage of generated content that users post with minimal or no edits. This is a key measure of quality.
