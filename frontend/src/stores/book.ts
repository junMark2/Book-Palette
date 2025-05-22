import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api'
const FIXTURE_PATH = '/fixture'

interface Category {
  id: number
  name: string
  color: string
  image: string | null
}

interface Book {
  id: number
  title: string
  author: string
  publisher: string
  pub_date: string
  description: string
  isbn: string
  cover_image: string
  category: Category
  price: number
}

interface Review {
  id: number
  book: number
  user: string
  content: string
  emotion_score: number
  created_at: string
  updated_at: string
}

export const useBookStore = defineStore('book', {
  state: () => ({
    categories: [] as Category[],
    books: [] as Book[],
    recentReviews: [] as Review[],
    currentBook: null as Book | null,
    loading: false,
    error: null as string | null,
  }),

  getters: {
    booksByCategory: (state) => (categoryId: number) => {
      return state.books.filter(book => book.category.id === categoryId)
    },
    getAverageEmotionScore: (state) => {
      if (state.recentReviews.length === 0) return 0
      const sum = state.recentReviews.reduce((acc, review) => acc + review.emotion_score, 0)
      return sum / state.recentReviews.length
    },
  },
  actions: {
    async loadFixtureData() {
      try {
        this.loading = true
        
        // 책 데이터 로드
        const booksResponse = await axios.get(`${FIXTURE_PATH}/formatted_books.json`)
        this.books = booksResponse.data.map((item: any) => ({
          id: item.pk,
          ...item.fields
        }))

        // 카테고리 데이터 로드
        const categoriesResponse = await axios.get(`${FIXTURE_PATH}/updated_categories.json`)
        this.categories = categoriesResponse.data.map((item: any) => ({
          id: item.pk,
          ...item.fields
        }))

        this.error = null
      } catch (error: any) {
        this.error = '데이터 로드 중 오류가 발생했습니다.'
        console.error('Error loading fixture data:', error)
      } finally {
        this.loading = false
      }
    },

    // API 연동 시 사용할 메서드들
    async fetchCategories() {
      try {
        this.loading = true
        const response = await axios.get(`${API_URL}/categories/`)
        this.categories = response.data.results
      } catch (error: any) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async fetchBooks(categoryId?: number) {
      try {
        this.loading = true
        const params = categoryId ? { category: categoryId } : {}
        const response = await axios.get(`${API_URL}/books/`, { params })
        this.books = response.data.results
      } catch (error: any) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async fetchBookDetails(bookId: number) {
      try {
        this.loading = true
        const response = await axios.get(`${API_URL}/books/${bookId}/`)
        this.currentBook = response.data
      } catch (error: any) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async fetchRecentReviews() {
      try {
        const response = await axios.get(`${API_URL}/reviews/`, {
          params: { ordering: '-created_at', limit: 5 }
        })
        this.recentReviews = response.data.results
      } catch (error: any) {
        this.error = error.message
      }
    },

    async submitReview(bookId: number, content: string) {
      try {
        this.loading = true
        await axios.post(`${API_URL}/reviews/`, {
          book: bookId,
          content
        })
        await this.fetchRecentReviews()
      } catch (error: any) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },  },
})
