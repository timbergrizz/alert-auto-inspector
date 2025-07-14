import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Load configuration from environment variables
LLM_API_KEY = os.getenv("LLM_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")
DB_PATH = os.getenv("DB_PATH", "chroma_db/chroma.sqlite3")
DB_COLLECTION_NAME = os.getenv("DB_COLLECTION_NAME", "knowledge_base")

# Check if the environment variables are set
if not LLM_API_KEY:
    raise ValueError("LLM_API_KEY environment variable not set.")
if not SLACK_WEBHOOK_URL:
    raise ValueError("SLACK_WEBHOOK_URL environment variable not set.")
if not LLM_BASE_URL:
    raise ValueError("LLM_BASE_URL environment variable not set.")
