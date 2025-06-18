<template>
  <div>
    <h2 class="text-2xl font-bold mb-4 text-center">{{ t.finds }}</h2>
    <p>Здесь отображаются товары дня.</p>
  </div>
</template>

<script setup>
defineProps({ t: Object });
</script>
