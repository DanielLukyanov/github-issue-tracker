const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const GITHUB_CLIENT_ID = import.meta.env.VITE_GITHUB_CLIENT_ID;

export interface User {
  login: string;
  name: string | null;
  avatar_url: string;
  id: number;
}

export interface AuthStatus {
  authenticated: boolean;
  user?: User;
}

export function redirectToGitHubLogin() {
  const redirectUri = `${API_BASE_URL}/auth/callback`;
  const githubAuthUrl = `https://github.com/login/oauth/authorize?client_id=${GITHUB_CLIENT_ID}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=repo`;
  window.location.href = githubAuthUrl;
}

export async function checkAuthStatus(): Promise<AuthStatus> {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/status`, {
      credentials: 'include' // Important! Send cookies
    });
    
    if (!response.ok) {
        console.warn("Firefox may be blocking cookies. Try allowing third-party cookies.");
        return { authenticated: false };
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error checking auth status:', error);
    return { authenticated: false };
  }
}

export async function logout(): Promise<void> {
  try {
    await fetch(`${API_BASE_URL}/auth/logout`, {
      method: 'POST',
      credentials: 'include'
    });
  } catch (error) {
    console.error('Error logging out:', error);
  }
}
