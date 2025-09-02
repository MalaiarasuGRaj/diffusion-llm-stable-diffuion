import streamlit as st

def render_sidebar():
    st.sidebar.header("⚙️ Configuration")
    st.sidebar.success("✅ Hugging Face token loaded")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Model Information")
    st.sidebar.info("""
    **Image Generation:** Stable Diffusion XL Base 1.0
    """)
