from celery.result import AsyncResult
from services.task_queue import celery_app  # Import your Celery app instance

# Replace with your actual task ID
task_id = "c6b597de-7532-46ac-9ff6-e4c60f41b158"
result = AsyncResult(task_id, app=celery_app)

# Print Task Status and Result
print("Task Status:", result.status)
print("Task Result:", result.result)

