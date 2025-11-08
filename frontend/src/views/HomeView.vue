<template>
  <section class="space-y-8">
    <header class="space-y-3">
      <h1 class="text-4xl font-bold leading-tight">Estimate Codeforces difficulty with data-driven insights.</h1>
      <p class="max-w-2xl text-lg text-slate-300">
        Browse problems, track attempt times, and adapt difficulty suggestions powered by solver rating statistics.
      </p>
      <div class="flex gap-3">
        <RouterLink
          to="/problems"
          class="rounded-md bg-amber-400 px-4 py-2 font-semibold text-slate-900 shadow hover:bg-amber-300"
        >
          Explore problems
        </RouterLink>
        <RouterLink
          to="/attempt"
          class="rounded-md border border-amber-400 px-4 py-2 font-semibold text-amber-400 hover:bg-amber-400/10"
        >
          Start a timed attempt
        </RouterLink>
      </div>
    </header>
    <section class="grid gap-6 md:grid-cols-3">
      <article class="rounded-lg border border-slate-800 bg-slate-950/60 p-6">
        <h2 class="text-xl font-semibold text-amber-300">Data-driven estimates</h2>
        <p class="mt-2 text-sm text-slate-300">
          Combine Codeforces solver statistics with personalized performance metrics to determine a difficulty that matches your skill level.
        </p>
      </article>
      <article class="rounded-lg border border-slate-800 bg-slate-950/60 p-6">
        <h2 class="text-xl font-semibold text-amber-300">Adaptive experience</h2>
        <p class="mt-2 text-sm text-slate-300">
          Provide feedback after each attempt to refine the estimated rating and receive smarter recommendations.
        </p>
      </article>
      <article class="rounded-lg border border-slate-800 bg-slate-950/60 p-6">
        <h2 class="text-xl font-semibold text-amber-300">Progress tracking</h2>
        <p class="mt-2 text-sm text-slate-300">
          Visualize your progress and time-to-solve metrics to focus on the skills that matter most.
        </p>
      </article>
    </section>
  </section>
</template>

<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>
