# gets the token via the env vars (with help from config.py) OR from OAuth flow (set up later). Main handles that.
import httpx
from app.services import normalize_issue, serialise_issue

class GitHubClient:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }
        self.cache: list[dict] = []  # In-memory cache of issues


    async def get_issues(self, owner: str, repo: str, force_refresh: bool = False) -> list[dict]:
        """
        Gets all issues from a given repo (open and closed).
        Returns JSON.
        """

        # Check cache first (can be improved later with timestamps, etc.)
        if self.cache and not force_refresh:
            print("Returning issues from cache")
            return self.cache

        url= f"{self.base_url}/repos/{owner}/{repo}/issues?state=all" #we create the URL here

        
        async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                issues_data = response.json()
                # Normalize the issues data before returning
                normalized_issues = [normalize_issue(issue) for issue in issues_data]
                self.cache = normalized_issues # Update cache
                print("Fetched issues from GitHub API and updated cache")
                return normalized_issues
            
           
        
    async def create_issue(self, owner: str, repo: str, dict_issue: dict) -> dict:
        """
        Creates an issue in the given repo with the provided data.
        Expects a dict with keys: title, body, assignees (list of usernames), priority (string), client (string), type (string)
        Returns the created issue as JSON.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        payload = serialise_issue(dict_issue)
            
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()

            created_issue = response.json()
            #append the new issue to cache (can be improved later with better cache management)
            normalized_issue = normalize_issue(created_issue)
            self.cache.append(normalized_issue)
            return response.json()