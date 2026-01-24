import streamlit as st
from src.core import ProductInput

st.set_page_config(page_title="E-commerce Copywriting Tool", layout="centered")

st.title("🛍️ E-commerce Copywriting Tool")
st.markdown("Generate on-brand Instagram captions, hashtags, and CTAs in seconds!")

# Brand tone options for the selectbox
BRAND_TONES = [
    "Playful", "Luxurious", "Professional", "Witty", "Eco-conscious", "Inspirational",
    "Informative", "Direct", "Friendly", "Bold"
]

with st.form("copy_generation_form"):
    st.header("Product Details")
    product_title = st.text_input(
        "Product Title",
        placeholder="e.g., Handcrafted Ceramic Mug",
        help="A concise name for your product."
    )
    product_category = st.text_input(
        "Product Category",
        placeholder="e.g., Home Goods, Kitchenware",
        help="What type of product is it?"
    )
    product_description = st.text_area(
        "Key Features / Description",
        placeholder="e.g., 'Dishwasher safe, unique speckled glaze, ergonomic handle. Perfect for morning coffee.'",
        help="Describe your product's key features, benefits, and unique selling points."
    )
    promotion = st.text_input(
        "Promotion / Discount (Optional)",
        placeholder="e.g., '20% off for a limited time', 'Free shipping on orders over $50'",
        help="Any special offers or discounts?"
    )
    brand_tone = st.selectbox(
        "Brand Tone",
        options=BRAND_TONES,
        help="Select the desired tone for your Instagram copy."
    )
    target_audience = st.text_input(
        "Target Audience (Optional)",
        placeholder="e.g., 'Coffee lovers, remote workers', 'Sustainable living enthusiasts'",
        help="Who are you trying to reach with this post?"
    )

    submitted = st.form_submit_button("Generate Copy")

    if submitted:
        if not product_title or not product_description or not product_category:
            st.error("Please fill in Product Title, Category, and Description.")
        else:
            # For now, just display the collected data
            # In later stories, this will trigger the AI generation
            product_input = ProductInput(
                title=product_title,
                category=product_category,
                description=product_description,
                brand_tone=brand_tone,
                promotion=promotion if promotion else None,
                target_audience=target_audience if target_audience else None
            )
            st.success("Form submitted successfully! Collected Data:")
            st.json(product_input.__dict__)