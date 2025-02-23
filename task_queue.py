import os
import sys
import logging
from dotenv import load_dotenv
from celery import Celery
from celery.utils.log import get_logger
from celery.exceptions import Retry
from requests.exceptions import HTTPError, ConnectionError, Timeout
from agents.project_manager import handle_project  # Ensure this import works

# Load environment variables
load_dotenv()

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = get_logger(__name__)

# Ensure project path is accessible for Celery workers
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize Celery with environment variables
celery_app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
)

# Celery Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,  # Tasks acknowledged after completion
    worker_prefetch_multiplier=1,  # Fair task distribution
    broker_connection_retry_on_startup=True,  # Retry broker connection on startup
)

@celery_app.task(bind=True, autoretry_for=(ConnectionError, Timeout), retry_backoff=True, retry_backoff_max=60, retry_jitter=True)
def process_prompt(self, prompt: str):
    """
    Celery task to process a prompt using the project manager agent.
    Uses Google Gemini API instead of OpenAI.
    Includes automatic retries for transient errors like network issues.
    """
    try:
        logger.info(f"📩 Received prompt: {prompt}")

        # Ensure handle_project is properly implemented
        result = handle_project(prompt)
        
        logger.info(f"✅ Processing completed. Result: {result}")
        return result

    except (ConnectionError, Timeout) as e:
        logger.error(f"⚠️ Network issue detected: {str(e)}. Retrying...", exc_info=True)
        raise self.retry(exc=e)  # Retry only for transient errors

    except HTTPError as e:
        logger.error(f"❌ API Error: {str(e)}", exc_info=True)
        return {"error": "API request failed", "details": str(e)}

    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}", exc_info=True)
        return {"error": "Unexpected error occurred", "details": str(e)}
