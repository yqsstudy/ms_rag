<template>
  <a
    :href="source.source_url"
    target="_blank"
    rel="noopener noreferrer"
    class="inline-flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors group"
  >
    <div class="flex-1 min-w-0">
      <p class="text-sm font-medium text-gray-800 line-clamp-1 group-hover:text-primary">
        {{ source.title }}
      </p>
      <p class="text-xs text-gray-500">
        相关度: {{ relevancePercent }}%
      </p>
    </div>
    <svg class="w-4 h-4 text-gray-400 group-hover:text-primary flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
    </svg>
  </a>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Source } from '@/types'

const props = defineProps<{
  source: Source
}>()

const relevancePercent = computed(() => {
  return Math.round(props.source.relevance_score * 100)
})
</script>