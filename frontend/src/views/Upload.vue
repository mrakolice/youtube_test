<template>
  <div class="upload-page">
    <div class="upload-container">
      <h1>Upload Video</h1>
      <form @submit.prevent="handleUpload">
        <div class="form-group">
          <label for="title">Title</label>
          <input id="title" v-model="title" type="text" maxlength="255" required />
        </div>
        <div class="form-group">
          <label for="description">Description</label>
          <textarea id="description" v-model="description" maxlength="5000" rows="4"></textarea>
        </div>
        <div class="form-group">
          <label for="file">Video file</label>
          <input id="file" type="file" accept="video/*" required @change="handleFileChange" />
        </div>
        <button type="submit" class="btn btn-primary" :disabled="isUploading">
          {{ isUploading ? 'Uploading...' : 'Upload' }}
        </button>
      </form>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { videosAPI } from '../api';

const title = ref('');
const description = ref('');
const file = ref<File | null>(null);
const isUploading = ref(false);
const errorMessage = ref('');
const router = useRouter();

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  file.value = target.files?.[0] ?? null;
};

const handleUpload = async () => {
  if (!file.value) {
    errorMessage.value = 'Please select a video file.';
    return;
  }

  const formData = new FormData();
  formData.append('title', title.value);
  if (description.value) {
    formData.append('description', description.value);
  }
  formData.append('file', file.value);

  isUploading.value = true;
  errorMessage.value = '';
  try {
    const response = await videosAPI.uploadVideo(formData);
    router.push(`/video/${response.data.id}`);
  } catch (error) {
    errorMessage.value = 'Upload failed. Please try again.';
  } finally {
    isUploading.value = false;
  }
};
</script>

<style scoped>
.upload-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
}

.upload-container {
  background: white;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 40px;
  max-width: 480px;
  width: 100%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 24px;
  margin-bottom: 30px;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

button {
  width: 100%;
  padding: 10px;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  margin-top: 16px;
  text-align: center;
  font-size: 14px;
  color: var(--primary-color);
}
</style>
