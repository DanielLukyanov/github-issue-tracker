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
        Fetches all pages from GitHub API.
        Returns JSON.
        """

        # Check cache first (can be improved later with timestamps, etc.)
        if self.cache and not force_refresh:
            print("Returning issues from cache")
            return self.cache

        all_issues = []
        page = 1
        per_page = 100  # Max allowed by GitHub API
        
        async with httpx.AsyncClient() as client:
            while True:
                url = f"{self.base_url}/repos/{owner}/{repo}/issues?state=all&page={page}&per_page={per_page}"
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                issues_data = response.json()
                
                if not issues_data:  # No more issues
                    break
                    
                all_issues.extend(issues_data)
                
                # Check if there are more pages
                if len(issues_data) < per_page:
                    break
                    
                page += 1
            
            # Normalize all issues
            normalized_issues = [normalize_issue(issue) for issue in all_issues]
            self.cache = normalized_issues
            print(f"Fetched {len(normalized_issues)} issues from GitHub API and updated cache")
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
            # Insert at the beginning of the cache to keep most recent issues at the top to mirror GitHub's default sorting by creation date
            self.cache.insert(0, normalized_issue)
            return response.json()