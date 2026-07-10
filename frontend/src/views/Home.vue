<template>
  <div class="home">
    <h1>Popular Videos</h1>
    <div class="videos-grid">
      <router-link v-for="video in videos" :key="video.id" :to="`/video/${video.id}`" class="card-link">
        <VideoCard :video="video" />
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { videosAPI } from '../api';
import VideoCard from '../components/VideoCard.vue';

interface Video {
  id: number;
  title: string;
  description?: string;
  duration: number;
  thumbnail_url?: string;
  created_at: string;
}

const videos = ref<Video[]>([]);

onMounted(async () => {
  try {
    const response = await videosAPI.listVideos();
    videos.value = response.data;
  } catch (error) {
    console.error('Failed to load videos:', error);
  }
});
</script>

<style scoped>
.home {
  padding: 20px;
}

h1 {
  font-size: 28px;
  margin-bottom: 20px;
}

.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.card-link {
  text-decoration: none;
}

@media (max-width: 768px) {
  .videos-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }
}
</style>
