import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/teams',
      name: 'teams',
      component: () => import('../views/TeamsView.vue'),
    },
    {
      path: '/teams/:id',
      name: 'team-detail',
      component: () => import('../views/TeamDetailView.vue'),
    },
    {
      path: '/compare',
      name: 'compare',
      component: () => import('../views/CompareView.vue'),
    },
    {
      path: '/groups',
      name: 'groups',
      component: () => import('../views/GroupsView.vue'),
    },
    {
      path: '/groups/:groupId',
      name: 'group-detail',
      component: () => import('../views/GroupDetailView.vue'),
    },
    {
      path: '/ratings',
      name: 'ratings',
      component: () => import('../views/RatingsTableView.vue'),
    },
    {
      path: '/statistics',
      name: 'statistics',
      component: () => import('../views/StatisticsView.vue'),
    },
  ],
})

export default router
