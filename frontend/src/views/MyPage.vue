<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useBookStore } from '../stores/book'
import { useCommunityStore } from '../stores/community'

const bookStore = useBookStore()
const communityStore = useCommunityStore()

const userName = ref('사용자')
const joinDate = ref(new Date('2024-01-01'))
const readBooksCount = ref(0)
const reviewsCount = ref(0)
const averageEmotion = ref(0)
const recentReviews = ref([])
const recentThreads = ref([])

const loadUserData = async () => {
  try {
    // 임시 데이터
    readBooksCount.value = 15
    reviewsCount.value = 8
    averageEmotion.value = 4.2
  } catch (error) {
    console.error('사용자 데이터 로드 실패:', error)
  }
}

const formatDate = (date: string | Date) => {
  return new Date(date).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  loadUserData()
})
</script>

<template>
  <div class="my-page">
    <div class="profile-section">
      <h1>마이 페이지</h1>
      <div class="user-info">
        <img src="https://via.placeholder.com/100" alt="Profile" class="profile-image" />
        <div class="user-details">
          <h2>{{ userName }}</h2>
          <p>가입일: {{ formatDate(joinDate) }}</p>
        </div>
      </div>
    </div>

    <div class="stats-section">
      <div class="stat-card">
        <h3>독서 통계</h3>
        <p>읽은 책: {{ readBooksCount }}권</p>
        <p>작성한 리뷰: {{ reviewsCount }}개</p>
        <p>평균 감정 점수: {{ averageEmotion }}</p>
      </div>
    </div>

    <div class="activity-section">
      <h2>최근 활동</h2>
      
      <div class="recent-reviews">
        <h3>최근 리뷰</h3>
        <div v-for="review in recentReviews" :key="review.id" class="review-card">
          <h4>{{ review.book.title }}</h4>
          <p>{{ review.content }}</p>
          <span class="review-date">{{ formatDate(review.created_at) }}</span>
        </div>
      </div>

      <div class="recent-threads">
        <h3>최근 게시글</h3>
        <div v-for="thread in recentThreads" :key="thread.id" class="thread-card">
          <RouterLink :to="{ name: 'thread-detail', params: { id: thread.id }}">
            <h4>{{ thread.title }}</h4>
            <p>{{ thread.content?.slice(0, 100) }}...</p>
            <span class="thread-date">{{ formatDate(thread.created_at) }}</span>
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.my-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-section {
  margin-bottom: 3rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-top: 1.5rem;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

.user-details h2 {
  margin: 0;
  margin-bottom: 0.5rem;
}

.stats-section {
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.activity-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.review-card, .thread-card {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.thread-card a {
  text-decoration: none;
  color: inherit;
}

.review-date, .thread-date {
  display: block;
  color: var(--color-text-light);
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

h3 {
  margin-bottom: 1rem;
}

h4 {
  margin: 0;
  margin-bottom: 0.5rem;
}
</style>
