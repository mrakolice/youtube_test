<template>
  <div class="login-page">
    <div class="login-container">
      <h1>Login</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
      <p>Don't have an account? <router-link to="/register">Register</router-link></p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../utils/useAuth';

const username = ref('');
const password = ref('');
const router = useRouter();
const { login } = useAuth();

const handleLogin = async () => {
  try {
    await login(username.value, password.value);
    router.push('/');
  } catch (error) {
    alert('Login failed. Please check your credentials.');
  }
};
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
}

.login-container {
  background: white;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 40px;
  max-width: 400px;
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

input {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 14px;
}

input:focus {
  outline: none;
  border-color: var(--primary-color);
}

button {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
}

p {
  text-align: center;
  font-size: 14px;
}

a {
  color: var(--primary-color);
  text-decoration: none;
}
</style>
