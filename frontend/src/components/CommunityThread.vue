<template>
  <div class="thread-container"></div>
    <div class="thread-header">
      <h2>{{ thread.title }}</h2>
      <div class="thread-meta">
        <span class="author">{{ thread.author }}</span>
        <span class="date">{{ formatDate(thread.created_at) }}</span>
      </div>
    </div>

    <div class="thread-content">
      {{ thread.content }}
    </div>

    <div class="thread-actions">
      <button @click="toggleLike" :class="{ 'liked': isLiked }">
        ❤️ {{ thread.likes_count }}
      </button>
      <button @click="showCommentForm = !showCommentForm">
        💬 댓글 {{ thread.comments_count }}
      </button>
    </div>

    <!-- 댓글 작성 폼 -->
    <div v-if="showCommentForm" class="comment-form">
      <textarea
        v-model="newComment"
        placeholder="댓글을 작성해주세요..."
        rows="3"
      ></textarea>
      <button @click="submitComment" :disabled="!newComment.trim()">
        댓글 작성
      </button>
    </div>

    <!-- 댓글 목록 -->
    <div class="comments-section">
      <div
        v-for="comment in comments"
        :key="comment.id"
        class="comment"
      >
        <div class="comment-header">
          <span class="comment-author">{{ comment.author }}</span>
          <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        </div>
        <div class="comment-content">
          {{ comment.content }}
        </div>
        <div class="comment-actions">
          <button @click="toggleCommentLike(comment)" :class="{ 'liked': isCommentLiked(comment) }">
            ❤️ {{ comment.likes_count }}
          </button>
          <button @click="showReplyForm(comment)">답글</button>
        </div>

        <!-- 대댓글 목록 -->
        <div v-if="comment.replies.length > 0" class="replies">
          <div
            v-for="reply in comment.replies"
            :key="reply.id"
            class="reply"
          >
            <div class="reply-header">
              <span class="reply-author">{{ reply.author }}</span>
              <span class="reply-date">{{ formatDate(reply.created_at) }}</span>
            </div>
            <div class="reply-content">
              {{ reply.content }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface Thread {
  id: number
  title: string
  content: string
  author: string
  created_at: string
  likes_count: number
  comments_count: number
}

interface Comment {
  id: number
  author: string
  content: string
  created_at: string
  likes_count: number
  replies: Comment[]
}

const props = defineProps<{
  threadId: number
}>()

const thread = ref<Thread>({} as Thread)
const comments = ref<Comment[]>([])
const newComment = ref('')
const showCommentForm = ref(false)
const isLiked = ref(false)

const API_URL = 'http://localhost:8000/api'

// 스레드 데이터 로드
const loadThread = async () => {
  try {
    const response = await axios.get(`${API_URL}/threads/${props.threadId}/`)
    thread.value = response.data
  } catch (error) {
    console.error('스레드 로드 실패:', error)
  }
}

// 댓글 데이터 로드
const loadComments = async () => {
  try {
    const response = await axios.get(`${API_URL}/comments/`, {
      params: { thread: props.threadId }
    })
    comments.value = response.data.results
  } catch (error) {
    console.error('댓글 로드 실패:', error)
  }
}

// 좋아요 토글
const toggleLike = async () => {
  try {
    await axios.post(`${API_URL}/threads/${props.threadId}/like/`)
    isLiked.value = !isLiked.value
    loadThread() // 좋아요 수 업데이트를 위해 다시 로드
  } catch (error) {
    console.error('좋아요 실패:', error)
  }
}

// 댓글 작성
const submitComment = async () => {
  try {
    await axios.post(`${API_URL}/comments/`, {
      thread: props.threadId,
      content: newComment.value
    })
    newComment.value = ''
    showCommentForm.value = false
    loadComments() // 새로운 댓글 표시를 위해 다시 로드
  } catch (error) {
    console.error('댓글 작성 실패:', error)
  }
}

// 날짜 포맷팅
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  loadThread()
  loadComments()
})
</script>

<style scoped>
.thread-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.thread-header {
  margin-bottom: 1.5rem;
}

.thread-meta {
  color: #666;
  font-size: 0.9rem;
}

.thread-content {
  margin: 1rem 0;
  line-height: 1.6;
}

.thread-actions {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
}

button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 20px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

button:hover {
  background: #f5f5f5;
}

button.liked {
  color: #ff4757;
  border-color: #ff4757;
}

.comment-form {
  margin: 1rem 0;
}

textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

.comments-section {
  margin-top: 2rem;
}

.comment {
  margin: 1rem 0;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 4px;
}

.replies {
  margin-left: 2rem;
  padding-left: 1rem;
  border-left: 2px solid #eee;
}
</style>
