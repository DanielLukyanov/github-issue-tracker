from fastapi import FastAPI, HTTPException
from app.github_client import GitHubClient
from app.error_handler import handle_error
from app.errors import AppError

from app.config import GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO # later change to dynamic config/OAuth
from dev_modules.dev_cors import * # for dev porpoises only, allows all CORS. Remove for production!

app = FastAPI()

# ======== DEV SETUP ========
allow_all_cors(app) # for dev porpoises only, allows all CORS. Remove for production!
# ========== END DEV SETUP ========

github_client = GitHubClient(GITHUB_TOKEN)

@app.get("/")
def read_root():
    return {"message": "Hello, Github Issue Tracker!"}

@app.get("/issues")
async def list_issues():
    try:
        """
        Retun all issues from github repo
        """
        issues = await github_client.get_issues(GITHUB_OWNER, GITHUB_REPO)
        return issues
    except Exception as e:
        raise handle_error(e)
