import ky from 'ky';
import { useAuthStore } from '../store/auth';

export const api = ky.create({
  prefixUrl: import.meta.env.VITE_API_BASE_URL,
  hooks: {
    beforeRequest: [
      req => {
        const token = useAuthStore.getState().accessToken;
        if (token) req.headers.set('Authorization', `Bearer ${token}`);
      }
    ]
  }
});