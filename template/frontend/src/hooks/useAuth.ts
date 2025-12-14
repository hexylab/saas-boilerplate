/**
 * Authentication hook using React Query.
 */

'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';

import { api } from '@/lib/api';
import { login, logout, register } from '@/lib/auth';
import type { LoginRequest, RegisterRequest, User } from '@/types';

/**
 * Query key for user data.
 */
export const userQueryKey = ['user'] as const;

/**
 * Hook for authentication state and actions.
 *
 * @returns Authentication state and mutation functions.
 */
export function useAuth() {
  const router = useRouter();
  const queryClient = useQueryClient();

  /**
   * Query for current user.
   */
  const {
    data: user,
    isLoading,
    error,
  } = useQuery<User, Error>({
    queryKey: userQueryKey,
    queryFn: api.users.me,
    retry: false,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  /**
   * Login mutation.
   */
  const loginMutation = useMutation({
    mutationFn: (credentials: LoginRequest) => login(credentials),
    onSuccess: (user) => {
      queryClient.setQueryData(userQueryKey, user);
      router.push('/dashboard');
    },
  });

  /**
   * Register mutation.
   */
  const registerMutation = useMutation({
    mutationFn: (data: RegisterRequest) => register(data),
    onSuccess: (user) => {
      queryClient.setQueryData(userQueryKey, user);
      router.push('/dashboard');
    },
  });

  /**
   * Logout mutation.
   */
  const logoutMutation = useMutation({
    mutationFn: logout,
    onSuccess: () => {
      queryClient.setQueryData(userQueryKey, null);
      queryClient.clear();
      router.push('/');
    },
  });

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    error,
    login: loginMutation.mutate,
    loginAsync: loginMutation.mutateAsync,
    isLoggingIn: loginMutation.isPending,
    loginError: loginMutation.error,
    register: registerMutation.mutate,
    registerAsync: registerMutation.mutateAsync,
    isRegistering: registerMutation.isPending,
    registerError: registerMutation.error,
    logout: logoutMutation.mutate,
    isLoggingOut: logoutMutation.isPending,
  };
}
