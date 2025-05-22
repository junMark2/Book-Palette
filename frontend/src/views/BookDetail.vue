<template>
  <div class="book-detail container">
    <div v-if="book" class="book-content">
      <div class="book-header">
        <img :src="book.cover_image" :alt="book.title" class="book-cover" />
        <div class="book-info">
          <h1>{{ book.title }}</h1>
          <p class="author">{{ book.author }}</p>
          <p class="publisher">{{ book.publisher }} | {{ book.pub_date }}</p>
          <p class="price">{{ book.price.toLocaleString() }}원</p>
          <div class="category-tag" :style="{ backgroundColor: book.category.color }">
            {{ book.category.name }}
          </div>
        </div>
      </div>

      <div class="book-description">
        <h2>책 소개</h2>
        <p>{{ book.description }}</p>
      </div>

      <div class="reviews-section">
        <h2>리뷰</h2>
        <EmotionThermometer v-if="averageEmotionScore !== null" :emotion-score="averageEmotionScore" />
        <div class="write-review">
          <textarea v-model="newReview" placeholder="리뷰를 작성해주세요..."></textarea>
          <button @click="submitReview" :disabled="!newReview.trim()" class="btn-primary">
            리뷰 작성
          </button>
        </div>
        <div class="reviews-list">
          <div v-for="review in reviews" :key="review.id" class="review-card">
            <p class="review-author">{{ review.user }}</p>
            <p class="review-content">{{ review.content }}</p>
            <p class="review-date">{{ formatDate(review.created_at) }}</p>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="loading">
      로딩 중...
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useBookStore } from '../stores/book'
import EmotionThermometer from '../components/EmotionThermometer.vue'

const route = useRoute()
const bookStore = useBookStore()
const newReview = ref('')

const book = computed(() => bookStore.currentBook)
const reviews = computed(() => bookStore.recentReviews)
const averageEmotionScore = computed(() => bookStore.getAverageEmotionScore)

const loadBookData = async () => {
  const bookId = Number(route.params.id)
  await bookStore.fetchBookDetails(bookId)
  await bookStore.fetchRecentReviews()
}

const submitReview = async () => {
  if (!book.value) return
  try {
    await bookStore.submitReview(book.value.id, newReview.value)
    newReview.value = ''
  } catch (error) {
    console.error('리뷰 작성 실패:', error)
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  loadBookData()
})
</script>

<style scoped>
.book-detail {
  padding: 2rem;
}

.book-header {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.book-cover {
  width: 100%;
  max-width: 300px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.book-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.category-tag {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  color: white;
  font-weight: bold;
  margin-top: 1rem;
}

.reviews-section {
  margin-top: 3rem;
}

.write-review {
  margin: 1rem 0;
}

textarea {
  width: 100%;
  min-height: 100px;
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  margin-bottom: 1rem;
}

.review-card {
  padding: 1rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  margin-bottom: 1rem;
}

.review-author {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.review-date {
  color: var(--color-text-light);
  font-size: 0.9rem;
  margin-top: 0.5rem;
}
</style>
