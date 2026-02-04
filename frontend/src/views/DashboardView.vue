<template>
  <div class="min-h-screen bg-gray-900">
    <Navbar />

    <main class="max-w-7xl mx-auto pt-24 pb-12 px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between mb-8 space-y-4 lg:space-y-0">
        <div>
          <h1 class="text-3xl font-bold text-white">Dashboard de Análises</h1>
          <p class="text-gray-400 mt-1">Gerencie suas previsões estatísticas</p>
        </div>

        <div class="flex flex-col sm:flex-row items-center gap-4">
          <div class="w-full sm:w-auto">
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Filtrar por Data</label>
            <input 
              v-model="filterDate" 
              @change="fetchMatches"
              type="date" 
              class="bg-gray-800 border border-gray-700 text-white text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2.5 outline-none"
            />
          </div>
          <button class="w-full sm:w-auto bg-green-500 hover:bg-green-400 text-gray-900 font-bold py-2.5 px-6 rounded-lg transition-all shadow-lg shadow-green-500/10">
            + Nova Análise
          </button>
        </div>
      </div>

      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-500"></div>
      </div>

      <div v-else-if="matches.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <MatchCard 
          v-for="match in matches" 
          :key="match.id" 
          :match="match" 
        />
      </div>

      <div v-else class="bg-gray-800/50 border border-gray-700 border-dashed rounded-2xl h-64 flex flex-col items-center justify-center text-gray-500">
        <p class="text-lg">Nenhuma análise encontrada para esta data.</p>
        <p class="text-sm italic">Tente mudar o filtro ou realize uma nova análise.</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';
import Navbar from '../components/Navbar.vue';
import MatchCard from '../components/MatchCard.vue';

const matches = ref([]);
const loading = ref(true);

// 1. Estado para a data do filtro (inicia com a data de hoje)
const filterDate = ref(new Date().toISOString().substr(0, 10));

// 2. Função auxiliar para formatar a data na tela (PT-BR)
const formatDate = (dateString) => {
  if (!dateString) return '';
  const [year, month, day] = dateString.split('-');
  return `${day}/${month}/${year}`;
};

// Função para buscar partidas da API
const fetchMatches = async () => {
  loading.value = true;
  try {
    // No mundo real, passaríamos o filtro de data como query param
    // Ex: api.get(`matches/?date=${filterDate.value}`)
    const response = await api.get('matches/');
    
    // Filtro manual no frontend para esta etapa (opcional se o backend já filtrar)
    const allMatches = response.data;
    matches.value = allMatches.filter(m => m.created_at.startsWith(filterDate.value));
    
  } catch (error) {
    console.error('Erro ao carregar partidas:', error);
  } finally {
    loading.value = false;
  }
};

// Carrega as partidas assim que o componente é montado
onMounted(fetchMatches);
</script>

<style scoped>
/* Estilização para o ícone do calendário no Chrome/Edge/Safari */
::-webkit-calendar-picker-indicator {
  filter: invert(1);
  cursor: pointer;
}
</style>