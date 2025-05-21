import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
  state: {
    user: null,
    books: [],
    threads: [],
    comments: [],
    likes: [],
    colorHistory: [],
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setBooks(state, books) {
      state.books = books;
    },
    setThreads(state, threads) {
      state.threads = threads;
    },
    setComments(state, comments) {
      state.comments = comments;
    },
    setLikes(state, likes) {
      state.likes = likes;
    },
    setColorHistory(state, colorHistory) {
      state.colorHistory = colorHistory;
    },
  },
  actions: {
    async fetchUser({ commit }, userId) {
      const response = await axios.get(`/api/users/${userId}`);
      commit('setUser', response.data);
    },
    async fetchBooks({ commit }) {
      const response = await axios.get('/api/books');
      commit('setBooks', response.data);
    },
    async fetchThreads({ commit }) {
      const response = await axios.get('/api/threads');
      commit('setThreads', response.data);
    },
    async fetchComments({ commit }) {
      const response = await axios.get('/api/comments');
      commit('setComments', response.data);
    },
    async fetchLikes({ commit }) {
      const response = await axios.get('/api/likes');
      commit('setLikes', response.data);
    },
    async fetchColorHistory({ commit }, userId) {
      const response = await axios.get(`/api/users/${userId}/color-history`);
      commit('setColorHistory', response.data);
    },
  },
  getters: {
    userColorProfile(state) {
      if (!state.colorHistory.length) return null;
      const primaryGenre = state.colorHistory.reduce((max, genre) => genre.count > max.count ? genre : max, state.colorHistory[0]);
      return primaryGenre.color;
    },
  },
});

export default store;
