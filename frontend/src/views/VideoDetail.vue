<template>
  <div class="video-detail-page">
    <div v-if="isLoading" class="status">Loading...</div>
    <div v-else-if="!video" class="status">Video not found.</div>
    <div v-else class="video-detail">
      <div class="player-area">
        <img v-if="video.thumbnail_url" :src="video.thumbnail_url" :alt="video.title" class="poster" />
        <div v-else class="no-thumbnail">No preview available</div>
      </div>

      <h1>{{ video.title }}</h1>

      <div class="meta">
        <span>{{ totalViews }} views</span>
        <span>{{ formatDate(video.created_at) }}</span>
      </div>

      <div class="reactions">
        <button class="btn btn-secondary" @click="react('like')">👍 {{ stats?.likes_count ?? 0 }}</button>
        <button class="btn btn-secondary" @click="react('dislike')">👎 {{ stats?.dislikes_count ?? 0 }}</button>
      </div>

      <p v-if="video.description" class="description">{{ video.description }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { likesAPI, videosAPI, viewsAPI } from '../api';

interface VideoDetailData {
  id: number;
  title: string;
  description?: string;
  duration: number;
  thumbnail_url?: string;
  created_at: string;
}

interface ReactionStats {
  video_id: number;
  likes_count: number;
  dislikes_count: number;
}

const route = useRoute();
const video = ref<VideoDetailData | null>(null);
const stats = ref<ReactionStats | null>(null);
const totalViews = ref(0);
const isLoading = ref(true);

const formatDate = (dateString: string) => new Date(dateString).toLocaleDateString();

const videoId = () => Number(route.params.id);

const react = async (reactionType: 'like' | 'dislike') => {
  try {
    await likesAPI.addReaction(videoId(), reactionType);
    const response = await likesAPI.getStats(videoId());
    stats.value = response.data;
  } catch (error) {
    console.error('Failed to submit reaction:', error);
  }
};

onMounted(async () => {
  const id = videoId();
  try {
    const videoResponse = await videosAPI.getVideo(id);
    video.value = videoResponse.data;
  } catch (error) {
    console.error('Failed to load video:', error);
    isLoading.value = false;
    return;
  }

  isLoading.value = false;

  try {
    const [statsResponse, viewsResponse] = await Promise.all([
      likesAPI.getStats(id),
      viewsAPI.getViewCount(id),
    ]);
    stats.value = statsResponse.data;
    totalViews.value = viewsResponse.data.total_views;
  } catch (error) {
    console.error('Failed to load reactions/views:', error);
  }

  viewsAPI.recordView(id, 0).catch((error) => {
    console.error('Failed to record view:', error);
  });
});
</script>

<style scoped>
.video-detail-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.status {
  text-align: center;
  padding: 60px 0;
  color: #606060;
}

.player-area {
  width: 100%;
  aspect-ratio: 16 / 9;
  background-color: #000;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.player-area .poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-thumbnail {
  color: white;
  font-size: 14px;
}

h1 {
  font-size: 22px;
  margin-bottom: 8px;
}

.meta {
  display: flex;
  gap: 12px;
  font-size: 14px;
  color: #606060;
  margin-bottom: 16px;
}

.reactions {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.reactions .btn {
  width: auto;
}

.description {
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
}
</style>
