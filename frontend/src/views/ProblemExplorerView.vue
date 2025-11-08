<template>
  <section class="space-y-6">
    <header class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
      <div>
        <h1 class="text-3xl font-semibold">Problem explorer</h1>
        <p class="text-sm text-slate-300">Browse Codeforces problems and filter by difficulty, tags, and status.</p>
      </div>
      <div class="flex gap-2">
        <input
          v-model="filters.search"
          type="search"
          placeholder="Search problems"
          class="rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:border-amber-400 focus:outline-none"
        />
        <select
          v-model.number="filters.ratingMin"
          class="rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:border-amber-400 focus:outline-none"
        >
          <option :value="0">Min rating</option>
          <option v-for="option in ratingOptions" :key="option" :value="option">{{ option }}</option>
        </select>
        <select
          v-model.number="filters.ratingMax"
          class="rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:border-amber-400 focus:outline-none"
        >
          <option :value="0">Max rating</option>
          <option v-for="option in ratingOptions" :key="option" :value="option">{{ option }}</option>
        </select>
      </div>
    </header>
    <section class="grid gap-4 md:grid-cols-2">
      <article
        v-for="problem in filteredProblems"
        :key="problem.codeforcesId"
        class="space-y-2 rounded-lg border border-slate-800 bg-slate-950/60 p-5"
      >
        <div class="flex items-start justify-between">
          <h2 class="text-lg font-semibold text-amber-300">
            <a :href="problem.url" target="_blank" rel="noopener">{{ problem.title }}</a>
          </h2>
          <span class="rounded-full border border-emerald-400 px-3 py-1 text-sm text-emerald-300">
            {{ problem.estimatedRating ?? "—" }}
          </span>
        </div>
        <p class="text-sm text-slate-300">
          {{ problem.summary }}
        </p>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="tag in problem.tags"
            :key="tag"
            class="rounded-md border border-slate-700 px-3 py-1 text-xs uppercase tracking-wide text-slate-300"
          >
            {{ tag }}
          </span>
        </div>
        <RouterLink
            :to="{ name: 'attempt', query: { problemId: problem.codeforcesId } }"
          class="inline-flex items-center rounded-md bg-amber-400 px-3 py-1.5 text-sm font-semibold text-slate-900 hover:bg-amber-300"
        >
          Attempt now
        </RouterLink>
      </article>
    </section>
  </section>
</template>

<script setup lang="ts">
import { computed, reactive } from "vue";
import { RouterLink } from "vue-router";

type ProblemSummary = {
  codeforcesId: string;
  title: string;
  url: string;
  estimatedRating: number | null;
  tags: string[];
  summary: string;
};

const ratingOptions = [800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400];

const problems = reactive<ProblemSummary[]>([
  {
    codeforcesId: "1A",
    title: "Theatre Square",
    url: "https://codeforces.com/problemset/problem/1/A",
    estimatedRating: 800,
    tags: ["math", "implementation"],
    summary: "Cover a rectangular square with flagstones while minimizing usage.",
  },
]);

const filters = reactive({
  search: "",
  ratingMin: 0,
  ratingMax: 0,
});

const filteredProblems = computed(() => {
  return problems.filter((problem) => {
    const matchesSearch = problem.title.toLowerCase().includes(filters.search.toLowerCase());
    const meetsMin = filters.ratingMin ? (problem.estimatedRating ?? 0) >= filters.ratingMin : true;
    const meetsMax = filters.ratingMax ? (problem.estimatedRating ?? Infinity) <= filters.ratingMax : true;
    return matchesSearch && meetsMin && meetsMax;
  });
});
</script>
