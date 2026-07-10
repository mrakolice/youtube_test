import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const authStore = useAuthStore();
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`;
  }
  return config;
});

export const authAPI = {
  register: (data: any) => api.post('/api/auth/register', data),
  login: (data: any) => api.post('/api/auth/login', data),
  getMe: () => api.get('/api/auth/me'),
  updateProfile: (data: any) => api.put('/api/auth/me', data),
};

export const videosAPI = {
  uploadVideo: (formData: FormData) =>
    api.post('/api/videos/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getVideo: (videoId: number) => api.get(`/api/videos/${videoId}`),
  listVideos: (skip = 0, limit = 10) =>
    api.get('/api/videos/', { params: { skip, limit } }),
};

export const viewsAPI = {
  recordView: (videoId: number, duration: number) =>
    api.post('/api/views/record', { video_id: videoId, watched_duration: duration }),
  getViewCount: (videoId: number) => api.get(`/api/views/${videoId}/count`),
};

export const likesAPI = {
  addReaction: (videoId: number, reactionType: string) =>
    api.post('/api/likes/add-reaction', { video_id: videoId, reaction_type: reactionType }),
  getStats: (videoId: number) => api.get(`/api/likes/${videoId}/stats`),
};

export default api;
