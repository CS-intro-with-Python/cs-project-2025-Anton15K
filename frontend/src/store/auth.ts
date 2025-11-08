import { defineStore } from "pinia";
import { computed, ref } from "vue";

import { apiClient } from "@/services/api";

type User = {
  id: number;
  username: string;
  email: string;
  codeforcesHandle?: string;
  rating?: number;
};

type AuthResponse = {
  accessToken: string;
  refreshToken?: string;
  user: User;
};

export const useAuthStore = defineStore("auth", () => {
  const token = ref<string | null>(localStorage.getItem("access_token"));
  const currentUser = ref<User | null>(null);
  const loading = ref(false);

  const isAuthenticated = computed(() => Boolean(token.value));

  const setSession = (payload: AuthResponse) => {
    token.value = payload.accessToken;
    currentUser.value = payload.user;
    localStorage.setItem("access_token", payload.accessToken);
    if (payload.refreshToken) {
      localStorage.setItem("refresh_token", payload.refreshToken);
    }
  };

  const clearSession = () => {
    token.value = null;
    currentUser.value = null;
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  };

  const login = async (credentials: { username: string; password: string }) => {
    loading.value = true;
    try {
      const { data } = await apiClient.post<AuthResponse>("/auth/login", credentials);
      setSession(data);
    } finally {
      loading.value = false;
    }
  };

  const register = async (payload: {
    username: string;
    email: string;
    password: string;
    codeforcesHandle?: string;
  }) => {
    loading.value = true;
    try {
      const { data } = await apiClient.post<AuthResponse>("/auth/register", payload);
      setSession(data);
    } finally {
      loading.value = false;
    }
  };

  const logout = async () => {
    try {
      await apiClient.post("/auth/logout");
    } catch (error) {
      console.warn("Logout request failed", error);
    } finally {
      clearSession();
    }
  };

  return {
    token,
    currentUser,
    isAuthenticated,
    loading,
    login,
    register,
    logout,
    clearSession,
  };
});
