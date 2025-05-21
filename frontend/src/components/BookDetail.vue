<template>
  <div class="book-detail">
    <img :src="book.coverImage" alt="Book Cover" />
    <div class="book-info">
      <h2>{{ book.title }}</h2>
      <p>{{ book.author }}</p>
      <p>{{ book.publisher }}</p>
      <p>{{ book.publishedAt }}</p>
      <p>{{ book.description }}</p>
      <div class="genres">
        <span v-for="genre in book.genres" :key="genre.id" :style="{ backgroundColor: genre.color }">
          {{ genre.name }}
        </span>
      </div>
      <div class="status">
        <label for="status">Reading Status:</label>
        <select v-model="status" @change="updateStatus">
          <option value="reading">Reading</option>
          <option value="completed">Completed</option>
          <option value="wishlist">Wishlist</option>
        </select>
      </div>
      <div class="personal-note">
        <label for="personalNote">Personal Note:</label>
        <textarea v-model="personalNote" @change="updatePersonalNote"></textarea>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'BookDetail',
  data() {
    return {
      status: '',
      personalNote: '',
    };
  },
  computed: {
    ...mapState(['books']),
    book() {
      return this.books.find(book => book.id === this.$route.params.id);
    },
  },
  methods: {
    ...mapActions(['fetchBooks', 'updateUserBook']),
    updateStatus() {
      this.updateUserBook({ bookId: this.book.id, status: this.status });
    },
    updatePersonalNote() {
      this.updateUserBook({ bookId: this.book.id, personalNote: this.personalNote });
    },
  },
  created() {
    this.fetchBooks();
  }
};
</script>

<style scoped>
.book-detail {
  width: 80%;
  margin: 0 auto;
}

.book-info {
  margin-left: 10px;
}

.genres span {
  display: inline-block;
  padding: 2px 5px;
  margin-right: 5px;
  border-radius: 3px;
  color: white;
}

.status, .personal-note {
  margin-top: 10px;
}
</style>
