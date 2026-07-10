import { useAuthStore } from '../stores/auth';
import { authAPI } from '../api';

export const useAuth = () => {
  const authStore = useAuthStore();

  const login = async (username: string, password: string) => {
    try {
      const response = await authAPI.login({ username, password });
      authStore.setToken(response.data.access_token);
      authStore.setUser(response.data.user);
      return response.data;
    } catch (error) {
      throw error;
    }
  };

  const register = async (userData: any) => {
    try {
      const response = await authAPI.register(userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    authStore.logout();
  };

  return {
    login,
    register,
    logout,
  };
};
