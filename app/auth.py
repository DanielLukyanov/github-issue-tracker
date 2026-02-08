import httpx
from fastapi import HTTPException
from app.config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET


async def exchange_code_for_token(code: str) -> str:
    """Exchange OAuth code for access token"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
            }
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange code for token")
        
        data = response.json()
        
        if "error" in data:
            raise HTTPException(status_code=400, detail=data.get("error_description", "OAuth error"))
        
        return data.get("access_token")


async def get_github_user(access_token: str) -> dict:
    """Get GitHub user info using access token"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid access token")
        
        return response.json()
