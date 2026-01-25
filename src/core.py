from dataclasses import dataclass
from typing import List, Optional
import json
import base64
from .client import GeminiClient, APIError

# --- Data Models ---

@dataclass
class ProductInput:
    """Input data for copy generation. Text fields are optional if an image is provided."""
    brand_tone: Optional[str] = None # Still required from UI, but optional here
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    promotion: Optional[str] = None
    target_audience: Optional[str] = None

@dataclass
class GeneratedCopy:
    """Structured output from the generation service."""
    captions: List[str]
    hashtags: List[str]
    ctas: List[str]

# --- Custom Exception ---

class GenerationError(Exception):
    """Raised for errors during the copy generation process."""
    pass

# --- Helper Functions ---

def format_results_for_txt(copy: GeneratedCopy) -> str:
    """Formats the GeneratedCopy object into a string for .txt export."""
    lines = ["*** Generated Copy ***\n"]
    
    for i, caption in enumerate(copy.captions, 1):
        lines.append(f"--- CAPTION {i} ---")
        lines.append(caption)
        lines.append("") # Add a blank line

    lines.append("--- HASHTAGS ---")
    lines.append(" ".join(copy.hashtags))
    lines.append("")

    lines.append("--- CTAs ---")
    for cta in copy.ctas:
        lines.append(f"- {cta}")
    
    return "\n".join(lines)


# --- Service Layer ---

def build_prompt(data: ProductInput) -> str:
    """
    Constructs the final text prompt to be sent to the LLM.
    Handles optional fields gracefully.
    """
    prompt_lines = [
        "You are an expert Instagram copywriter. Given the following product details (and/or an image), generate 3 unique Instagram captions, 10 relevant hashtags, and 2 calls-to-action.",
        "If an image is the primary input, focus on visually descriptive and engaging copy. If text details are provided, use them to inform the tone and content.",
        "Return the output as a single, minified JSON object with keys: \"captions\" (a list of 3 strings), \"hashtags\" (a list of 10 strings), and \"ctas\" (a list of 2 strings).",
    ]
    
    details_added = False
    details_section = ["\n--- PRODUCT DETAILS ---"]
    if data.title:
        details_section.append(f"Title: {data.title}")
        details_added = True
    if data.category:
        details_section.append(f"Category: {data.category}")
        details_added = True
    if data.description:
        details_section.append(f"Description: {data.description}")
        details_added = True
    if data.brand_tone:
        details_section.append(f"Brand Tone: {data.brand_tone}")
        details_added = True
    if data.promotion:
        details_section.append(f"Current Promotion: {data.promotion}")
        details_added = True
    if data.target_audience:
        details_section.append(f"Target Audience: {data.target_audience}")
        details_added = True

    # Only add the details section if at least one detail was present
    if details_added:
        prompt_lines.extend(details_section)
    
    return "\n".join(prompt_lines)


def generate_copy_from_input(
    data: ProductInput, 
    image_bytes: Optional[bytes] = None, 
    image_mime_type: Optional[str] = None
) -> GeneratedCopy:
    """
    Orchestrates the copy generation process, now with optional image input.

    Args:
        data: The structured product input.
        image_bytes: Optional raw bytes of the image file.
        image_mime_type: Optional MIME type of the image file.

    Returns:
        A GeneratedCopy object with the AI-generated content.

    Raises:
        GenerationError: If the generation process fails at any step.
    """
    try:
        prompt = build_prompt(data)
        client = GeminiClient()

        image_b64_data = None
        if image_bytes and image_mime_type:
            # The API expects a base64-encoded string
            image_b64_data = base64.b64encode(image_bytes).decode('utf-8')

        response = client.generate(
            prompt, 
            image_b64_data=image_b64_data, 
            image_mime_type=image_mime_type
        )
        
        # The Gemini API returns JSON in the text of the first candidate's content part
        if not (response.get('candidates') and response['candidates'][0].get('content') and response['candidates'][0]['content'].get('parts')):
            raise GenerationError("Invalid API response structure: missing candidates or content.")

        response_text = response['candidates'][0]['content']['parts'][0]['text']
        
        # Clean the response text to ensure it's valid JSON
        # The model sometimes wraps the JSON in ```json ... ```
        if response_text.strip().startswith("```json"):
            response_text = response_text.strip()[7:-3].strip()
            
        data_dict = json.loads(response_text)

        return GeneratedCopy(
            captions=data_dict.get("captions", []),
            hashtags=data_dict.get("hashtags", []),
            ctas=data_dict.get("ctas", []),
        )

    except APIError as e:
        # Re-raise API errors as a more specific GenerationError
        raise GenerationError(f"API communication failed: {e}")
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        # Catch errors from parsing the expected structure
        raise GenerationError(f"Failed to parse or find data in API response: {e}")
    except Exception as e:
        # Catch any other unexpected errors
        raise GenerationError(f"An unexpected error occurred during generation: {e}")
