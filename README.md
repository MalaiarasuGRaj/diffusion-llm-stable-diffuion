# Diffusion LLM - PoC

A professional Streamlit application for generating images using Stable Diffusion XL via Hugging Face Inference API. The app is modular, always in dark mode, and supports prompt submission via Enter key or button.

## Features
- Modern dark mode UI
- Modular codebase (`src` folder for logic, sidebar, and config)
- Image generation using Stable Diffusion XL (16:9 ratio, suitable for YouTube thumbnails)
- Hugging Face API integration
- Prompt submission via Enter key or button

## Prerequisites
- Python 3.8+
- Git
- Hugging Face account and API token ([get your token](https://huggingface.co/settings/tokens))

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/MalaiarasuGRaj/diffusion-llm-stable-diffuion.git
cd diffusion-llm-stable-diffuion/codebase
```

### 2. Create and Activate a Virtual Environment (Recommended)
```sh
python -m venv .venv
.\.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Add Your Hugging Face Token
Create a `.env` file in the `codebase` directory:
```
HUGGINGFACE_TOKEN=your_huggingface_token_here
```
Get your token from [Hugging Face settings](https://huggingface.co/settings/tokens).

### 5. Run the Application
```sh
streamlit run app.py
```

## File Structure
```
codebase/
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── .env                  # Hugging Face token
├── style.css             # Custom dark mode styles
├── src/
│   ├── page_config.py    # Page configuration
│   ├── sidebar.py        # Sidebar rendering
│   └── stable_diffusion.py # Stable Diffusion API logic
```

## Troubleshooting
- **API Error: Monthly credits exceeded**: Upgrade to Hugging Face PRO or wait for next month's reset.
- **Network issues**: Ensure you have internet access and firewall/proxy allows outbound HTTPS.
- **Module import errors**: Make sure you are running from the `codebase` directory and have the correct file structure.

## License
MIT

## Credits
- [Streamlit](https://streamlit.io/)
- [Hugging Face](https://huggingface.co/)
- [Stable Diffusion XL](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)
