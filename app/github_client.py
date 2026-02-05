# gets the token via the env vars (with help from config.py) OR from OAuth flow (set up later). Main handles that.
import httpx
from app.services import extract_labels, normalize_issue

class GitHubClient:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }

    async def get_issues(self, owner: str, repo: str):
        """
        Gets all issues from a given repo (open and closed).
        Returns JSON.
        """
        url= f"{self.base_url}/repos/{owner}/{repo}/issues?state=all" #we create the URL here

        
        async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                issues_data = response.json()
                # Normalize the issues data before returning
                normalized_issues = [normalize_issue(issue) for issue in issues_data]
                return normalized_issues
            
           
        
    # asyn def create_issue