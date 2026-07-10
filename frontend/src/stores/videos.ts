import { defineStore } from 'pinia';
import { ref } from 'vue';

interface Video {
  id: number;
  title: string;
  description?: string;
  duration: number;
  thumbnail_url?: string;
  user_id: number;
  is_published: boolean;
  created_at: string;
}

export const useVideoStore = defineStore('videos', () => {
  const videos = ref<Video[]>([]);
  const currentVideo = ref<Video | null>(null);

  const setVideos = (newVideos: Video[]) => {
    videos.value = newVideos;
  };

  const setCurrentVideo = (video: Video | null) => {
    currentVideo.value = video;
  };

  const addVideo = (video: Video) => {
    videos.value.push(video);
  };

  return {
    videos,
    currentVideo,
    setVideos,
    setCurrentVideo,
    addVideo,
  };
});
