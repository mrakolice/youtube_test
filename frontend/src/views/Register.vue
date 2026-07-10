<template>
  <div class="register-page">
    <div class="register-container">
      <h1>Create Account</h1>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="formData.username"
            type="text"
            required
          />
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            required
          />
        </div>
        <div class="form-group">
          <label for="firstName">First Name</label>
          <input
            id="firstName"
            v-model="formData.first_name"
            type="text"
          />
        </div>
        <div class="form-group">
          <label for="lastName">Last Name</label>
          <input
            id="lastName"
            v-model="formData.last_name"
            type="text"
          />
        </div>
        <button type="submit" class="btn btn-primary">Register</button>
      </form>
      <p>Already have an account? <router-link to="/login">Login</router-link></p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../utils/useAuth';

const formData = ref({
  username: '',
  email: '',
  password: '',
  first_name: '',
  last_name: '',
});

const router = useRouter();
const { register } = useAuth();

const handleRegister = async () => {
  try {
    await register(formData.value);
    router.push('/login');
  } catch (error) {
    alert('Registration failed. Please try again.');
  }
};
</script>

<style scoped>
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
}

.register-container {
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
