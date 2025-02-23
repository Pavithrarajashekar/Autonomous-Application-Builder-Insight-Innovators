import google.generativeai as genai
import os

# Configure Gemini API Key (Ensure you set this in your environment variables)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def process_prompt_sync(prompt: str):
    try:
        model = genai.GenerativeModel("gemini-pro")  # Use the appropriate model
        response = model.generate_content(prompt)

        # Ensure we get valid AI-generated content
        if response and hasattr(response, "text"):
            return {
                "status": "success",
                "data": {
                    "app_name": "AI-Generated App",
                    "description": response.text.strip()  # Format the response properly
                }
            }
        else:
            return {
                "status": "error",
                "message": "Invalid response from Gemini API"
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error processing request: {str(e)}"
        }
