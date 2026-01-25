import streamlit as st
from src.core import ProductInput, GeneratedCopy, generate_copy_from_input, GenerationError, format_results_for_txt
from st_copy import copy_button

st.set_page_config(page_title="E-commerce Copywriting Tool", layout="centered")

st.title("🛍️ E-commerce Copywriting Tool")
st.markdown("Generate on-brand Instagram captions, hashtags, and CTAs in seconds!")

# --- Session State Initialization ---
if 'generated_copy' not in st.session_state:
    st.session_state.generated_copy = None

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

# --- Form Submission & Results Display ---
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
                # Store results in session state
                st.session_state.generated_copy = generate_copy_from_input(product_input)
            except GenerationError as e:
                st.session_state.generated_copy = None # Clear previous results on error
                st.error(f"Failed to generate copy: {e}")

# --- Display Area (if results exist) ---
if st.session_state.generated_copy:
    results = st.session_state.generated_copy
    
    st.subheader("✅ Here's your generated copy!")
    st.markdown("---")

    # Download Button
    st.download_button(
        label="⬇️ Download All as TXT",
        data=format_results_for_txt(results),
        file_name="copy_results.txt",
        mime="text/plain"
    )

    st.markdown("---")
    st.markdown("### 📢 Captions")
    for i, caption in enumerate(results.captions, 1):
        st.text_area(f"Caption Option {i}", caption, height=100, key=f"caption_{i}")
        copy_button(caption, tooltip=f"Copy Caption {i}", key=f"copy_caption_{i}")

    st.markdown("---")
    st.markdown("### #️⃣ Hashtags")
    hashtag_str = " ".join(results.hashtags)
    st.info(hashtag_str)
    copy_button(hashtag_str, tooltip="Copy Hashtags", key="copy_hashtags")
    
    st.markdown("---")
    st.markdown("### 👉 Calls to Action (CTAs)")
    cta_display_list = [f"- {cta}" for cta in results.ctas]
    cta_copy_str = "\n".join(cta_display_list)
    st.markdown(cta_copy_str)
    copy_button(cta_copy_str, tooltip="Copy CTAs", key="copy_ctas")