<template>
  <div class="min-h-screen bg-slate-900 text-slate-100">
    <AppHeader />
    <main class="mx-auto w-full max-w-6xl px-4 py-8">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import AppHeader from "@/components/AppHeader.vue";
import { RouterView } from "vue-router";
</script>
