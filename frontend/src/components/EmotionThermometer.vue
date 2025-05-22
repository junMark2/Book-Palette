<template>
  <div class="emotion-thermometer">
    <div class="thermometer-container">
      <div 
        class="thermometer-fill"
        :style="{ 
          height: `${getEmotionHeight()}%`,
          backgroundColor: getEmotionColor()
        }"
      ></div>
      <div class="thermometer-scale">
        <span class="scale-mark positive">긍정적</span>
        <span class="scale-mark neutral">중립적</span>
        <span class="scale-mark negative">부정적</span>
      </div>
    </div>
    <div class="emotion-info">
      <h3>현재 감성 온도</h3>
      <p class="emotion-score">{{ formattedScore }}</p>
      <p class="emotion-description">{{ getEmotionDescription() }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  emotionScore: number // -1.0 ~ 1.0 범위의 감정 점수
}

const props = defineProps<Props>()

const formattedScore = computed(() => {
  // -1 ~ 1 범위를 0 ~ 100으로 변환
  return Math.round((props.emotionScore + 1) * 50)
})

const getEmotionHeight = () => {
  // 감정 점수를 퍼센트로 변환 (0% ~ 100%)
  return ((props.emotionScore + 1) / 2) * 100
}

const getEmotionColor = () => {
  // 감정 점수에 따른 색상 반환
  if (props.emotionScore > 0.3) return '#FF9AA2' // 긍정
  if (props.emotionScore < -0.3) return '#355C7D' // 부정
  return '#61C0BF' // 중립
}

const getEmotionDescription = () => {
  if (props.emotionScore > 0.3) {
    return '긍정적인 감정이 느껴지네요! 🌟'
  } else if (props.emotionScore < -0.3) {
    return '조금 우울한 감정이 느껴집니다... 🌧️'
  }
  return '평온한 상태입니다 ✨'
}
</script>

<style scoped>
.emotion-thermometer {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding: 1rem;
}

.thermometer-container {
  position: relative;
  width: 40px;
  height: 200px;
  background-color: #f5f5f5;
  border-radius: 20px;
  overflow: hidden;
}

.thermometer-fill {
  position: absolute;
  bottom: 0;
  width: 100%;
  transition: height 0.5s ease, background-color 0.5s ease;
}

.thermometer-scale {
  position: absolute;
  right: -80px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 10px 0;
}

.scale-mark {
  font-size: 0.8rem;
  color: #666;
}

.emotion-info {
  text-align: left;
}

.emotion-score {
  font-size: 2rem;
  font-weight: bold;
  margin: 0.5rem 0;
}

.emotion-description {
  color: #666;
  font-size: 1.1rem;
}
</style>
