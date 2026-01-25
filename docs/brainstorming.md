# Brainstorming & Convergence: E-commerce Copywriting Tool

**Version:** 1.0
**Status:** Scoped for MVP Implementation
**Context:** This document captures the brainstorming and convergence process for the E-commerce Copywriting Tool, aligning with PRD v1.1, Architecture v1.1, and IRR v1.0.

---

## 1. Problem Framing

### 1.1. User Pain Points & Jobs-to-be-Done (JTBD)

Based on the PRD personas (Sarah the Solopreneur, Ben the Marketer, Maria the Freelancer), the core JTBD is to **"quickly create compelling, on-brand social media copy to drive sales without creative burnout."**

*   **Pain Points:**
    *   **Time Sink:** Writing good copy takes too long.
    *   **Creative Drain:** It's hard to be consistently creative, especially for multiple products or clients.
    *   **Generic Output:** The resulting copy often lacks punch and fails to convert.
    *   **Blank Page Problem:** Just getting started is often the hardest part.

### 1.2. Why Image Input Matters

*   A picture is worth a thousand words. For physical products, an image provides rich, implicit details (color, texture, style, mood) that are tedious to describe manually.
*   **For Sarah the Solopreneur,** uploading a photo is faster than writing a detailed description.
*   **For Ben the Marketer,** it ensures the copy is grounded in the visual reality of the product.
*   **MVP Constraints:** To keep scope minimal, the MVP supports only one image (`.jpg`/`.jpeg`/`.png`), max 5MB, with no built-in editing tools.

---

## 2. Assumptions and Constraints

### 2.1. Technical Assumptions
*   **Frontend:** The app is built with Streamlit, which manages the web server and UI components.
*   **Backend:** The core logic is Python.
*   **API:** We are using the Google Gemini API, specifically the `generateContent` endpoint which supports multimodal parts (text and `inline_data`).
*   **Image Handling:** Images are not stored. They are read into memory, base64-encoded by our service layer, and sent directly to the API.
*   **Statelessness:** The application is entirely stateless. No data is persisted between sessions.
*   **Timeout:** A default 15-second timeout is enforced for API calls.

### 2.2. Product Constraints
*   **Minimal Scope:** The focus is on a single, streamlined workflow: input -> generate -> export.
*   **Unchanged Output:** The output structure (3 captions, hashtags, 2 CTAs) is fixed for the MVP, regardless of input mode (text, image, or both).

### 2.3. Compliance & Privacy
*   **Data Privacy:** No user data or images are stored on the server. A disclaimer in the UI must communicate this.
*   **Content Accuracy:** The user is ultimately responsible for the accuracy of the generated content. A disclaimer will be present in the UI.

---

## 3. Brainstorming (Idea Generation)

### Theme 1: Input Experience & UX
1.  **Image URL Input:** Allow users to paste a URL instead of uploading a file.
2.  **Image Editing:** Basic cropping/resizing before submission.
3.  **Saved Brand Profiles:** Allow users (e.g., Maria) to save and recall brand tone/audience settings.
4.  **CSV Upload:** Bulk generate copy by uploading a CSV of product details.

### Theme 2: Prompting & Quality
5.  **Negative Prompts:** Add a field for "what to avoid" in the copy.
6.  **Custom Output Structure:** Allow users to define the number of captions or CTA's.
7.  **"Regenerate" Option:** A button to re-run generation for a single caption or the entire output.
8.  **Alt-Text Generation:** Automatically generate descriptive alt-text for the uploaded image for accessibility.

### Theme 3: Safety & Compliance
9.  **Toxicity/Safety Scoring:** Use the API's safety ratings to flag potentially problematic content.
10. **Claim Detection:** Highlight potentially factual claims (e.g., "50% more effective") and remind the user to verify.

