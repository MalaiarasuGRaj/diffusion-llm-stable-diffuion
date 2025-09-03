import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Use st.cache_resource to load the model and tokenizer only once
@st.cache_resource
def load_gemma_model(hf_token):
    """
    Loads the Gemma model and tokenizer from Hugging Face.
    Caches the model and tokenizer to avoid reloading on every run.
    """
    model_name = "google/gemma-2b-it"
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
        # The model is loaded in float16 to save memory and is mapped to the GPU if available
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            token=hf_token,
        )
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading Gemma model: {e}")
        return None, None

def generate_text_gemma(prompt, hf_token):
    """
    Generates text using the Gemma model.
    """
    tokenizer, model = load_gemma_model(hf_token)
    if not tokenizer or not model:
        st.error("Model and/or tokenizer not loaded. Cannot generate text.")
        return "Error: Model not loaded."

    # Format the prompt for Gemma's instruction-tuned model
    chat = [{"role": "user", "content": prompt}]
    formatted_prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=256, do_sample=True, temperature=0.7)
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Clean up the output to only show the model's response
    return generated_text.split("<start_of_turn>model\n")[-1]