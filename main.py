from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.github_client import GitHubClient
from app.error_handler import handle_error
from app.errors import AppError
from app.auth import exchange_code_for_token, get_github_user

# ======== DEV IMPORTS SETUP ========
from app.config import (
    GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO,
    SESSION_SECRET, FRONTEND_URL
)
# from dev_modules.dev_cors import * # for dev porpoises only, allows all CORS. Remove for production!
# ========== END DEV IMPORTS SETUP ========


app = FastAPI()

# ======== DEV SETUP ========
# allow_all_cors(app) # for dev porpoises only, allows all CORS. Remove for production!
# ========== END DEV SETUP ========

origins = [
    "https://github-issue-tracker-frontend.onrender.com",  #backend-link
    "http://localhost:5173",          # allow local dev (Vite default port)
]

# Add SessionMiddleware FIRST (middleware runs in reverse order, so this executes AFTER CORS)
app.add_middleware(
    SessionMiddleware, 
    secret_key=SESSION_SECRET,
    session_cookie="session",
    max_age=14 * 24 * 60 * 60,  # 14 days
    same_site="none",  # Allow cross-domain
    https_only=True    # Required for same_site=none (use False for local dev)
)

# Add CORS LAST so it executes FIRST and sets headers before session cookie is read
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],    # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],    # Allow all headers
)

# Include your routes

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

@app.get("/auth/callback")
async def auth_callback(code: str, request: Request):
    """Handle GitHub OAuth callback"""
    try:
        # Exchange code for access token
        access_token = await exchange_code_for_token(code)
        
        # Get user info
        user_info = await get_github_user(access_token)
        
        # Store in session
        request.session["access_token"] = access_token
        request.session["user"] = {
            "login": user_info["login"],
            "name": user_info.get("name"),
            "avatar_url": user_info["avatar_url"],
            "id": user_info["id"]
        }
        
        # Redirect back to frontend with success flag
        return RedirectResponse(url=f"{FRONTEND_URL}?login=success")
    
    except Exception as e:
        print(f"OAuth error: {e}")
        return RedirectResponse(url=f"{FRONTEND_URL}?error=auth_failed")

@app.get("/auth/status")
async def auth_status(request: Request):
    """Check if user is authenticated"""
    user = request.session.get("user")
    if user:
        return {"authenticated": True, "user": user}
    return {"authenticated": False}

@app.post("/auth/logout")
async def logout(request: Request):
    """Logout user"""
    request.session.clear()
    return {"message": "Logged out successfully"}

@app.get("/issues")
async def list_issues(request: Request, force_refresh: bool = False):
    # Verify user is authenticated
    if "access_token" not in request.session:
        raise AppError(
            message="Authentication required. Please log in.",
            status_code=401,
            code="unauthorized"
        )
    
    try:
        """
        Retun all issues from github repo
        """
        issues = await github_client.get_issues(GITHUB_OWNER, GITHUB_REPO, force_refresh=force_refresh)
        return issues
    except Exception as e:
        raise handle_error(e)

@app.post("/issues")
async def create_issue(request: Request, issue: dict):
    # Verify user is authenticated
    if "access_token" not in request.session:
        raise AppError(
            message="Authentication required. Please log in.",
            status_code=401,
            code="unauthorized"
        )
    
    try:
        """
        Create an issue in the github repo with the provided data.
        """
        created_issue = await github_client.create_issue(GITHUB_OWNER, GITHUB_REPO, issue)
        return created_issue
    except Exception as e:
        raise handle_error(e)