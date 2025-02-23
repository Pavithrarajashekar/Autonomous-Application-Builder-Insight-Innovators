from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import google.generativeai as genai
import os
import logging
import datetime
import re

# Configure Google Gemini API Key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ Missing GEMINI_API_KEY! Set it in your environment variables.")

genai.configure(api_key=API_KEY)

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable CORS (Allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model with validation
class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=5, description="Prompt should be at least 5 characters long")

# Function to process the prompt with Gemini API
def process_prompt_sync(prompt: str):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            generated_text = response.text.strip()

            # Extract description and code separately
            description = generated_text
            extracted_code = None

            if "```" in generated_text:  # Check if code block exists
                parts = generated_text.split("```")
                description = parts[0].strip()  # Text before code block
                extracted_code = parts[1].strip() if len(parts) > 1 else None

            logger.info(f"🤖 AI Response:\n{generated_text}")

            return {
                "status": "success",
                "data": {
                    "app_name": "AI-Generated App",
                    "description": description if description else "No description provided.",
                    "code": extracted_code if extracted_code else "No code generated."
                }
            }
        else:
            logger.warning("⚠️ Invalid response format from Gemini API.")
            return {
                "status": "error",
                "message": "Invalid response from Gemini API"
            }

    except Exception as e:
        logger.error(f"🔥 AI Processing Error: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"Error processing request: {str(e)}"
        }

@app.post("/generate-app/")
async def generate_app(request: PromptRequest):
    """
    API endpoint to process a prompt synchronously.
    """
    try:
        timestamp = datetime.datetime.utcnow().isoformat()
        logger.info(f"📩 [{timestamp}] Received request: {request.prompt}")

        # Process the request synchronously using Google Gemini
        response = process_prompt_sync(request.prompt)

        logger.info(f"✅ Response generated at {timestamp}")

        return response  # ✅ Ensure valid JSON response

    except Exception as e:
        logger.error(f"🔥 Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
