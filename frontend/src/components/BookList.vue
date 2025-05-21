<template>
  <div class="book-list">
    <h2>Book List</h2>
    <ul>
      <li v-for="book in books" :key="book.id">
        <img :src="book.coverImage" alt="Book Cover" />
        <div class="book-info">
          <h3>{{ book.title }}</h3>
          <p>{{ book.author }}</p>
          <div class="genres">
            <span v-for="genre in book.genres" :key="genre.id" :style="{ backgroundColor: genre.color }">
              {{ genre.name }}
            </span>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'BookList',
  computed: {
    ...mapState(['books']),
  },
  methods: {
    ...mapActions(['fetchBooks']),
  },
  created() {
    this.fetchBooks();
  }
};
</script>

<style scoped>
.book-list {
  width: 80%;
  margin: 0 auto;
}

.book-list ul {
  list-style: none;
  padding: 0;
}

.book-list li {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
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
</style>
