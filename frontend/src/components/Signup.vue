<template>
  <div class="signup">
    <h2>Signup</h2>
    <form @submit.prevent="signup">
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label for="username">Username:</label>
        <input type="text" v-model="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Signup</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      username: '',
      password: '',
    };
  },
  methods: {
    async signup() {
      try {
        const response = await axios.post('/api/auth/signup', {
          email: this.email,
          username: this.username,
          password: this.password,
        });
        this.$store.commit('setUser', response.data.user);
        this.$router.push('/');
      } catch (error) {
        console.error('Signup failed:', error);
      }
    },
  },
};
</script>

<style scoped>
.signup {
  max-width: 400px;
  margin: 0 auto;
  padding: 1em;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
