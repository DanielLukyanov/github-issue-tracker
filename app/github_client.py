# gets the token via the env vars (with help from config.py) OR from OAuth flow (set up later). Main handles that.
import httpx

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
        url= f"{self.base_url}/repos/{owner}/{repo}/issues?state=all"

        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            
            except httpx.HTTPError as e:
                #GitHub responded but with an error status (i.e 4xx or 5xx)
                error_data = e.response.json()
                message = error_data.get("message", "Github API error")

                raise GithubAPIError(
                    status_code=e.response.status_code,
                    message=message
                )
            
            except httpx.RequestError as e:
                #A network error occurred
                raise RuntimeError(f"Network error occurred: {str(e)}")
        
    # asyn def create_issue


class GithubAPIError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"GitHub API Error {status_code}: {message}")