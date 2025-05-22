<template>
  <div class="thread-detail">
    <div v-if="thread" class="thread-content">
      <div class="thread-header">
        <h1>{{ thread.title }}</h1>
        <div class="thread-meta">
          <span>{{ thread.author }}</span>
          <span>{{ formatDate(thread.created_at) }}</span>
          <span class="thread-type" :class="thread.thread_type.toLowerCase()">
            {{ getThreadTypeLabel(thread.thread_type) }}
          </span>
        </div>
      </div>

      <div class="thread-body">
        <p>{{ thread.content }}</p>
      </div>

      <div class="thread-actions">
        <button class="like-button" @click="toggleLike" :class="{ liked: thread.is_liked }">
          ❤️ {{ thread.likes_count }}
        </button>
      </div>

      <div class="comments-section">
        <h2>댓글 {{ thread.comments_count }}개</h2>
        
        <div class="write-comment">
          <textarea 
            v-model="newComment" 
            placeholder="댓글을 작성해주세요..."
            rows="3"
          ></textarea>
          <button 
            @click="submitComment" 
            :disabled="!newComment.trim()"
            class="btn-primary"
          >
            댓글 작성
          </button>
        </div>

        <div class="comments-list">
          <div 
            v-for="comment in comments" 
            :key="comment.id" 
            class="comment-card"
          >
            <div class="comment-header">
              <span class="comment-author">{{ comment.author }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
            </div>
            <p class="comment-content">{{ comment.content }}</p>
            <div class="comment-actions">
              <button 
                class="like-button small" 
                @click="toggleCommentLike(comment)"
                :class="{ liked: comment.is_liked }"
              >
                ❤️ {{ comment.likes_count }}
              </button>
              <button 
                class="reply-button"
                @click="showReplyForm(comment.id)"
              >
                답글
              </button>
            </div>

            <!-- 답글 작성 폼 -->
            <div 
              v-if="replyToCommentId === comment.id"
              class="reply-form"
            >
              <textarea 
                v-model="newReply" 
                placeholder="답글을 작성해주세요..."
                rows="2"
              ></textarea>
              <div class="reply-actions">
                <button @click="cancelReply">취소</button>
                <button 
                  @click="submitReply(comment.id)"
                  :disabled="!newReply.trim()"
                  class="btn-primary"
                >
                  답글 작성
                </button>
              </div>
            </div>

            <!-- 답글 목록 -->
            <div 
              v-if="comment.replies && comment.replies.length > 0"
              class="replies-list"
            >
              <div 
                v-for="reply in comment.replies" 
                :key="reply.id"
                class="reply-card"
              >
                <div class="comment-header">
                  <span class="comment-author">{{ reply.author }}</span>
                  <span class="comment-date">{{ formatDate(reply.created_at) }}</span>
                </div>
                <p class="comment-content">{{ reply.content }}</p>
                <div class="comment-actions">
                  <button 
                    class="like-button small" 
                    @click="toggleReplyLike(reply)"
                    :class="{ liked: reply.is_liked }"
                  >
                    ❤️ {{ reply.likes_count }}
                  </button>
                </div>
              </div>
            </div>
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
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCommunityStore } from '../stores/community'

const route = useRoute()
const communityStore = useCommunityStore()

const thread = ref(null)
const comments = ref([])
const newComment = ref('')
const newReply = ref('')
const replyToCommentId = ref(null)

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

const toggleLike = async () => {
  try {
    await communityStore.toggleThreadLike(thread.value.id)
  } catch (error) {
    console.error('좋아요 토글 실패:', error)
  }
}

const submitComment = async () => {
  try {
    await communityStore.createComment({
      thread_id: thread.value.id,
      content: newComment.value
    })
    newComment.value = ''
  } catch (error) {
    console.error('댓글 작성 실패:', error)
  }
}

const showReplyForm = (commentId: number) => {
  replyToCommentId.value = commentId
  newReply.value = ''
}

const cancelReply = () => {
  replyToCommentId.value = null
  newReply.value = ''
}

const submitReply = async (commentId: number) => {
  try {
    await communityStore.createReply({
      thread_id: thread.value.id,
      comment_id: commentId,
      content: newReply.value
    })
    cancelReply()
  } catch (error) {
    console.error('답글 작성 실패:', error)
  }
}

const toggleCommentLike = async (comment: any) => {
  try {
    await communityStore.toggleCommentLike(comment.id)
  } catch (error) {
    console.error('댓글 좋아요 토글 실패:', error)
  }
}

const toggleReplyLike = async (reply: any) => {
  try {
    await communityStore.toggleReplyLike(reply.id)
  } catch (error) {
    console.error('답글 좋아요 토글 실패:', error)
  }
}

const loadThreadData = async () => {
  const threadId = Number(route.params.id)
  await communityStore.fetchThreadDetails(threadId)
  thread.value = communityStore.currentThread
  comments.value = communityStore.currentThreadComments
}

onMounted(() => {
  loadThreadData()
})
</script>

<style scoped>
.thread-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.thread-header {
  margin-bottom: 2rem;
}

.thread-meta {
  display: flex;
  gap: 1rem;
  color: var(--color-text-light);
  margin-top: 0.5rem;
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

.thread-body {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.thread-actions {
  margin-bottom: 2rem;
}

.comments-section {
  margin-top: 3rem;
}

.write-comment {
  margin: 1rem 0 2rem;
}

textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  margin-bottom: 1rem;
}

.comment-card {
  background: white;
  padding: 1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  margin-bottom: 1rem;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.comment-author {
  font-weight: bold;
}

.comment-date {
  color: var(--color-text-light);
  font-size: 0.9rem;
}

.comment-actions {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.like-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.like-button:hover {
  background: var(--color-background-soft);
}

.like-button.liked {
  color: var(--color-primary);
}

.reply-form {
  margin: 1rem 0;
  padding-left: 1rem;
  border-left: 2px solid var(--color-border);
}

.reply-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.replies-list {
  margin-top: 1rem;
  padding-left: 1rem;
  border-left: 2px solid var(--color-border);
}

.reply-card {
  background: var(--color-background-soft);
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: var(--color-text-light);
}
</style>
