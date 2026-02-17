# gets the token via the env vars (with help from config.py) OR from OAuth flow (set up later). Main handles that.
import httpx
from app.services import normalize_issue, serialise_issue

class GitHubClient:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.cache: dict[str, list[dict]] = {}  # Cache per user token

    def _get_headers(self, token: str) -> dict:
        """Generate headers with user's OAuth token"""
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
        }

    async def get_issues(
        self, 
        owner: str, 
        repo: str, 
        token: str,  # ← Now requires user's OAuth token
        force_refresh: bool = False
    ) -> list[dict]:
        """
        Gets all issues from a given repo using the user's OAuth token.
        """
        cache_key = f"{token}:{owner}/{repo}"
        
        # Check cache first
        if cache_key in self.cache and not force_refresh:
            print("Returning issues from cache")
            return self.cache[cache_key]

        all_issues = []
        page = 1
        per_page = 100
        
        async with httpx.AsyncClient() as client:
            while True:
                url = f"{self.base_url}/repos/{owner}/{repo}/issues?state=all&page={page}&per_page={per_page}"
                response = await client.get(url, headers=self._get_headers(token))
                response.raise_for_status()
                issues_data = response.json()
                
                if not issues_data:
                    break
                    
                all_issues.extend(issues_data)
                
                if len(issues_data) < per_page:
                    break
                    
                page += 1
            
            normalized_issues = [normalize_issue(issue) for issue in all_issues]
            self.cache[cache_key] = normalized_issues
            print(f"Fetched {len(normalized_issues)} issues from GitHub API and updated cache")
            return normalized_issues
            
    async def create_issue(
        self, 
        owner: str, 
        repo: str, 
        token: str,  # ← Now requires user's OAuth token
        dict_issue: dict
    ) -> dict:
        """
        Creates an issue using the user's OAuth token.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        payload = serialise_issue(dict_issue)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self._get_headers(token), json=payload)
            response.raise_for_status()

            created_issue = response.json()
            normalized_issue = normalize_issue(created_issue)
            
            # Update cache for this user
            cache_key = f"{token}:{owner}/{repo}"
            if cache_key in self.cache:
                self.cache[cache_key].insert(0, normalized_issue)
            
            return created_issue