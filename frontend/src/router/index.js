import { createRouter, createWebHistory } from 'vue-router'

// Definimos as rotas iniciais. 
// Por enquanto, apontamos a raiz para um componente básico.
const routes = [
  {
    path: '/',
    name: 'Login',
    component: () => import('../views/LoginView.vue') 
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router