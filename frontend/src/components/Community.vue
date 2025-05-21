<template>
  <div class="community">
    <h2>Community Threads</h2>
    <ul>
      <li v-for="thread in threads" :key="thread.id">
        <div class="thread-content">
          <p>{{ thread.content }}</p>
          <div class="thread-info">
            <span>{{ thread.user.username }}</span>
            <span>{{ thread.createdAt }}</span>
          </div>
        </div>
        <div class="comments">
          <h3>Comments</h3>
          <ul>
            <li v-for="comment in thread.comments" :key="comment.id">
              <p>{{ comment.content }}</p>
              <div class="comment-info">
                <span>{{ comment.user.username }}</span>
                <span>{{ comment.createdAt }}</span>
              </div>
            </li>
          </ul>
        </div>
        <div class="add-comment">
          <textarea v-model="newComment" placeholder="Add a comment"></textarea>
          <button @click="addComment(thread.id)">Post Comment</button>
        </div>
      </li>
    </ul>
    <div class="add-thread">
      <textarea v-model="newThread" placeholder="Start a new thread"></textarea>
      <button @click="addThread">Post Thread</button>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'Community',
  data() {
    return {
      newThread: '',
      newComment: '',
    };
  },
  computed: {
    ...mapState(['threads']),
  },
  methods: {
    ...mapActions(['fetchThreads', 'addThread', 'addComment']),
  },
  created() {
    this.fetchThreads();
  }
};
</script>

<style scoped>
.community {
  width: 80%;
  margin: 0 auto;
}

.thread-content {
  margin-bottom: 10px;
}

.thread-info, .comment-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.8em;
  color: gray;
}

.comments {
  margin-left: 20px;
}

.add-comment, .add-thread {
  margin-top: 10px;
}

textarea {
  width: 100%;
  height: 50px;
  margin-bottom: 5px;
}

button {
  display: block;
  margin-top: 5px;
}
</style>
