import axios, { type AxiosInstance } from 'axios';
import { useAuthStore } from '../stores/auth';

// Each backend feature is its own microservice on its own port (see
// docker-compose.yml) — there is no shared gateway in front of them, so the
// frontend needs a separate base URL per service rather than one shared one.
const AUTH_API_URL = import.meta.env.VITE_AUTH_API_URL || 'http://localhost:8001';
const VIDEO_API_URL = import.meta.env.VITE_VIDEO_API_URL || 'http://localhost:8002';
const VIEW_API_URL = import.meta.env.VITE_VIEW_API_URL || 'http://localhost:8003';
const LIKE_API_URL = import.meta.env.VITE_LIKE_API_URL || 'http://localhost:8004';

const createClient = (baseURL: string): AxiosInstance => {
  const client = axios.create({ baseURL });
  client.interceptors.request.use((config) => {
    const authStore = useAuthStore();
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`;
    }
    return config;
  });
  return client;
};

const authClient = createClient(AUTH_API_URL);
const videoClient = createClient(VIDEO_API_URL);
const viewClient = createClient(VIEW_API_URL);
const likeClient = createClient(LIKE_API_URL);

export const authAPI = {
  register: (data: any) => authClient.post('/api/auth/register', data),
  login: (data: any) => authClient.post('/api/auth/login', data),
  getMe: () => authClient.get('/api/auth/me'),
  updateProfile: (data: any) => authClient.put('/api/auth/me', data),
};

export const videosAPI = {
  // Don't set a manual Content-Type here: axios/the browser need to add the
  // multipart boundary themselves when serializing FormData. A hardcoded
  // 'multipart/form-data' header has no boundary, so the server can't parse
  // the body at all.
  uploadVideo: (formData: FormData) => videoClient.post('/api/videos/upload', formData),
  getVideo: (videoId: number) => videoClient.get(`/api/videos/${videoId}`),
  listVideos: (skip = 0, limit = 10) =>
    videoClient.get('/api/videos/', { params: { skip, limit } }),
};

export const viewsAPI = {
  recordView: (videoId: number, duration: number) =>
    viewClient.post('/api/views/record', { video_id: videoId, watched_duration: duration }),
  getViewCount: (videoId: number) => viewClient.get(`/api/views/${videoId}/count`),
};

export const likesAPI = {
  addReaction: (videoId: number, reactionType: string) =>
    likeClient.post('/api/likes/add-reaction', { video_id: videoId, reaction_type: reactionType }),
  getStats: (videoId: number) => likeClient.get(`/api/likes/${videoId}/stats`),
};
