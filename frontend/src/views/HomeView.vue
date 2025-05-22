<script setup lang="ts">
import CategorySection from '../components/CategorySection.vue'
import { useBookStore } from '@/stores/book'
import { ref, onMounted } from 'vue'

const bookStore = useBookStore()

const popularBooks = ref([])
const recommendedBooks = ref([])
const categorizedBooks = ref<{ [key: number]: any[] }>({})

onMounted(async () => {
  await bookStore.loadFixtureData()
  
  // 인기 도서와 추천 도서 데이터 로드
  popularBooks.value = bookStore.books.slice(0, 6)  // 상위 6개를 인기 도서로 설정
  recommendedBooks.value = bookStore.books.slice(6, 12)  // 다음 6개를 추천 도서로 설정
  
  // 카테고리별 도서 분류
  bookStore.categories.forEach(category => {
    categorizedBooks.value[category.id] = bookStore.books.filter(
      book => book.category.id === category.id
    ).slice(0, 4) // 각 카테고리당 4개씩 표시
  })
})
</script>

<template>
  <div class="home-container">
    <!-- 인기 도서 섹션 -->
    <section id="popular" class="section">
      <h2 class="section-title">인기 도서</h2>
      <div class="book-grid">
        <div v-for="book in popularBooks" :key="book.id" class="book-card">
          <img :src="book.cover_image" :alt="book.title" class="book-cover">
          <h3>{{ book.title }}</h3>
          <p class="author">{{ book.author }}</p>
        </div>
      </div>
    </section>

    <!-- 카테고리 섹션 -->
    <section id="categories" class="section">
      <h2 class="section-title">카테고리</h2>
      <div class="categories-grid">
        <div v-for="category in bookStore.categories" :key="category.id" class="category-container">
          <h3 class="category-title" :style="{ color: category.color }">{{ category.name }}</h3>
          <div class="category-books">
            <div v-for="book in categorizedBooks[category.id]" :key="book.id" class="book-mini-card">
              <img :src="book.cover_image" :alt="book.title" class="book-mini-cover">
              <div class="book-mini-info">
                <p class="book-mini-title">{{ book.title }}</p>
                <p class="book-mini-author">{{ book.author }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <CategorySection />
    </section>

    <!-- 커뮤니티 섹션 -->
    <section id="community" class="section">
      <h2 class="section-title">커뮤니티</h2>
      <div class="community-preview">
        <div class="thread-list">
          <div v-for="i in 3" :key="i" class="thread-card">
            <h3>독서 모임 {{ i }}</h3>
            <p>함께 읽고 이야기 나누어요!</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 추천 도서 섹션 -->
    <section id="recommended" class="section">
      <h2 class="section-title">추천 도서</h2>
      <div class="book-grid">
        <div v-for="book in recommendedBooks" :key="book.id" class="book-card">
          <img :src="book.cover_image" :alt="book.title" class="book-cover">
          <h3>{{ book.title }}</h3>
          <p class="author">{{ book.author }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-container {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.section {
  padding: 4rem 0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.section-title {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 2rem;
  text-align: center;
}

.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
  padding: 1rem;
}

.book-card {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.book-card:hover {
  transform: translateY(-4px);
}

.book-cover {
  width: 100%;
  height: 280px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.book-card h3 {
  font-size: 1.1rem;
  margin: 0.5rem 0;
  color: #2c3e50;
}

.author {
  color: #666;
  font-size: 0.9rem;
}

.community-preview {
  padding: 2rem;
}

.thread-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.thread-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.thread-card:hover {
  transform: translateY(-4px);
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 1rem;
}

.category-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.category-title {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  text-align: center;
}

.category-books {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.book-mini-card {
  display: flex;
  gap: 1rem;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.book-mini-card:hover {
  transform: translateY(-2px);
}

.book-mini-cover {
  width: 80px;
  height: 120px;
  object-fit: cover;
  border-radius: 4px;
}

.book-mini-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.book-mini-title {
  font-weight: 500;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.book-mini-author {
  font-size: 0.8rem;
  color: #666;
}
</style>
