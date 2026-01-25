import streamlit as st
from src.core import ProductInput, generate_copy_from_input, GenerationError

st.set_page_config(page_title="E-commerce Copywriting Tool", layout="centered")

st.title("🛍️ E-commerce Copywriting Tool")
st.markdown("Generate on-brand Instagram captions, hashtags, and CTAs in seconds!")

# --- Form Definition ---
BRAND_TONES = [
    "Playful", "Luxurious", "Professional", "Witty", "Eco-conscious", "Inspirational",
    "Informative", "Direct", "Friendly", "Bold"
]

with st.form("copy_generation_form"):
    st.header("Product Details")
    product_title = st.text_input("Product Title", placeholder="e.g., Handcrafted Ceramic Mug")
    product_category = st.text_input("Product Category", placeholder="e.g., Home Goods, Kitchenware")
    product_description = st.text_area("Key Features / Description", placeholder="e.g., 'Dishwasher safe, unique speckled glaze...'")
    promotion = st.text_input("Promotion / Discount (Optional)", placeholder="e.g., '20% off for a limited time'")
    brand_tone = st.selectbox("Brand Tone", options=BRAND_TONES)
    target_audience = st.text_input("Target Audience (Optional)", placeholder="e.g., 'Coffee lovers, remote workers'")

    submitted = st.form_submit_button("Generate Copy")

# --- Form Submission Logic ---
if submitted:
    if not product_title or not product_description or not product_category:
        st.error("Please fill in Product Title, Category, and Description.")
    else:
        with st.spinner("Generating copy... This may take a moment."):
            try:
                product_input = ProductInput(
                    title=product_title,
                    category=product_category,
                    description=product_description,
                    brand_tone=brand_tone,
                    promotion=promotion if promotion else None,
                    target_audience=target_audience if target_audience else None
                )
                
                # Call the generation service
                generated_copy = generate_copy_from_input(product_input)

                # Display the results
                st.subheader("✅ Here's your generated copy!")

                st.markdown("---")
                st.markdown("### 📢 Captions")
                for i, caption in enumerate(generated_copy.captions, 1):
                    st.text_area(f"Caption Option {i}", caption, height=100)

                st.markdown("---")
                st.markdown("### #️⃣ Hashtags")
                st.info(" ".join(generated_copy.hashtags))
                
                st.markdown("---")
                st.markdown("### 👉 Calls to Action (CTAs)")
                for cta in generated_copy.ctas:
                    st.markdown(f"- {cta}")

            except GenerationError as e:
                st.error(f"Failed to generate copy: {e}")

