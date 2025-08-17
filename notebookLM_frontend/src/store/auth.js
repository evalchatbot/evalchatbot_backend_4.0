import { create } from 'zustand';

export const useAuthStore = create(set => ({
  userId: localStorage.getItem('user_id') || '',
  accessToken: localStorage.getItem('access_token') || '',
  sessionId: localStorage.getItem('session_id') || '',
  setAuth: ({ userId, accessToken }) => {
    if (userId) { localStorage.setItem('user_id', userId); }
    if (accessToken) { localStorage.setItem('access_token', accessToken); }
    set({ userId: userId ?? '', accessToken: accessToken ?? '' });
  },
  setSessionId: (sessionId) => {
    localStorage.setItem('session_id', sessionId || '');
    set({ sessionId: sessionId || '' });
  },
  logout: () => {
    localStorage.removeItem('user_id');
    localStorage.removeItem('access_token');
    localStorage.removeItem('session_id');
    set({ userId:'', accessToken:'', sessionId:'' });
  }
}));
