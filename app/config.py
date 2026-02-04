import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")
if not GITHUB_TOKEN or not GITHUB_REPO:
    raise ValueError("GITHUB_TOKEN and GITHUB_REPO must be set in the .env file")