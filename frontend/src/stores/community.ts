import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

interface Thread {
  id: number
  title: string
  content: string
  author: string
  book: number | null
  thread_type: string
  created_at: string
  updated_at: string
  comments_count: number
  likes_count: number
}

interface Comment {
  id: number
  thread: number
  author: string
  content: string
  parent: number | null
  created_at: string
  updated_at: string
  replies: Comment[]
  likes_count: number
}

export const useCommunityStore = defineStore('community', {
  state: () => ({
    threads: [] as Thread[],
    currentThread: null as Thread | null,
    comments: [] as Comment[],
    loading: false,
    error: null as string | null,
  }),

  getters: {
    bookThreads: (state) => (bookId: number) => {
      return state.threads.filter(thread => thread.book === bookId)
    },
    freeThreads: (state) => {
      return state.threads.filter(thread => thread.thread_type === 'FREE')
    },
  },

  actions: {
    async fetchThreads(params = {}) {
      try {
        this.loading = true
        const response = await axios.get(`${API_URL}/threads/`, { params })
        this.threads = response.data.results
      } catch (error: any) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async fetchThreadDetails(threadId: number) {
      try {
        this.loading = true
        const response = await axios.get(`${API_URL}/threads/${threadId}/`)
        this.currentThread = response.data
        await this.fetchComments(threadId)
      } catch (error: any) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async fetchComments(threadId: number) {
      try {
        const response = await axios.get(`${API_URL}/comments/`, {
          params: { thread: threadId }
        })
        this.comments = response.data.results
      } catch (error: any) {
        this.error = error.message
      }
    },

    async createThread(threadData: Partial<Thread>) {
      try {
        this.loading = true
        await axios.post(`${API_URL}/threads/`, threadData)
        await this.fetchThreads()
      } catch (error: any) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async createComment(commentData: { thread: number; content: string; parent?: number }) {
      try {
        this.loading = true
        await axios.post(`${API_URL}/comments/`, commentData)
        if (this.currentThread) {
          await this.fetchComments(this.currentThread.id)
        }
      } catch (error: any) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async toggleThreadLike(threadId: number) {
      try {
        await axios.post(`${API_URL}/threads/${threadId}/like/`)
        if (this.currentThread?.id === threadId) {
          await this.fetchThreadDetails(threadId)
        } else {
          await this.fetchThreads()
        }
      } catch (error: any) {
        this.error = error.message
      }
    },

    async toggleCommentLike(commentId: number) {
      try {
        await axios.post(`${API_URL}/comments/${commentId}/like/`)
        if (this.currentThread) {
          await this.fetchComments(this.currentThread.id)
        }
      } catch (error: any) {
        this.error = error.message
      }
    },
  },
})
