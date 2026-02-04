<template>
  <div class="bg-gray-800 border border-gray-700 rounded-2xl overflow-hidden hover:border-green-500/50 transition-all shadow-lg group">
    <div class="bg-gray-700/50 px-4 py-2 flex justify-between items-center border-b border-gray-700">
      <span class="text-xs font-bold text-green-400 uppercase tracking-widest">{{ match.league }}</span>
      <span class="text-xs text-gray-400">{{ formatTime(match.created_at) }}</span>
    </div>

    <div class="p-5 text-center">
      <div class="flex items-center justify-between gap-2">
        <div class="flex-1">
          <p class="text-lg font-bold text-white truncate">{{ match.is_away ? 'Visitante' : 'Mandante' }}</p>
          <p class="text-xs text-gray-400 uppercase">Favorito</p>
        </div>
        <div class="text-gray-600 font-black text-xl italic">VS</div>
        <div class="flex-1">
          <p class="text-lg font-bold text-white truncate">Underdog</p>
          <p class="text-xs text-gray-400 uppercase">Oponente</p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-px bg-gray-700 border-t border-gray-700">
      <div class="bg-gray-800 p-3 text-center">
        <p class="text-[10px] text-gray-500 uppercase font-bold mb-1 tracking-tighter">Gols (Total)</p>
        <p class="text-xl font-black text-green-500">{{ match.prediction_goals.toFixed(2) }}</p>
      </div>
      <div class="bg-gray-800 p-3 text-center">
        <p class="text-[10px] text-gray-500 uppercase font-bold mb-1 tracking-tighter">Chutes H1</p>
        <p class="text-xl font-black text-blue-400">{{ match.prediction_shots_h1.toFixed(2) }}</p>
      </div>
      <div class="bg-gray-800 p-3 text-center">
        <p class="text-[10px] text-gray-500 uppercase font-bold mb-1 tracking-tighter">Cantos H1</p>
        <p class="text-xl font-black text-yellow-500">{{ match.prediction_corners_h1.toFixed(2) }}</p>
      </div>
    </div>

    <div class="px-4 py-3 bg-gray-900/30 text-[11px] text-gray-400 flex justify-between items-center">
      <span>Status da Análise:</span>
      <span class="px-2 py-0.5 rounded-full bg-green-900/30 text-green-400 font-semibold border border-green-800/50">
        Processado
      </span>
    </div>
  </div>
</template>

<script setup>
// Recebe os dados da partida como uma "prop" vinda do Dashboard
defineProps({
  match: {
    type: Object,
    required: true
  }
});

const formatTime = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
};
</script>