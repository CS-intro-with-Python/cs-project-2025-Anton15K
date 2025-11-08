<template>
  <section class="space-y-6">
    <header class="flex flex-col gap-2">
      <h1 class="text-3xl font-semibold">Your performance</h1>
      <p class="text-sm text-slate-300">Review statistics from your recent attempts and track your growth over time.</p>
    </header>
    <div class="grid gap-4 md:grid-cols-3">
      <article class="rounded-lg border border-slate-800 bg-slate-950/70 p-5">
        <p class="text-xs uppercase tracking-wide text-slate-400">Current rating</p>
        <p class="text-3xl font-semibold text-amber-300">{{ user?.rating ?? "—" }}</p>
      </article>
      <article class="rounded-lg border border-slate-800 bg-slate-950/70 p-5">
        <p class="text-xs uppercase tracking-wide text-slate-400">Attempts this week</p>
        <p class="text-3xl font-semibold text-emerald-300">{{ stats.attemptsThisWeek }}</p>
      </article>
      <article class="rounded-lg border border-slate-800 bg-slate-950/70 p-5">
        <p class="text-xs uppercase tracking-wide text-slate-400">Average solve time</p>
        <p class="text-3xl font-semibold text-sky-300">{{ stats.averageSolveTime }} min</p>
      </article>
    </div>
    <section class="rounded-xl border border-slate-800 bg-slate-950/70 p-6">
      <h2 class="text-xl font-semibold text-amber-300">Recent attempts</h2>
      <ul class="mt-4 space-y-3">
        <li
          v-for="attempt in stats.recentAttempts"
          :key="attempt.id"
          class="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-900/70 px-4 py-3 text-sm"
        >
          <span class="font-medium">{{ attempt.problemTitle }}</span>
          <span class="text-slate-300">{{ attempt.duration }} min · {{ attempt.result }}</span>
        </li>
      </ul>
    </section>
  </section>
</template>

<script setup lang="ts">
import { computed, reactive } from "vue";

import { useAuthStore } from "@/store/auth";

const authStore = useAuthStore();
const user = computed(() => authStore.currentUser);

const stats = reactive({
  attemptsThisWeek: 5,
  averageSolveTime: 28,
  recentAttempts: [
    {
      id: 1,
      problemTitle: "Educational Round 140 E",
      duration: 35,
      result: "Solved",
    },
    {
      id: 2,
      problemTitle: "Div2 738 C",
      duration: 18,
      result: "Solved",
    },
  ],
});
</script>
