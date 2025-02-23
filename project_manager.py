from agents.designer_agent import generate_ui
from agents.developer_agent import generate_code
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_project(prompt: str):
    """
    Handles the AI project generation based on the given prompt.
    Calls UI generation and code generation agents.
    Uses Google Gemini API instead of OpenAI.
    """
    try:
        logger.info(f"🚀 Processing project for prompt: {prompt}")

        # Generate UI design
        ui_design = None
        try:
            ui_design = generate_ui(prompt)
            if ui_design:
                logger.info("✅ UI design generated successfully.")
            else:
                logger.warning("⚠️ UI generation returned empty response.")
        except Exception as ui_error:
            logger.error(f"❌ UI generation failed: {str(ui_error)}", exc_info=True)

        # Generate Code
        code = None
        try:
            code = generate_code(prompt)
            if code:
                logger.info("✅ Code generation completed.")
            else:
                logger.warning("⚠️ Code generation returned empty response.")
        except Exception as code_error:
            logger.error(f"❌ Code generation failed: {str(code_error)}", exc_info=True)

        # Check if both UI and code failed
        if ui_design is None and code is None:
            return {"error": "Both UI and code generation failed."}
        
        return {"ui": ui_design, "code": code}

    except Exception as e:
        logger.error(f"🔥 Critical error in handle_project: {str(e)}", exc_info=True)
        return {"error": str(e)}
