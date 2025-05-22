import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: () => import('../views/MainPage.vue'),
    },
    {
      path: '/example',
      name: 'example',
      component: () => import('../views/ExampleView.vue'),
    },
    {
      path: '/books/:id',
      name: 'book-detail',
      component: () => import('../views/BookDetail.vue'),
      props: true,
    },
    {
      path: '/category/:id',
      name: 'category',
      component: () => import('../views/CategoryView.vue'),
      props: true,
    },
    {
      path: '/community',
      name: 'community',
      component: () => import('../views/CommunityView.vue'),
    },
    {
      path: '/thread/:id',
      name: 'thread-detail',
      component: () => import('../views/ThreadDetail.vue'),
      props: true,
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: () => import('../views/MyPage.vue'),
      props: true,
    },
  ],
})

export default router
