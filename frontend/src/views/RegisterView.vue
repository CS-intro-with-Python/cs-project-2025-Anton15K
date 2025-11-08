<template>
  <section class="mx-auto max-w-xl space-y-6 rounded-xl border border-slate-800 bg-slate-950/70 p-6">
    <header class="space-y-2">
      <h1 class="text-2xl font-semibold">Create your account</h1>
      <p class="text-sm text-slate-300">
        Track problem attempts, personalize ratings, and improve faster.
      </p>
    </header>
    <form class="grid gap-4 md:grid-cols-2" @submit.prevent="handleSubmit">
      <div class="space-y-2 md:col-span-1">
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
      <div class="space-y-2 md:col-span-1">
        <label class="block text-sm font-medium text-slate-300" for="email">Email</label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          autocomplete="email"
          required
          class="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-slate-50 focus:border-amber-400 focus:outline-none"
        />
      </div>
      <div class="space-y-2 md:col-span-1">
        <label class="block text-sm font-medium text-slate-300" for="password">Password</label>
        <input
          id="password"
          v-model="form.password"
          type="password"
          autocomplete="new-password"
          required
          class="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-slate-50 focus:border-amber-400 focus:outline-none"
        />
      </div>
      <div class="space-y-2 md:col-span-1">
        <label class="block text-sm font-medium text-slate-300" for="handle">Codeforces handle (optional)</label>
        <input
          id="handle"
          v-model="form.codeforcesHandle"
          type="text"
          autocomplete="nickname"
          class="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-slate-50 focus:border-amber-400 focus:outline-none"
        />
      </div>
      <div class="md:col-span-2">
        <button
          type="submit"
          :disabled="loading"
          class="flex w-full items-center justify-center rounded-md bg-amber-400 px-4 py-2 font-semibold text-slate-900 hover:bg-amber-300 disabled:cursor-not-allowed disabled:bg-amber-400/60"
        >
          <span v-if="loading" class="animate-pulse">Creating account…</span>
          <span v-else>Create account</span>
        </button>
      </div>
    </form>
    <p class="text-center text-sm text-slate-400">
      Already registered?
      <RouterLink to="/login" class="text-amber-300 hover:text-amber-200">Sign in</RouterLink>
    </p>
  </section>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { RouterLink, useRouter } from "vue-router";

import { useAuthStore } from "@/store/auth";

const router = useRouter();
const authStore = useAuthStore();

const form = reactive({
  username: "",
  email: "",
  password: "",
  codeforcesHandle: "",
});

const loading = authStore.loading;

const handleSubmit = async () => {
  await authStore.register({
    username: form.username,
    email: form.email,
    password: form.password,
    codeforcesHandle: form.codeforcesHandle || undefined,
  });

  if (authStore.isAuthenticated) {
    router.push("/");
  }
};
</script>
