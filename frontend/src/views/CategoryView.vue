<template>
  <div class="category-view container">
    <div class="category-header">
      <h1>{{ currentCategory ? currentCategory.name : '전체 도서' }}</h1>
      <p v-if="currentCategory" class="category-description">
        {{ currentCategory.description }}
      </p>
    </div>

    <div class="books-grid">
      <div v-for="book in filteredBooks" :key="book.id" class="book-card">
        <RouterLink :to="{ name: 'book-detail', params: { id: book.id }}">
          <img :src="book.cover_image" :alt="book.title" class="book-cover" />
          <div class="book-info">
            <h3>{{ book.title }}</h3>
            <p class="author">{{ book.author }}</p>
            <p class="price">{{ book.price.toLocaleString() }}원</p>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useBookStore } from '../stores/book'

const route = useRoute()
const bookStore = useBookStore()

const currentCategory = computed(() => {
  const categoryId = Number(route.params.id)
  return bookStore.categories.find(c => c.id === categoryId)
})

const filteredBooks = computed(() => {
  if (!route.params.id) return bookStore.books
  return bookStore.books.filter(book => book.category.id === Number(route.params.id))
})

onMounted(() => {
  if (!bookStore.books.length) {
    bookStore.loadFixtureData()
  }
})
</script>

<style scoped>
.category-view {
  padding: 2rem;
}

.category-header {
  margin-bottom: 2rem;
  text-align: center;
}

.category-description {
  color: var(--color-text-light);
  max-width: 600px;
  margin: 1rem auto;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
}

.book-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.book-card:hover {
  transform: translateY(-4px);
}

.book-card a {
  text-decoration: none;
  color: inherit;
}

.book-cover {
  width: 100%;
  height: 280px;
  object-fit: cover;
}

.book-info {
  padding: 1rem;
}

.book-info h3 {
  margin: 0;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.author {
  color: var(--color-text-light);
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.price {
  font-weight: bold;
  color: var(--color-primary);
}
</style>
