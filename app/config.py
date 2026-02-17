import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass 

# Repository configuration (still needed to know which repo to access)
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")

# OAuth configuration
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
SESSION_SECRET = os.getenv("SESSION_SECRET", "githubissuetracker")

# Frontend URL for redirects
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://github-issue-tracker-frontend.onrender.com")

if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
    raise ValueError("GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET must be set for OAuth")

if not GITHUB_OWNER or not GITHUB_REPO:
    raise ValueError("GITHUB_OWNER and GITHUB_REPO must be set")