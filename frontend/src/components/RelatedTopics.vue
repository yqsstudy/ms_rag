<template>
  <div v-if="topics && topics.length > 0" class="mt-4 pt-4 border-t border-gray-100">
    <h4 class="text-sm font-medium text-gray-500 mb-3 flex items-center gap-1">
      <span>🔗</span> 相关主题
    </h4>
    <div class="flex flex-wrap gap-2">
      <button
        v-for="topic in topics"
        :key="topic.doc_id"
        class="px-3 py-1.5 text-sm bg-gray-50 hover:bg-primary-light text-gray-600 hover:text-primary rounded-full transition-colors cursor-pointer border border-gray-200 hover:border-primary"
        @click="$emit('select', topic)"
      >
        {{ topic.title }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { RelatedTopic } from '@/types'

defineProps<{
  topics: RelatedTopic[]
}>()

defineEmits<{
  select: [topic: RelatedTopic]
}>()
</script>
