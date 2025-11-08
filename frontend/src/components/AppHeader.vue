<template>
  <header class="border-b border-slate-800 bg-slate-950/80 backdrop-blur">
    <div class="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-4">
      <RouterLink to="/" class="text-xl font-semibold text-amber-400">CF Difficulty</RouterLink>
      <nav class="flex items-center gap-4 text-sm">
        <RouterLink to="/problems" class="hover:text-amber-300">Problems</RouterLink>
        <RouterLink to="/attempt" class="hover:text-amber-300">Attempt</RouterLink>
        <RouterLink to="/profile" class="hover:text-amber-300">Profile</RouterLink>
        <RouterLink
          v-if="!isAuthenticated"
          to="/login"
          class="rounded-md bg-amber-400 px-3 py-1.5 font-medium text-slate-950 hover:bg-amber-300"
        >
          Sign In
        </RouterLink>
        <button
          v-else
          class="rounded-md border border-amber-400 px-3 py-1.5 font-medium text-amber-400 hover:bg-amber-400/10"
          @click="handleLogout"
        >
          Sign out
        </button>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { RouterLink, useRouter } from "vue-router";

import { useAuthStore } from "@/store/auth";

const router = useRouter();
const authStore = useAuthStore();

const isAuthenticated = computed(() => authStore.isAuthenticated);

const handleLogout = () => {
  authStore.logout();
  router.push("/");
};
</script>
