<template>
  <div class="example-view">
    <h2>전체 도서 목록</h2>
    <div v-if="loading">로딩 중...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <div v-for="book in books" :key="book.id" class="book-item">
        {{ book.title }}
      </div>
    </div>

    <h2>로맨스 도서</h2>
    <div v-for="book in romanceBooks" :key="book.id" class="book-item">
      {{ book.title }}
    </div>

    <h2>카테고리 목록</h2>
    <div v-for="category in categories" :key="category.id" class="category-item">
      {{ category.name }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { computed } from 'vue'
import { useBookStore } from '../stores/book'

const bookStore = useBookStore()
const { books, categories, loading, error } = storeToRefs(bookStore)

// 카테고리별 책 목록
const romanceBooks = computed(() => 
  books.value.filter(book => book.category === '로맨스')
)
</script>

<style scoped>
.example-view {
  padding: 20px;
}

.book-item, .category-item {
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #eee;
  border-radius: 4px;
}
</style>
