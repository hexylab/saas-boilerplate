/**
 * Zustand stores for client-side state management.
 *
 * Use React Query for server state (API data).
 * Use Zustand for client state (UI state, form state, etc.).
 */

import { create } from 'zustand';

/**
 * UI state store.
 *
 * @example
 * ```tsx
 * function MyComponent() {
 *   const { isSidebarOpen, toggleSidebar } = useUIStore();
 *   return (
 *     <button onClick={toggleSidebar}>
 *       {isSidebarOpen ? 'Close' : 'Open'}
 *     </button>
 *   );
 * }
 * ```
 */
interface UIState {
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  isSidebarOpen: true,
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  setSidebarOpen: (open) => set({ isSidebarOpen: open }),
}));
