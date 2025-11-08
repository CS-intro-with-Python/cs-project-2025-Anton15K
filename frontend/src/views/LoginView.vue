<template>
  <section class="mx-auto max-w-md space-y-6 rounded-xl border border-slate-800 bg-slate-950/70 p-6">
    <header class="space-y-2">
      <h1 class="text-2xl font-semibold">Sign in</h1>
      <p class="text-sm text-slate-300">Access personalized recommendations and track your progress.</p>
    </header>
    <form class="space-y-4" @submit.prevent="handleSubmit">
      <div class="space-y-2">
        <label class="block text-sm font-medium text-slate-300" for="username">Username</label>
        <input
          id="username"
          v-model="form.username"
          type="text"
          autocomplete="username"
          required
          class="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-slate-50 focus:border-amber-400 focus:outline-none"
        />
      </div>
      <div class="space-y-2">
        <label class="block text-sm font-medium text-slate-300" for="password">Password</label>
        <input
          id="password"
          v-model="form.password"
          type="password"
          autocomplete="current-password"
          required
          class="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-slate-50 focus:border-amber-400 focus:outline-none"
        />
      </div>
      <button
        type="submit"
        :disabled="loading"
        class="flex w-full items-center justify-center rounded-md bg-amber-400 px-4 py-2 font-semibold text-slate-900 hover:bg-amber-300 disabled:cursor-not-allowed disabled:bg-amber-400/60"
      >
        <span v-if="loading" class="animate-pulse">Signing in…</span>
        <span v-else>Sign in</span>
      </button>
    </form>
    <p class="text-center text-sm text-slate-400">
      Need an account?
      <RouterLink to="/register" class="text-amber-300 hover:text-amber-200">Create one</RouterLink>
    </p>
  </section>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { useRouter, RouterLink } from "vue-router";

import { useAuthStore } from "@/store/auth";

const router = useRouter();
const authStore = useAuthStore();

const form = reactive({
  username: "",
  password: "",
});

const loading = authStore.loading;

const handleSubmit = async () => {
  await authStore.login({ ...form });
  if (authStore.isAuthenticated) {
    router.push((router.currentRoute.value.query.redirect as string) || "/");
  }
};
</script>
