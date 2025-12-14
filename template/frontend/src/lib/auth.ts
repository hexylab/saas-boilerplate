/**
 * Authentication utilities.
 */

import { api, removeToken, setToken } from '@/lib/api';
import type { LoginRequest, RegisterRequest, User } from '@/types';

/**
 * Login and store the access token.
 *
 * @param credentials - Login credentials.
 * @returns The logged in user.
 */
export async function login(credentials: LoginRequest): Promise<User> {
  const response = await api.auth.login(credentials);
  setToken(response.access_token);
  return api.users.me();
}

/**
 * Register a new user and login.
 *
 * @param data - Registration data.
 * @returns The registered user.
 */
export async function register(data: RegisterRequest): Promise<User> {
  await api.auth.register(data);
  // Login after registration
  return login({ email: data.email, password: data.password });
}

/**
 * Logout and remove the access token.
 */
export async function logout(): Promise<void> {
  try {
    await api.auth.logout();
  } finally {
    removeToken();
  }
}

/**
 * Check if the user is authenticated.
 *
 * @returns True if authenticated.
 */
export function isAuthenticated(): boolean {
  if (typeof window === 'undefined') return false;
  return !!localStorage.getItem('access_token');
}
