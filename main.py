from fastapi import FastAPI, HTTPException
from app.github_client import GitHubClient, GithubAPIError

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
    
    except httpx.RequestError as e:
        raise GitHubAPIError(
            status_code=503,
            message="Could not connect to GitHub API"
        )
