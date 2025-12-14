/**
 * React Query client configuration.
 */

'use client';

import { QueryClient } from '@tanstack/react-query';

/**
 * Create a new QueryClient instance.
 *
 * @returns Configured QueryClient.
 */
export function makeQueryClient(): QueryClient {
  return new QueryClient({
    defaultOptions: {
      queries: {
        // Stale time of 1 minute
        staleTime: 60 * 1000,
        // Retry failed requests 1 time
        retry: 1,
        // Refetch on window focus in production
        refetchOnWindowFocus: process.env.NODE_ENV === 'production',
      },
    },
  });
}

let browserQueryClient: QueryClient | undefined = undefined;

/**
 * Get or create a QueryClient instance.
 *
 * On the server, always creates a new instance.
 * On the client, reuses the same instance.
 *
 * @returns QueryClient instance.
 */
export function getQueryClient(): QueryClient {
  if (typeof window === 'undefined') {
    // Server: always make a new query client
    return makeQueryClient();
  }
  // Browser: make a new query client if we don't already have one
  if (!browserQueryClient) {
    browserQueryClient = makeQueryClient();
  }
  return browserQueryClient;
}
