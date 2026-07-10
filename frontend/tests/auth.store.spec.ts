import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useAuthStore } from '../src/stores/auth';

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('initializes with no user', () => {
    const store = useAuthStore();
    expect(store.user).toBeNull();
    expect(store.isAuthenticated).toBe(false);
  });

  it('sets user correctly', () => {
    const store = useAuthStore();
    const testUser = {
      id: 1,
      username: 'testuser',
      email: 'test@example.com',
    };
    store.setUser(testUser);
    expect(store.user).toEqual(testUser);
  });

  it('sets token and persists to localStorage', () => {
    const store = useAuthStore();
    const testToken = 'test-token-123';
    store.setToken(testToken);
    expect(store.token).toBe(testToken);
    expect(localStorage.getItem('access_token')).toBe(testToken);
  });

  it('logs out correctly', () => {
    const store = useAuthStore();
    store.setUser({ id: 1, username: 'test', email: 'test@example.com' });
    store.setToken('test-token');
    
    store.logout();
    
    expect(store.user).toBeNull();
    expect(store.token).toBeNull();
    expect(store.isAuthenticated).toBe(false);
  });
});
