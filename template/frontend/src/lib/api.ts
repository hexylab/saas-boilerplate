/**
 * API client for backend communication.
 */

import type {
  ApiError,
  LoginRequest,
  RegisterRequest,
  TokenResponse,
  User,
  UserUpdate,
} from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Custom error class for API errors.
 */
export class ApiClientError extends Error {
  constructor(
    message: string,
    public status: number
  ) {
    super(message);
    this.name = 'ApiClientError';
  }
}

/**
 * Get the stored access token.
 */
function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('access_token');
}

/**
 * Store the access token.
 */
export function setToken(token: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('access_token', token);
}

/**
 * Remove the stored access token.
 */
export function removeToken(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('access_token');
}

/**
 * Make an API request.
 */
async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let message = 'An error occurred';
    try {
      const error: ApiError = await response.json();
      message = error.detail;
    } catch {
      message = response.statusText;
    }
    throw new ApiClientError(message, response.status);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

/**
 * API client object with all endpoints.
 */
export const api = {
  auth: {
    /**
     * Login with email and password.
     */
    login: (data: LoginRequest): Promise<TokenResponse> =>
      request('/api/v1/auth/login', {
        method: 'POST',
        body: JSON.stringify(data),
      }),

    /**
     * Register a new user.
     */
    register: (data: RegisterRequest): Promise<User> =>
      request('/api/v1/auth/register', {
        method: 'POST',
        body: JSON.stringify(data),
      }),

    /**
     * Logout (client-side token removal).
     */
    logout: (): Promise<{ message: string }> =>
      request('/api/v1/auth/logout', {
        method: 'POST',
      }),
  },

  users: {
    /**
     * Get current user information.
     */
    me: (): Promise<User> => request('/api/v1/users/me'),

    /**
     * Update current user information.
     */
    updateMe: (data: UserUpdate): Promise<User> =>
      request('/api/v1/users/me', {
        method: 'PATCH',
        body: JSON.stringify(data),
      }),
  },
};
