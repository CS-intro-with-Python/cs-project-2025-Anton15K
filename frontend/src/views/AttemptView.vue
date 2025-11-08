<template>
  <section class="mx-auto max-w-2xl space-y-6 rounded-xl border border-slate-800 bg-slate-950/70 p-6">
    <header class="space-y-2">
      <h1 class="text-3xl font-semibold">Timed attempt</h1>
      <p class="text-sm text-slate-300">
        Start the timer, solve the problem, then record your result to improve future recommendations.
      </p>
    </header>
    <div class="rounded-lg border border-slate-800 bg-slate-900/80 p-5">
      <p class="text-sm uppercase tracking-wide text-slate-400">Selected problem</p>
      <h2 class="text-xl font-semibold text-amber-300">{{ problemTitle }}</h2>
      <p class="text-sm text-slate-300">Estimated rating: {{ estimatedRating ?? "—" }}</p>
    </div>
    <div class="flex flex-col items-center gap-4">
      <span class="text-5xl font-mono font-semibold">{{ formattedTime }}</span>
      <div class="flex gap-3">
        <button
          v-if="!isRunning"
          class="rounded-md bg-emerald-500 px-5 py-2 font-semibold text-slate-900 hover:bg-emerald-400"
          @click="startTimer"
        >
          Start
        </button>
        <button
          v-else
          class="rounded-md bg-amber-400 px-5 py-2 font-semibold text-slate-900 hover:bg-amber-300"
          @click="pauseTimer"
        >
          Pause
        </button>
        <button
          class="rounded-md border border-rose-500 px-5 py-2 font-semibold text-rose-400 hover:bg-rose-500/10"
          @click="resetTimer"
        >
          Reset
        </button>
      </div>
    </div>
    <form class="space-y-4" @submit.prevent="submitAttempt">
      <div class="space-y-2">
        <label class="block text-sm font-medium text-slate-300" for="result">Result</label>
        <select
          id="result"
          v-model="result"
          class="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-slate-100 focus:border-amber-400 focus:outline-none"
        >
          <option value="solved">Solved</option>
          <option value="partial">Partial</option>
          <option value="unsolved">Unsolved</option>
        </select>
      </div>
      <div class="space-y-2">
        <label class="block text-sm font-medium text-slate-300" for="feedback">Feedback</label>
        <textarea
          id="feedback"
          v-model="feedback"
          rows="3"
          class="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-slate-100 focus:border-amber-400 focus:outline-none"
          placeholder="Share insights that could adjust the estimated difficulty"
        ></textarea>
      </div>
      <button
        type="submit"
        class="w-full rounded-md bg-amber-400 px-4 py-2 font-semibold text-slate-900 hover:bg-amber-300"
      >
        Submit attempt
      </button>
    </form>
  </section>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import { apiClient } from "@/services/api";

const route = useRoute();
const timer = ref(0);
const intervalId = ref<number | null>(null);
const isRunning = ref(false);
const result = ref("solved");
const feedback = ref("");

const problemId = computed(() => route.query.problemId as string | undefined);
const problemTitle = computed(() => (problemId.value ? `Problem ${problemId.value}` : "No problem selected"));
const estimatedRating = ref<number | null>(null);

const formattedTime = computed(() => {
  const seconds = timer.value;
  const minutes = Math.floor(seconds / 60)
    .toString()
    .padStart(2, "0");
  const secs = (seconds % 60).toString().padStart(2, "0");
  return `${minutes}:${secs}`;
});

const startTimer = () => {
  if (isRunning.value) return;
  isRunning.value = true;
  intervalId.value = window.setInterval(() => {
    timer.value += 1;
  }, 1000);
};

const pauseTimer = () => {
  if (!isRunning.value) return;
  isRunning.value = false;
  if (intervalId.value) {
    window.clearInterval(intervalId.value);
    intervalId.value = null;
  }
};

const resetTimer = () => {
  pauseTimer();
  timer.value = 0;
};

const submitAttempt = async () => {
  await apiClient.post("/attempts", {
    problemId: problemId.value,
    durationSeconds: timer.value,
    result: result.value,
    feedback: feedback.value,
  });

  resetTimer();
  feedback.value = "";
};

onMounted(async () => {
  if (problemId.value) {
    try {
      const { data } = await apiClient.get<{ estimatedRating: number }>(`/problems/${problemId.value}`);
      estimatedRating.value = data.estimatedRating;
    } catch (error) {
      console.warn("Failed to load problem info", error);
    }
  }
});

onBeforeUnmount(() => {
  if (intervalId.value) {
    window.clearInterval(intervalId.value);
  }
});
</script>
