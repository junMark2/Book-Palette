<template>
  <div class="profile">
    <div class="profile-header">
      <img :src="user.profileImage" alt="Profile Image" class="profile-image" />
      <h1>{{ user.username }}</h1>
      <p>{{ user.email }}</p>
    </div>
    <div class="profile-color-palette">
      <h2>Reading Color Palette</h2>
      <div class="color-palette">
        <div
          v-for="color in colorHistory"
          :key="color.genre"
          :style="{ backgroundColor: color.color }"
          class="color-block"
        >
          {{ color.genre }}
        </div>
      </div>
    </div>
    <div class="profile-statistics">
      <h2>Statistics</h2>
      <ul>
        <li v-for="stat in statistics" :key="stat.label">
          {{ stat.label }}: {{ stat.value }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'Profile',
  computed: {
    ...mapState(['user', 'colorHistory', 'statistics']),
  },
  created() {
    this.fetchUser(this.$route.params.id);
    this.fetchColorHistory(this.$route.params.id);
    this.fetchStatistics(this.$route.params.id);
  },
  methods: {
    ...mapActions(['fetchUser', 'fetchColorHistory', 'fetchStatistics']),
  },
};
</script>

<style scoped>
.profile {
  padding: 20px;
}

.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 20px;
}

.profile-color-palette {
  margin-bottom: 20px;
}

.color-palette {
  display: flex;
  flex-wrap: wrap;
}

.color-block {
  width: 50px;
  height: 50px;
  margin: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: bold;
}

.profile-statistics {
  margin-bottom: 20px;
}
</style>
