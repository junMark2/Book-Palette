<template>
  <div class="home-page">
    <div class="profile">
      <img :src="user.profileImage" alt="Profile Image" class="profile-image" />
      <div class="wave" :style="{ backgroundColor: userColorProfile }"></div>
    </div>
    <div class="recommended-books">
      <h2>Recommended Books</h2>
      <ul>
        <li v-for="book in recommendedBooks" :key="book.id">
          <img :src="book.coverImage" alt="Book Cover" />
          <div class="book-info">
            <h3>{{ book.title }}</h3>
            <p>{{ book.author }}</p>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex';

export default {
  name: 'HomePage',
  computed: {
    ...mapState(['user']),
    ...mapGetters(['userColorProfile']),
    recommendedBooks() {
      return this.$store.state.books.filter(book => book.recommended);
    }
  },
  methods: {
    ...mapActions(['fetchUser', 'fetchBooks']),
  },
  created() {
    this.fetchUser(1); // Fetch user with ID 1 for demonstration
    this.fetchBooks();
  }
};
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile {
  position: relative;
  margin-bottom: 20px;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.wave {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  animation: wave-animation 2s infinite;
}

@keyframes wave-animation {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.recommended-books {
  width: 80%;
}

.recommended-books ul {
  list-style: none;
  padding: 0;
}

.recommended-books li {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.book-info {
  margin-left: 10px;
}
</style>
