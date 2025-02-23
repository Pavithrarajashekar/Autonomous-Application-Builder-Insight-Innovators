import logging
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Retrieve API key
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

if not GOOGLE_GEMINI_API_KEY:
    raise ValueError("❌ Google Gemini API Key is missing! Set GOOGLE_GEMINI_API_KEY in .env")

# Configure Google Gemini API
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

def generate_ui(prompt: str):
    """
    Generates a UI component (React) based on the given prompt using Google Gemini API.
    """
    try:
        logger.info(f"Generating UI for prompt: {prompt}")

        # Use Gemini model
        model = genai.GenerativeModel("gemini-pro")  # Use "gemini-1.5-pro" if available
        response = model.generate_content(prompt)

        # Extract generated code
        ui_code = response.text if response else "⚠️ No response generated"

        logger.info("UI generation completed successfully.")
        return ui_code

    except Exception as e:
        logger.error(f"❌ Error generating UI: {str(e)}", exc_info=True)
        return "⚠️ Error generating UI"
