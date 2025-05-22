<template>
  <div class="main-page">
    <h1>도서 카테고리</h1>
    <CategorySection />

    <div class="emotion-section" v-if="latestReview">
      <h2>나의 독서 감정</h2>
      <EmotionThermometer :emotionScore="latestReview.emotion_score" />
    </div>

    <div class="recent-threads">
      <h2>최근 커뮤니티 활동</h2>
      <div 
        v-for="thread in recentThreads" 
        :key="thread.id"
        class="thread-preview"
        @click="navigateToThread(thread.id)"
      >
        <h3>{{ thread.title }}</h3>
        <p class="thread-meta">
          <span>{{ thread.author }}</span>
          <span>댓글 {{ thread.comments_count }}개</span>
          <span>❤️ {{ thread.likes_count }}</span>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import CategorySection from '@/components/CategorySection.vue'
import EmotionThermometer from '@/components/EmotionThermometer.vue'

const router = useRouter()
const latestReview = ref(null)
const recentThreads = ref([])

const API_URL = 'http://localhost:8000/api'

// 최근 리뷰 데이터 로드
const loadLatestReview = async () => {
  try {
    const response = await axios.get(`${API_URL}/reviews/`, {
      params: { ordering: '-created_at', limit: 1 }
    })
    if (response.data.results.length > 0) {
      latestReview.value = response.data.results[0]
    }
  } catch (error) {
    console.error('최근 리뷰 로드 실패:', error)
  }
}

// 최근 스레드 데이터 로드
const loadRecentThreads = async () => {
  try {
    const response = await axios.get(`${API_URL}/threads/`, {
      params: { ordering: '-created_at', limit: 5 }
    })
    recentThreads.value = response.data.results
  } catch (error) {
    console.error('최근 스레드 로드 실패:', error)
  }
}

const navigateToThread = (threadId: number) => {
  router.push(`/thread/${threadId}`)
}

onMounted(() => {
  loadLatestReview()
  loadRecentThreads()
})
</script>

<style scoped>
.main-page {
  padding: 2rem;
}

h1, h2 {
  margin-bottom: 1.5rem;
}

.emotion-section {
  margin: 3rem 0;
  padding: 2rem;
  background-color: #f8f9fa;
  border-radius: 12px;
}

.recent-threads {
  margin-top: 3rem;
}

.thread-preview {
  padding: 1rem;
  margin-bottom: 1rem;
  border: 1px solid #eee;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.thread-preview:hover {
  background-color: #f8f9fa;
  transform: translateY(-2px);
}

.thread-meta {
  display: flex;
  gap: 1rem;
  color: #666;
  font-size: 0.9rem;
}

h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
}
</style>
