<template>
  <div class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="logo">
        <span class="logo-text">YouTube Clone</span>
      </router-link>
      
      <nav class="nav-menu">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link v-if="!isAuthenticated" to="/login" class="nav-link">Login</router-link>
        <router-link v-if="!isAuthenticated" to="/register" class="nav-link">Register</router-link>
        <router-link v-if="isAuthenticated" to="/upload" class="nav-link">Upload</router-link>
        <button v-if="isAuthenticated" @click="handleLogout" class="nav-link logout-btn">
          Logout
        </button>
      </nav>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const isAuthenticated = computed(() => authStore.isAuthenticated);

const handleLogout = () => {
  authStore.logout();
  router.push('/');
};
</script>

<style scoped>
.navbar {
  background-color: white;
  border-bottom: 1px solid var(--border-color);
  padding: 10px 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  cursor: pointer;
}

.logo-text {
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-color);
}

.nav-menu {
  display: flex;
  gap: 20px;
  align-items: center;
}

.nav-link {
  color: var(--text-color);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 12px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background-color: var(--secondary-color);
}

.logout-btn {
  background: none;
  color: var(--text-color);
  cursor: pointer;
}

@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    gap: 10px;
  }

  .nav-menu {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
