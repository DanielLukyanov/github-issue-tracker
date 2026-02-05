from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.github_client import GitHubClient
from app.error_handler import handle_error
from app.errors import AppError

# ======== DEV IMPORTS SETUP ========
from app.config import GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO # later change to dynamic config/OAuth
from dev_modules.dev_cors import * # for dev porpoises only, allows all CORS. Remove for production!
# ========== END DEV IMPORTS SETUP ========


app = FastAPI()

# ======== DEV SETUP ========
allow_all_cors(app) # for dev porpoises only, allows all CORS. Remove for production!
# ========== END DEV SETUP ========

github_client = GitHubClient(GITHUB_TOKEN)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )

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
