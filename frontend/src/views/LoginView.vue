<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 px-4">
    <div class="max-w-md w-full space-y-8 bg-gray-800 p-10 rounded-2xl shadow-2xl border border-gray-700">
      
      <div class="text-center">
        <h2 class="text-4xl font-extrabold text-white tracking-tight">
          Bet <span class="text-green-500">Smart</span>
        </h2>
        <p class="mt-2 text-sm text-gray-400 font-medium">
          Análise estatística avançada para futebol
        </p>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="space-y-4">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-300">Usuário</label>
            <input 
              v-model="username" 
              id="username" 
              type="text" 
              required 
              class="mt-1 block w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
              placeholder="Digite seu usuário"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-300">Senha</label>
            <input 
              v-model="password" 
              id="password" 
              type="password" 
              required 
              class="mt-1 block w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
              placeholder="••••••••"
            />
          </div>
        </div>

        <div v-if="errorMessage" class="bg-red-900/50 border border-red-500 text-red-200 text-sm p-3 rounded-lg text-center">
            {{ errorMessage }}
        </div>

        <div>
          <button 
            type="submit" 
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-bold text-gray-900 bg-green-500 hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-green-500 transition-colors uppercase tracking-wider"
          >
            Entrar no Sistema
          </button>
        </div>
      </form>

      <div class="text-center">
        <p class="text-xs text-gray-500">
          Protegido por criptografia JWT
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api'; // Nossa instância configurada do Axios

const router = useRouter();
const username = ref('');
const password = ref('');
const errorMessage = ref('');
const isLoading = ref(false);

const handleLogin = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    // 1. Envia as credenciais para o endpoint do SimpleJWT no Django
    const response = await api.post('token/', {
      username: username.value,
      password: password.value
    });

    // 2. Armazena os tokens no LocalStorage do navegador
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);

    // 3. Configura o cabeçalho padrão do Axios para as próximas chamadas
    api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;

    console.log('Login realizado com sucesso!');
    
    // 4. Redireciona para o Dashboard (que criaremos na Etapa 8)
    router.push('/dashboard');

  } catch (error) {
    console.error('Erro no login:', error);
    errorMessage.value = 'Usuário ou senha inválidos.';
  } finally {
    isLoading.value = false;
  }
};
</script>