### Theme 4: Export & Workflow
11. **Multiple Export Formats:** Offer export to `.json` or `.csv` in addition to `.txt`.
12. **Post Scheduling Integration:** A (hypothetical) "Send to Buffer/Hootsuite" button.

---

## 4. Converge & Prioritize (MVP Scope)

Based on the PRD v1.1 MoSCoW and IRR v1.0 scope lock, we converge on the following:

*   **Must-Haves (IN SCOPE):**
    *   Text-only, Image-only, and Image+Text generation modes.
    *   Simple UI form for text inputs.
    *   File uploader for a single image (JPG/JPEG/PNG, <5MB).
    *   Display of results in a fixed structure (3 captions, hashtags, 2 CTAs).
    *   Copy-to-clipboard and Download-as-TXT functionality.
    *   Clear error messages for invalid uploads or API failures.

*   **Should-Haves (DEFERRED):**
    *   CSV Upload (#4)
    *   Alt-Text Generation (#8)
    *   Multiple Export Formats (#11)

*   **Could-Haves (DEFERRED):**
    *   Custom Output Structure (#6)
    *   Saved Brand Profiles (#3)

*   **Explicitly Out-of-Scope (WON'T HAVE for MVP):**
    *   Image URL Input (#1)
    *   Image Editing (#2)
    *   Negative Prompts (#5)
    *   Regenerate Option (#7)
    *   Safety Scoring/Claim Detection (#9, #10)
    *   Post Scheduling Integration (#12)
    *   User accounts, databases, or any state persistence.

---

## 5. Key Risks & Mitigations

*   **Prompt Injection:** (Low) User reviews content before use. Mitigation: Rely on user review for MVP.
*   **Hallucination/Inaccurate Claims:** (Medium) Model may invent details not in the image/text. Mitigation: UI disclaimer "Please review all claims for accuracy."
*   **Image Privacy:** (Low) User may upload sensitive images. Mitigation: UI disclaimer "Your data is processed and immediately discarded." and ensure stateless implementation.
*   **API Cost/Latency:** (Medium) Multimodal calls can be slower/more expensive. Mitigation: Enforce a 15-second timeout and display a loading spinner to manage user expectations.
*   **Model Limitations:** (Medium) Image-only generation may lack specific brand context. Mitigation: Encourage users to provide text inputs (like Brand Tone) alongside images for best results.

---

## 6. Proposed Success Metrics

*   **Task Completion Rate (>90%):** Measured by the number of successful content generations (copy/download) vs. total generation attempts. (Lightweight MVP measurement: could be simple session-based counters if possible, otherwise qualitative).
*   **Time-to-Value (<90s):** Median time from page load to first content export. (Requires analytics, deferred post-MVP).
*   **Qualitative Feedback (>80% "Yes"):** A simple "Was this helpful? (Yes/No)" poll in the UI after generation.

---

## 7. Open Questions / Decisions Needed

This section captures key decisions made to define the MVP scope.

*   **Max file size?** DECIDED: 5MB. Balances quality with performance.
*   **Accepted file types?** DECIDED: `.jpg`, `.jpeg`, `.png`. These are the most common web image formats.
*   **Is Brand Tone required for image-only?** DECIDED: Yes (UI requires it via dropdown). Image-only means only image + brand tone; other text fields optional.
*   **How to handle missing text fields?** DECIDED: All text fields are optional if an image is provided. The prompt construction logic will gracefully handle missing fields.
*   **What are the exact error messages?** DECIDED: As per PRD/Stories (e.g., "Image is too large. Please upload an image under 5MB.").

---

## 8. Next Steps

*   **Artifacts:** `prd.md`, `architecture.md`, `epics.md`, and `irr.md` are all up-to-date and serve as the source of truth.
*   **Implementation:** The work is covered by Stories 1 through 10, with the multimodal feature detailed specifically in:
    *   `docs/stories/story-009-streamlit-ui-multimodal-upload.md`
    *   `docs/stories/story-010-backend-multimodal-payload.md`
