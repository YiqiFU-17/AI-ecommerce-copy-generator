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
import base64

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

def test_build_prompt_image_only(mocker):
    """Tests that the prompt does not include empty details for an image-only scenario."""
    # Input has no text fields, which simulates an image-only submission
    image_only_input = ProductInput(brand_tone="Witty")
    
    prompt = build_prompt(image_only_input)
    
    # Check that the main instruction is there
    assert "You are an expert Instagram copywriter" in prompt
    # Crucially, check that the prompt does NOT contain labels for empty fields
    assert "Title:" not in prompt
    assert "Category:" not in prompt
    assert "Description:" not in prompt
    # It should still contain the brand tone, as that is always selected in the UI
    assert "Brand Tone: Witty" in prompt
    # Check that the whole details section header is there, since tone is present
    assert "--- PRODUCT DETAILS ---" in prompt

def test_build_prompt_no_details_at_all(mocker):
    """Tests that the details section is omitted entirely if no data is present."""
    no_details_input = ProductInput() # Absolutely nothing provided
    prompt = build_prompt(no_details_input)
    assert "--- PRODUCT DETAILS ---" not in prompt

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

# --- New Tests for Multimodal ---

def test_generate_copy_from_input_with_image(mocker, full_product_input, mock_gemini_response):
    """Tests that the service calls the client with base64-encoded image data."""
    mock_generate = mocker.patch("src.core.GeminiClient.generate", return_value=mock_gemini_response)
    
    # Create some dummy image data
    image_bytes = b"dummy_image_bytes"
    image_mime_type = "image/png"
    expected_b64_data = base64.b64encode(image_bytes).decode('utf-8')
    
    generate_copy_from_input(
        full_product_input,
        image_bytes=image_bytes,
        image_mime_type=image_mime_type
    )
    
    mock_generate.assert_called_once()
    # Check the keyword arguments passed to the generate method
    call_args = mock_generate.call_args.kwargs
    assert call_args['image_b64_data'] == expected_b64_data
    assert call_args['image_mime_type'] == image_mime_type

def test_generate_copy_from_input_text_only_path(mocker, full_product_input, mock_gemini_response):
    """Tests the service path when no image is provided, ensuring kwargs are None."""
    mock_generate = mocker.patch("src.core.GeminiClient.generate", return_value=mock_gemini_response)
    
    generate_copy_from_input(full_product_input) # No image args passed
    
    mock_generate.assert_called_once()
    # Check the keyword arguments passed to the generate method
    call_args = mock_generate.call_args.kwargs
    assert call_args['image_b64_data'] is None
    assert call_args['image_mime_type'] is None

