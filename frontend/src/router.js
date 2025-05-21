import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import BookList from './components/BookList.vue';
import BookDetail from './components/BookDetail.vue';
import Community from './components/Community.vue';
import Profile from './components/Profile.vue';
import Login from './components/Login.vue';
import Signup from './components/Signup.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/books', component: BookList },
  { path: '/books/:id', component: BookDetail },
  { path: '/community', component: Community },
  { path: '/profile', component: Profile },
  { path: '/login', component: Login },
  { path: '/signup', component: Signup },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
