/**
 * Common type definitions.
 */

/**
 * User type returned from API.
 */
export interface User {
  id: number;
  email: string;
  name: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Login request payload.
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * Registration request payload.
 */
export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}

/**
 * Token response from login.
 */
export interface TokenResponse {
  access_token: string;
  token_type: string;
}

/**
 * API error response.
 */
export interface ApiError {
  detail: string;
}

/**
 * User update payload.
 */
export interface UserUpdate {
  email?: string;
  name?: string;
  password?: string;
}
