<template>
  <div class="bg-white rounded-lg shadow-sm overflow-hidden">
    <!-- 用户问题 -->
    <div v-if="message.type === 'user'" class="p-4 bg-primary-light">
      <div class="flex items-start gap-3">
        <div class="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center flex-shrink-0">
          <span class="text-sm">👤</span>
        </div>
        <p class="text-gray-800 pt-1">{{ message.content }}</p>
      </div>
    </div>

    <!-- AI回答 -->
    <div v-else class="p-4">
      <!-- 回答内容 -->
      <div class="flex items-start gap-3 mb-4">
        <div class="w-8 h-8 rounded-full bg-green-500 text-white flex items-center justify-center flex-shrink-0">
          <span class="text-sm">🤖</span>
        </div>
        <div class="flex-1 pt-1">
          <div v-if="message.content" class="prose prose-sm max-w-none" v-html="renderedContent"></div>
          <div v-else class="text-gray-400">思考中...</div>
        </div>
      </div>

      <!-- 来源文档 -->
      <div v-if="message.sources && message.sources.length > 0" class="mt-4 pt-4 border-t border-gray-100">
        <h4 class="text-sm font-medium text-gray-500 mb-3 flex items-center gap-1">
          <span>📄</span> 来源文档
        </h4>
        <div class="flex flex-wrap gap-2">
          <SourceCard
            v-for="source in message.sources"
            :key="source.doc_id"
            :source="source"
          />
        </div>
      </div>

      <!-- 相关图片 -->
      <div v-if="message.images && message.images.length > 0" class="mt-4 pt-4 border-t border-gray-100">
        <h4 class="text-sm font-medium text-gray-500 mb-3 flex items-center gap-1">
          <span>🖼️</span> 相关图片
        </h4>
        <ImageGallery :images="message.images" />
      </div>

      <!-- 相关主题 -->
      <RelatedTopics
        v-if="message.relatedTopics && message.relatedTopics.length > 0"
        :topics="message.relatedTopics"
        @select="handleRelatedTopicSelect"
      />

      <!-- 元信息 -->
      <div v-if="message.questionType || message.responseTime" class="mt-4 pt-4 border-t border-gray-100 text-xs text-gray-400 flex gap-4">
        <span v-if="message.questionType">问题类型: {{ message.questionType }}</span>
        <span v-if="message.responseTime">响应时间: {{ message.responseTime }}ms</span>
        <span v-if="message.cached" class="text-green-500">缓存命中 ({{ message.cacheLevel }})</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import type { Message, RelatedTopic } from '@/types'
import SourceCard from './SourceCard.vue'
import ImageGallery from './ImageGallery.vue'
import RelatedTopics from './RelatedTopics.vue'

const props = defineProps<{
  message: Message
}>()

const emit = defineEmits<{
  'related-topic-select': [topic: RelatedTopic]
}>()

const renderedContent = computed(() => {
  if (!props.message.content) return ''
  const raw = marked.parse(props.message.content) as string
  return DOMPurify.sanitize(raw)
})

function handleRelatedTopicSelect(topic: RelatedTopic) {
  emit('related-topic-select', topic)
}
</script>