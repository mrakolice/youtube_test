<template>
  <div class="video-card">
    <div class="thumbnail">
      <img v-if="video.thumbnail_url" :src="video.thumbnail_url" :alt="video.title" />
      <div v-else class="no-thumbnail">No Thumbnail</div>
    </div>
    <div class="video-info">
      <h3 class="title">{{ video.title }}</h3>
      <p v-if="video.description" class="description">{{ truncateDescription(video.description) }}</p>
      <div class="meta">
        <span class="duration">{{ formatDuration(video.duration) }}</span>
        <span class="date">{{ formatDate(video.created_at) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Video {
  id: number;
  title: string;
  description?: string;
  duration: number;
  thumbnail_url?: string;
  created_at: string;
}

defineProps<{
  video: Video;
}>();

const truncateDescription = (desc: string, limit = 100) => {
  return desc.length > limit ? desc.substring(0, limit) + '...' : desc;
};

const formatDuration = (seconds: number) => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  if (hours > 0) {
    return `${hours}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  }
  return `${minutes}:${String(secs).padStart(2, '0')}`;
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString();
};
</script>

<style scoped>
.video-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid var(--border-color);
}

.video-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.thumbnail {
  width: 100%;
  height: 200px;
  background-color: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-thumbnail {
  color: white;
  font-size: 14px;
}

.video-info {
  padding: 12px;
}

.title {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.description {
  font-size: 12px;
  color: #606060;
  margin-bottom: 8px;
  line-height: 1.4;
}

.meta {
  display: flex;
  gap: 8px;
  font-size: 12px;
  color: #606060;
}
</style>
