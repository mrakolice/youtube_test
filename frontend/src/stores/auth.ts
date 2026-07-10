import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

interface User {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const token = ref<string | null>(localStorage.getItem('access_token'));
  const isAuthenticated = computed(() => !!token.value);

  const setUser = (newUser: User | null) => {
    user.value = newUser;
  };

  const setToken = (newToken: string | null) => {
    token.value = newToken;
    if (newToken) {
      localStorage.setItem('access_token', newToken);
    } else {
      localStorage.removeItem('access_token');
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
  };

  return {
    user,
    token,
    isAuthenticated,
    setUser,
    setToken,
    logout,
  };
});
