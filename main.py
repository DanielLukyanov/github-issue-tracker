from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.github_client import GitHubClient
from app.error_handler import handle_error
from app.errors import AppError
from app.auth import exchange_code_for_token, get_github_user
from app.config import (
    GITHUB_OWNER, GITHUB_REPO,
    SESSION_SECRET, FRONTEND_URL
)
import os

app = FastAPI()

# Production origin - your Render frontend URL
origins = [
    "https://github-issue-tracker-frontend.onrender.com",
]

# Add CORS first (executes last)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add SessionMiddleware last (executes first)
app.add_middleware(
    SessionMiddleware, 
    secret_key=SESSION_SECRET,
    session_cookie="session",
    max_age=14 * 24 * 60 * 60,
    same_site="none",  # Required for cross-origin cookies
    https_only=True    # Required when same_site="none"
)

# Initialize GitHub client WITHOUT any token
github_client = GitHubClient()

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
        access_token = await exchange_code_for_token(code)
        user_info = await get_github_user(access_token)
        
        request.session["access_token"] = access_token
        request.session["user"] = {
            "login": user_info["login"],
            "name": user_info.get("name"),
            "avatar_url": user_info["avatar_url"],
            "id": user_info["id"]
        }
        
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
    # Get user's OAuth token from session
    access_token = request.session.get("access_token")
    if not access_token:
        raise AppError(
            message="Authentication required. Please log in.",
            status_code=401,
            code="unauthorized"
        )
    
    try:
        # Pass user's OAuth token to GitHubClient
        issues = await github_client.get_issues(
            GITHUB_OWNER, 
            GITHUB_REPO, 
            token=access_token,  # ← Use user's OAuth token
            force_refresh=force_refresh
        )
        return issues
    except Exception as e:
        raise handle_error(e)

@app.post("/issues")
async def create_issue(request: Request, issue: dict):
    # Get user's OAuth token from session
    access_token = request.session.get("access_token")
    if not access_token:
        raise AppError(
            message="Authentication required. Please log in.",
            status_code=401,
            code="unauthorized"
        )
    
    try:
        # Pass user's OAuth token to GitHubClient
        created_issue = await github_client.create_issue(
            GITHUB_OWNER, 
            GITHUB_REPO, 
            token=access_token,  # ← Use user's OAuth token
            dict_issue=issue
        )
        return created_issue
    except Exception as e:
        raise handle_error(e)