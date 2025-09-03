import streamlit as st
import requests
import io
import time
import os
from dotenv import load_dotenv
from src.page_config import set_page_config
from src.stable_diffusion import generate_image_stable_diffusion
from src.gemma import load_gemma_model, generate_text_gemma
from src.sidebar import render_sidebar

# Load environment variables
load_dotenv()

# Set page config from external file
set_page_config()

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def ui_image_generation(hf_token):
    """Handles the UI and logic for the Image Generation mode."""
    st.subheader("🖼️ Image Generation Mode")
    st.markdown("""
    <div class="mode-description">
        How it works: Enter any descriptive text prompt and the Stable Diffusion XL model will generate a high-quality image that visually represents your prompt.

        Examples of good prompts:
            - A serene mountain landscape at sunset, vibrant colors, photorealistic
            - Cyberpunk city street with neon lights and flying cars, digital art
            - Portrait of a futuristic astronaut on an alien planet, cinematic lighting
    </div>
    """, unsafe_allow_html=True)
    
    prompt = st.text_area(
        "Enter your image prompt:",
        placeholder="Describe the image you want to generate...",
        height=100,
        key="image_prompt"
    )

    if st.button("🎨 Generate Image", type="primary"):
        if prompt:
            with st.spinner("Generating image... This may take 30-60 seconds."):
                image = generate_image_stable_diffusion(prompt.strip(), hf_token)
                if image:
                    st.success("Image generated successfully!")
                    st.image(image, caption=f"Generated: {prompt.strip()}", use_column_width='auto')
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    st.download_button(
                        label="📥 Download Image",
                        data=buf.getvalue(),
                        file_name=f"generated_image_{int(time.time())}.png",
                        mime="image/png"
                    )
        else:
            st.warning("Please enter a prompt to generate an image.")

def ui_text_generation(hf_token):
    """Handles the UI and logic for the Text Generation mode."""
    st.subheader("✍️ Text Generation Mode")
    st.markdown("""
    <div class="mode-description">
        How it works: Enter any question or instruction and the Google Gemma model will provide a text-based response.
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading Gemma model... This might take a moment on first run."):
        gemma_tokenizer, gemma_model = load_gemma_model(hf_token)

    if not gemma_tokenizer or not gemma_model:
        st.error("Could not load the text generation model. Please check the logs.")
        return

    prompt = st.text_area("Enter your text prompt:", placeholder="Ask a question or give an instruction...", height=100, key="text_prompt")

    if st.button("✍️ Generate Text", type="primary"):
        if prompt:
            with st.spinner("Generating text..."):
                response = generate_text_gemma(prompt.strip(), gemma_tokenizer, gemma_model)
                st.success("Text generated successfully!")
                st.markdown(response)
        else:
            st.warning("Please enter a prompt to generate text.")

# Main app
def main():
    load_css("style.css")
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    
    st.markdown('<h1 class="main-header">🎨 Diffusion LLM - PoC</h1>', unsafe_allow_html=True)
    
    if not hf_token:
        st.markdown("""
        <div class="error-box">
            <h4>⚠️ Configuration Required</h4>
            <p>Please add your Hugging Face token to the .env file to use this application.</p>
            <p>Create a .env file in the same directory as this app with:</p>
            <code>HUGGINGFACE_TOKEN=your_token_here</code>
            <p>Get your token from: <a href="https://huggingface.co/settings/tokens" target="_blank">https://huggingface.co/settings/tokens</a></p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Sidebar
    render_sidebar()

    # Mode selection
    mode = st.radio(
        "Choose your generation mode:",
        ("🖼️ Image Generation", "✍️ Text Generation"),
        horizontal=True,
        key="mode_selection"
    )

    # --- Image Generation Mode ---
    if mode == "🖼️ Image Generation":
        ui_image_generation(hf_token)

    # --- Text Generation Mode ---
    elif mode == "✍️ Text Generation":
        ui_text_generation(hf_token)

if __name__ == "__main__":
    main()