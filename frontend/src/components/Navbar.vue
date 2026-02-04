<template>
  <nav class="bg-gray-800 border-b border-gray-700 fixed w-full z-10 top-0">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center">
          <span class="text-2xl font-bold text-white">
            Bet <span class="text-green-500">Smart</span>
          </span>
        </div>
        <div class="flex items-center space-x-4">
          <span class="text-gray-300 text-sm hidden md:block">Analista: {{ username }}</span>
          <button @click="handleLogout" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
            Sair
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();
const username = "Admin"; // Futuramente buscaremos do backend

const handleLogout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  router.push('/');
};
</script>