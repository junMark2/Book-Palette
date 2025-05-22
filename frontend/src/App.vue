<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { useBookStore } from '@/stores/book'
import { ref, onMounted, onUnmounted, computed } from 'vue'

const bookStore = useBookStore()
const isLoading = computed(() => bookStore.loading)
const error = computed(() => bookStore.error)
const isScrolled = ref(false)
const showScrollTop = ref(false)
const showLoginModal = ref(false)
const isLoggedIn = ref(false) // TODO: 실제 인증 상태로 변경

// 스크롤 이벤트 처리
const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
  showScrollTop.value = window.scrollY > 500
}

// 섹션으로 스크롤
const scrollToSection = (sectionId: string) => {
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

// 상단으로 스크롤
const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

// 로그아웃 처리
const handleLogout = () => {
  // TODO: 실제 로그아웃 로직 구현
  isLoggedIn.value = false
}

onMounted(async () => {
  await bookStore.loadFixtureData()  // fixture 데이터 로드
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <div v-if="isLoading" class="loading-overlay">
    <div class="loading-spinner">데이터 로딩 중...</div>
  </div>
  
  <div v-else-if="error" class="error-message">
    {{ error }}
  </div>
  
  <div v-else>
    <header class="app-header" :class="{ 'scrolled': isScrolled }">
      <nav class="main-nav">
        <RouterLink to="/" class="logo-link">
          Book Palette
        </RouterLink>

        <div class="nav-links">
          <a href="#popular" @click="scrollToSection('popular')">인기도서</a>
          <a href="#categories" @click="scrollToSection('categories')">카테고리</a>
          <a href="#community" @click="scrollToSection('community')">커뮤니티</a>
          <a href="#recommended" @click="scrollToSection('recommended')">추천도서</a>
        </div>

        <div class="auth-links">
          <template v-if="!isLoggedIn">
            <button @click="showLoginModal = true">로그인</button>
            <RouterLink to="/register" class="register-btn">회원가입</RouterLink>
          </template>
          <template v-else>
            <button @click="handleLogout">로그아웃</button>
            <RouterLink to="/mypage" class="mypage-btn">마이페이지</RouterLink>
          </template>
        </div>
      </nav>
    </header>

    <main class="app-main">
      <RouterView />
      <button 
        v-if="showScrollTop" 
        @click="scrollToTop" 
        class="scroll-top-btn"
        aria-label="페이지 상단으로 이동"
      >
        ↑
      </button>
    </main>

    <footer class="app-footer">
      <p>&copy; 2025 독서 커뮤니티. All rights reserved.</p>
    </footer>
  </div>
</template>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.error-message {
  padding: 20px;
  margin: 20px;
  background: #fff3f3;
  border: 1px solid #ffcdd2;
  border-radius: 4px;
  color: #d32f2f;
}

.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  transition: all 0.3s ease;
}

.app-header.scrolled {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(8px);
}

.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.logo-link {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: #2c3e50;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-links a {
  text-decoration: none;
  color: #2c3e50;
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-links a:hover {
  color: #42b883;
}

.auth-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.auth-links button,
.register-btn,
.mypage-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.auth-links button {
  background-color: transparent;
  color: #2c3e50;
}

.register-btn,
.mypage-btn {
  background-color: #42b883;
  color: white;
  text-decoration: none;
}

.scroll-top-btn {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #42b883;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  z-index: 1000;
}

.scroll-top-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.app-main {
  padding-top: 80px; /* 네비게이션 바 높이만큼 여백 추가 */
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
