import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import QuoteRequestsView from '../views/QuoteRequestsView.vue'
import QuoteResultsView from '../views/QuoteResultsView.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: DashboardView, meta: { title: 'Dashboard' } },
  { path: '/requests', name: 'QuoteRequests', component: QuoteRequestsView, meta: { title: 'Sync History' } },
  { path: '/results', name: 'QuoteResults', component: QuoteResultsView, meta: { title: 'Detailed Logs' } },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  linkActiveClass: 'active',
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} | Insurance Premium Calculator` : 'Insurance Premium Calculator'
  next()
})

export default router
