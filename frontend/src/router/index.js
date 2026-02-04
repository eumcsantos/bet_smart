import { createRouter, createWebHistory } from 'vue-router'

// Definimos as rotas iniciais. 
// Por enquanto, apontamos a raiz para um componente básico.
const routes = [
  {
    path: '/',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    // Criaremos este arquivo na Etapa 8.1, mas já deixamos a rota pronta
    component: () => import('../views/DashboardView.vue'),
    meta: { requiresAuth: true } // Esta meta-tag indica que a rota é protegida
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// O Guard de Rota (Segurança do Frontend)
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access_token');

  // Se a rota exige autenticação e o usuário não está logado
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' });
  } 
  // Se o usuário já está logado e tenta ir para o Login, manda para o Dashboard
  else if (to.name === 'Login' && isAuthenticated) {
    next({ name: 'Dashboard' });
  } 
  // Caso contrário, permite a navegação
  else {
    next();
  }
});

export default router