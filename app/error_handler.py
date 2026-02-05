import httpx
from .errors import AppError

def handle_error(exc: Exception) -> AppError:
    #Github / HTTP errors

    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code

        if status == 404:
            return AppError(
                message="Resource not found",
                status_code=404,
                code="not_found"
            )
        
        if status == 401 or status == 403:
            return AppError(
                message="GitHub authentication failed",
                status_code=status,
                code="github_auth_error"
            )
        
        if status == 429:
            return AppError(
                message="GitHub rate limit exceeded",
                status_code=429,
                code="github_rate_limited",
            )
        
        return AppError(
            message="GitHub API error",
            status_code=status,
            code="github_api_error"
        )
    
    if isinstance(exc, AppError):
        return exc
    
    return AppError(
        message="Internal server error",
        status_code=500,
        code="internal_error"
    )