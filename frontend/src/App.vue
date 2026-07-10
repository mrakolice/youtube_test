<template>
  <div id="app">
    <Navbar />
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import Navbar from './components/Navbar.vue';
</script>

<style>
#app {
  min-height: 100vh;
  background-color: #fff;
}

main {
  min-height: calc(100vh - 64px);
}
</style>
