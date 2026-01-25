from dataclasses import dataclass
from typing import List, Optional
import json
from .client import GeminiClient, APIError

# --- Data Models ---

@dataclass
class ProductInput:
    """Input data for copy generation."""
    title: str
    category: str
    description: str
    brand_tone: str
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

# --- Service Layer ---

def build_prompt(data: ProductInput) -> str:
    """
    Constructs the final text prompt to be sent to the LLM.
    """
    prompt_lines = [
        "You are an expert Instagram copywriter. Given the following product details, generate 3 unique Instagram captions, 10 relevant hashtags, and 2 calls-to-action.",
        "Return the output as a single, minified JSON object with keys: \"captions\" (a list of 3 strings), \"hashtags\" (a list of 10 strings), and \"ctas\" (a list of 2 strings).",
        "\n--- PRODUCT DETAILS ---",
        f"Title: {data.title}",
        f"Category: {data.category}",
        f"Description: {data.description}",
        f"Brand Tone: {data.brand_tone}",
    ]
    if data.promotion:
        prompt_lines.append(f"Current Promotion: {data.promotion}")
    if data.target_audience:
        prompt_lines.append(f"Target Audience: {data.target_audience}")
    
    return "\n".join(prompt_lines)


def generate_copy_from_input(data: ProductInput) -> GeneratedCopy:
    """
    Orchestrates the copy generation process.

    Args:
        data: The structured product input.

    Returns:
        A GeneratedCopy object with the AI-generated content.

    Raises:
        GenerationError: If the generation process fails at any step.
    """
    try:
        prompt = build_prompt(data)
        client = GeminiClient()
        response = client.generate(prompt)
        
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