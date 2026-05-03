<template>
  <div class="py-8">
    <h2 class="text-lg font-medium text-gray-700 mb-4 text-center">
      💡 试试以下问题
    </h2>
    <div class="flex flex-wrap justify-center gap-2">
      <button
        v-for="question in questions"
        :key="question"
        @click="$emit('select', question)"
        class="px-4 py-2 bg-white border border-gray-200 rounded-full hover:bg-primary hover:text-white hover:border-primary transition-colors text-sm"
      >
        {{ question }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineEmits<{
  select: [question: string]
}>()

const questions = [
  '模型训练慢怎么定位？',
  'msprof工具怎么用？',
  '什么是快慢卡问题？',
  '如何分析通信耗时？',
  'Host Bound问题怎么解决？',
]
</script>