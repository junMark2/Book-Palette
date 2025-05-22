<template>
  <div class="community-view container">
    <div class="community-header">
      <h1>커뮤니티</h1>
      <button @click="showCreateForm = true" class="btn-primary">
        새 글 작성
      </button>
    </div>

    <div class="thread-filters">
      <button 
        v-for="type in threadTypes" 
        :key="type.value"
        :class="['filter-btn', { active: currentType === type.value }]"
        @click="currentType = type.value"
      >
        {{ type.label }}
      </button>
    </div>

    <div class="threads-list">
      <div v-for="thread in filteredThreads" :key="thread.id" class="thread-card">
        <RouterLink :to="{ name: 'thread-detail', params: { id: thread.id }}">
          <div class="thread-header">
            <h3>{{ thread.title }}</h3>
            <span class="thread-type" :class="thread.thread_type.toLowerCase()">
              {{ getThreadTypeLabel(thread.thread_type) }}
            </span>
          </div>
          <p class="thread-preview">{{ thread.content.slice(0, 100) }}...</p>
          <div class="thread-meta">
            <span>{{ thread.author }}</span>
            <span>{{ formatDate(thread.created_at) }}</span>
            <span>💬 {{ thread.comments_count }}</span>
            <span>❤️ {{ thread.likes_count }}</span>
          </div>
        </RouterLink>
      </div>
    </div>

    <!-- 새 글 작성 모달 -->
    <div v-if="showCreateForm" class="modal-overlay" @click="showCreateForm = false">
      <div class="modal-content" @click.stop>
        <h2>새 글 작성</h2>
        <form @submit.prevent="createThread">
          <div class="form-group">
            <label>제목</label>
            <input v-model="newThread.title" type="text" required>
          </div>
          <div class="form-group">
            <label>내용</label>
            <textarea v-model="newThread.content" required rows="5"></textarea>
          </div>
          <div class="form-group">
            <label>유형</label>
            <select v-model="newThread.thread_type">
              <option value="FREE">자유 게시글</option>
              <option value="BOOK">도서 리뷰</option>
            </select>
          </div>
          <div class="form-actions">
            <button type="button" @click="showCreateForm = false">취소</button>
            <button type="submit" class="btn-primary">작성</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useCommunityStore } from '../stores/community'

const communityStore = useCommunityStore()
const showCreateForm = ref(false)
const currentType = ref('ALL')

const threadTypes = [
  { label: '전체', value: 'ALL' },
  { label: '자유', value: 'FREE' },
  { label: '도서 리뷰', value: 'BOOK' }
]

const newThread = ref({
  title: '',
  content: '',
  thread_type: 'FREE'
})

const filteredThreads = computed(() => {
  if (currentType.value === 'ALL') return communityStore.threads
  return communityStore.threads.filter(thread => thread.thread_type === currentType.value)
})

const getThreadTypeLabel = (type: string) => {
  return type === 'BOOK' ? '도서 리뷰' : '자유'
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const createThread = async () => {
  try {
    await communityStore.createThread(newThread.value)
    showCreateForm.value = false
    newThread.value = {
      title: '',
      content: '',
      thread_type: 'FREE'
    }
  } catch (error) {
    console.error('스레드 작성 실패:', error)
  }
}

onMounted(() => {
  communityStore.fetchThreads()
})
</script>

<style scoped>
.community-view {
  padding: 2rem;
}

.community-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.thread-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.filter-btn {
  padding: 0.5rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 20px;
  background: white;
  cursor: pointer;
}

.filter-btn.active {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.thread-card {
  background: white;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  margin-bottom: 1rem;
  transition: transform 0.2s;
}

.thread-card:hover {
  transform: translateY(-2px);
}

.thread-card a {
  display: block;
  padding: 1rem;
  text-decoration: none;
  color: inherit;
}

.thread-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.thread-type {
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  background: var(--color-background-soft);
}

.thread-type.book {
  background: var(--color-primary);
  color: white;
}

.thread-meta {
  display: flex;
  gap: 1rem;
  color: var(--color-text-light);
  font-size: 0.9rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}
</style>
