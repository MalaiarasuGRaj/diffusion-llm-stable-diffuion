import streamlit as st
import requests
import io
from PIL import Image
import json

def generate_image_stable_diffusion(prompt, hf_token=None):
    """
    Generate image using Hugging Face Stable Diffusion API
    """
    if not hf_token:
        st.error("Please provide your Hugging Face token in the .env file")
        return None
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "num_inference_steps": 50,
            "guidance_scale": 7.5,
            "width": 1280,
            "height": 720
        }
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            return image
        elif response.status_code == 503:
            st.warning("Model is loading, please wait a few seconds and try again...")
            return None
        else:
            error_msg = response.text
            try:
                error_data = json.loads(error_msg)
                if "error" in error_data:
                    st.error(f"API Error: {error_data['error']}")
                else:
                    st.error(f"HTTP {response.status_code}: {error_msg}")
            except:
                st.error(f"HTTP {response.status_code}: {error_msg}")
            return None
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None
