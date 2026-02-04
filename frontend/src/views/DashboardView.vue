<template>
  <div class="p-10">
    <h1 class="text-3xl font-bold text-green-500">Dashboard - Acesso Autorizado!</h1>
    <button @click="logout" class="mt-4 bg-red-500 p-2 rounded">Sair</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();

const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  router.push('/');
};
</script>