import streamlit as st
import requests
import io
import time
import os
from dotenv import load_dotenv
from src.page_config import set_page_config
from src.stable_diffusion import generate_image_stable_diffusion
from src.sidebar import render_sidebar

# Load environment variables
load_dotenv()

# Set page config from external file
set_page_config()

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


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

    # Image generation UI
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
    
    # Input
    prompt = st.text_area(
        "Enter your image prompt:",
        placeholder="Describe the image you want to generate...",
        height=100,
        on_change=None,
        key="image_prompt"
    )

    # Detect Enter key press in text area
    generate = st.button("🎨 Generate Image", type="primary")
    enter_pressed = False
    if st.session_state.get("image_prompt") and st.session_state.get("image_prompt") != "":
        # If the prompt changed and ends with a newline, treat as Enter pressed
        if st.session_state["image_prompt"].endswith("\n"):
            enter_pressed = True

    if (generate or enter_pressed):
        if prompt:
            with st.spinner("Generating image... This may take 30-60 seconds."):
                image = generate_image_stable_diffusion(prompt.strip(), hf_token)
                if image:
                    st.success("Image generated successfully!")
                    st.image(image, caption=f"Generated: {prompt.strip()}", width='stretch')
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

if __name__ == "__main__":
    main()