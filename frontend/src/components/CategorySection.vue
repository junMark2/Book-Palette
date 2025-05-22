<template>
  <div class="category-section-container">
    <div class="category-carousel">
      <button class="nav-button prev" @click="prevSlide">
        &lt;
      </button>
      <div class="category-section">
        <div class="carousel-container" :style="{ transform: `translateX(-${currentSlide * 100}%)` }">          
          <div
            v-for="(category, index) in bookStore.categories"
            :key="category.id"
            class="category-card"
            :class="{ 'active': isActiveSlide(index) }"
            :style="{ '--category-bg-image': `url(${getCategoryRandomBookImage(category)})` }"
            @click="selectCategory(category)"
            @mouseover="hoverCategory(category)"
            @mouseleave="resetHover"
          >
            <div
              class="overlay"
              :style="{ backgroundColor: category.color }"
            ></div>
            <span class="category-label">{{ category.name }}</span>
          </div>
        </div>
      </div>
      <button class="nav-button next" @click="nextSlide" :disabled="isLastSlide">
        &gt;
      </button>
    </div>

    <div v-if="selectedCategory" class="books-grid">
      <div
        v-for="book in filteredBooks"
        :key="book.id"
        class="book-card"
        @click="handleBookClick(book)"
      >
        <img
          :src="book.cover_image || getDefaultBookImage(book.title)"
          :alt="book.title"
          class="book-cover"
        >
        <div class="book-info">
          <h3 class="book-title">{{ book.title }}</h3>
          <p class="book-author">{{ book.author }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useBookStore } from '@/stores/book'
import type { Category, Book } from '@/types/models'

const router = useRouter()
const bookStore = useBookStore()
const hoveredCategory = ref<Category | null>(null)
const selectedCategory = ref<Category | null>(null)
const currentSlide = ref(0)

// 캐러셀 네비게이션
const ITEMS_PER_SLIDE = 4

const totalSlides = computed(() => Math.ceil(bookStore.categories.length / ITEMS_PER_SLIDE))

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % totalSlides.value
}

const prevSlide = () => {
  currentSlide.value = currentSlide.value > 0 ? currentSlide.value - 1 : totalSlides.value - 1
}

const isActiveSlide = (index: number) => {
  const slideIndex = Math.floor(index / ITEMS_PER_SLIDE)
  return slideIndex === currentSlide.value
}

const isLastSlide = computed(() => false)

// 필터링된 책 목록
const filteredBooks = computed(() => {
  if (!selectedCategory.value) return []
  return bookStore.books.filter(book => book.category.id === selectedCategory.value?.id)
})

// 카테고리 선택 핸들러
const selectCategory = (category: Category) => {
  selectedCategory.value = category
}

// 책 클릭 핸들러
const handleBookClick = (book: Book) => {
  router.push({ 
    name: 'book',
    params: { id: book.id }
  })
}

// 카테고리별 랜덤 책 이미지 가져오기
const getCategoryBooks = (categoryId: number) => {
  return bookStore.books.filter(book => book.category.id === categoryId)
}

// 기본 이미지 URL 생성
const getDefaultImage = (categoryName: string) => {
  return `https://source.unsplash.com/400x400/?${encodeURIComponent(categoryName + ',books')}`
}

// 카테고리별 랜덤 책 이미지 가져오기
const getCategoryRandomBookImage = (category: Category): string => {
  const books = getCategoryBooks(category.id)
  if (books.length > 0) {
    const randomBook = books[Math.floor(Math.random() * books.length)]
    return randomBook.cover_image || getDefaultImage(category.name)
  }
  return getDefaultImage(category.name)
}

const getDefaultBookImage = (bookTitle: string) => {
  return `https://source.unsplash.com/300x450/?${encodeURIComponent(bookTitle + ',book')}`
}

// 호버 효과 관련 함수들
const hoverCategory = (category: Category) => {
  hoveredCategory.value = category
}

const resetHover = () => {
  hoveredCategory.value = null
}

onMounted(async () => {
  if (bookStore.categories.length === 0) {
    await bookStore.loadFixtureData()
  }
})
</script>

<style scoped>
.category-section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.category-carousel {
  position: relative;
  display: flex;
  align-items: center;
  margin-bottom: 40px;
}

.category-section {
  flex: 1;
  overflow: hidden;
}

.carousel-container {
  display: flex;
  transition: transform 0.5s ease;
}

.category-card {
  position: relative;
  flex: 0 0 calc(25% - 20px);
  height: 250px;
  margin: 0 10px;
  overflow: hidden;
  border-radius: 12px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  opacity: 0.8;
  transform: scale(0.95);
  --category-bg-image: none;
}

.category-card.active {
  opacity: 1;
  transform: scale(1);
}

.category-card:hover {
  transform: translateY(-4px) scale(1.02);
}

.overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0.85;
  transition: all 0.5s ease;
  background-blend-mode: overlay;
  z-index: 1;
  transform: translateY(0);
}

.category-card:hover .overlay {
  transform: translateY(100%);
  opacity: 0.3;
}

.category-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: var(--category-bg-image);
  background-size: cover;
  background-position: center;
  filter: blur(3px) brightness(0.7);
  z-index: 0;
  transition: filter 0.5s ease;
}

.category-card:hover::before {
  filter: blur(2px) brightness(0.8);
}

.category-label {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  z-index: 1;
  transition: transform 0.3s ease;
}

.category-card:hover .category-label {
  transform: translate(-50%, -4px);
}

.nav-button {
  position: relative;
  z-index: 2;
  padding: 10px 15px;
  margin: 0 10px;
  border: none;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.9);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.nav-button:hover:not(:disabled) {
  background-color: rgba(255, 255, 255, 1);
  transform: scale(1.1);
}

.nav-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 24px;
  padding: 20px 0;
}

.book-card {
  position: relative;
  cursor: pointer;
  transition: transform 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
  background-color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.book-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.book-cover {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.book-info {
  padding: 16px;
  background: rgba(255, 255, 255, 0.9);
}

.book-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: bold;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.book-author {
  margin: 4px 0 0;
  font-size: 0.9rem;
  color: #666;
}

@media (max-width: 768px) {
  .books-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 16px;
  }

  .book-cover {
    height: 225px;
  }

  .book-info {
    padding: 12px;
  }

  .book-title {
    font-size: 1rem;
  }

  .book-author {
    font-size: 0.8rem;
  }
}
</style>
