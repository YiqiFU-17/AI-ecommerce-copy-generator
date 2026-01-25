import pytest
from src.core import (
    ProductInput,
    GeneratedCopy,
    build_prompt,
    generate_copy_from_input,
    GenerationError,
)
from src.client import APIError
import json

# --- Fixtures ---

@pytest.fixture
def basic_product_input():
    """A fixture for a basic ProductInput object without optional fields."""
    return ProductInput(
        title="Ceramic Mug",
        category="Kitchenware",
        description="A beautiful handcrafted mug.",
        brand_tone="Minimalist",
    )

@pytest.fixture
def full_product_input():
    """A fixture for a ProductInput object with all fields populated."""
    return ProductInput(
        title="Ceramic Mug",
        category="Kitchenware",
        description="A beautiful handcrafted mug.",
        brand_tone="Minimalist",
        promotion="20% off",
        target_audience="Coffee lovers",
    )

@pytest.fixture
def mock_gemini_response():
    """A fixture for a valid Gemini API JSON response."""
    return {
        "candidates": [{
            "content": {
                "parts": [{
                    "text": json.dumps({
                        "captions": ["Caption 1", "Caption 2", "Caption 3"],
                        "hashtags": ["#mug", "#coffee", "#handmade", "#ceramics", "#shoplocal", "#giftidea", "#coffeelover", "#morningcoffee", "#pottery", "#homedecor"],
                        "ctas": ["Shop now!", "Link in bio."]
                    })
                }]
            }
        }]
    }

# --- Tests for build_prompt ---

def test_build_prompt_basic(basic_product_input):
    """Tests that the prompt includes required fields correctly."""
    prompt = build_prompt(basic_product_input)
    assert "Title: Ceramic Mug" in prompt
    assert "Brand Tone: Minimalist" in prompt
    assert "Current Promotion" not in prompt
    assert "Target Audience" not in prompt

def test_build_prompt_with_optionals(full_product_input):
    """Tests that the prompt includes optional fields when provided."""
    prompt = build_prompt(full_product_input)
    assert "Title: Ceramic Mug" in prompt
    assert "Brand Tone: Minimalist" in prompt
    assert "Current Promotion: 20% off" in prompt
    assert "Target Audience: Coffee lovers" in prompt

# --- Tests for generate_copy_from_input ---

def test_generate_copy_from_input_success(mocker, full_product_input, mock_gemini_response):
    """Tests a successful generation path."""
    mocker.patch("src.core.GeminiClient.generate", return_value=mock_gemini_response)
    
    result = generate_copy_from_input(full_product_input)
    
    assert isinstance(result, GeneratedCopy)
    assert len(result.captions) == 3
    assert result.captions[0] == "Caption 1"
    assert len(result.hashtags) == 10
    assert result.hashtags[0] == "#mug"

def test_generate_copy_from_input_handles_markdown_wrapper(mocker, full_product_input, mock_gemini_response):
    """Tests that the service correctly handles JSON wrapped in markdown code fences."""
    # Modify the response text to include markdown
    mock_gemini_response["candidates"][0]["content"]["parts"][0]["text"] = f"```json\n{mock_gemini_response['candidates'][0]['content']['parts'][0]['text']}\n```"
    mocker.patch("src.core.GeminiClient.generate", return_value=mock_gemini_response)
    
    result = generate_copy_from_input(full_product_input)
    assert isinstance(result, GeneratedCopy)
    assert len(result.captions) == 3

def test_generate_copy_from_input_raises_on_api_error(mocker, full_product_input):
    """Tests that an APIError from the client is wrapped in a GenerationError."""
    mocker.patch("src.core.GeminiClient.generate", side_effect=APIError("403 Forbidden"))
    
    with pytest.raises(GenerationError, match="API communication failed: 403 Forbidden"):
        generate_copy_from_input(full_product_input)

def test_generate_copy_from_input_raises_on_invalid_json(mocker, full_product_input):
    """Tests that an invalid JSON response raises a GenerationError."""
    invalid_response = {
        "candidates": [{"content": {"parts": [{"text": "this is not json"}]}}]
    }
    mocker.patch("src.core.GeminiClient.generate", return_value=invalid_response)
    
    with pytest.raises(GenerationError, match="Failed to parse or find data in API response"):
        generate_copy_from_input(full_product_input)

def test_generate_copy_from_input_raises_on_missing_structure(mocker, full_product_input):
    """Tests that a response with missing keys raises a GenerationError."""
    malformed_response = {"candidates": []} # Missing the nested structure
    mocker.patch("src.core.GeminiClient.generate", return_value=malformed_response)
    
    with pytest.raises(GenerationError, match="Invalid API response structure"):
        generate_copy_from_input(full_product_input)

