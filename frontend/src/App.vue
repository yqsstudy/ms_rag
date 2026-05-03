<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="fixed top-0 w-full bg-white shadow-sm z-10">
      <div class="max-w-4xl mx-auto px-4 py-3 flex justify-between items-center">
        <h1 class="text-xl font-bold text-primary">
          🎯 性能定位指南RAG系统
        </h1>
        <button
          @click="clearMessages"
          class="text-gray-500 hover:text-gray-700 text-sm flex items-center gap-1"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          清除对话
        </button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="pt-16 pb-24">
      <div class="max-w-4xl mx-auto px-4">
        <!-- 快捷问题 -->
        <QuickQuestions
          v-if="messages.length === 0"
          @select="handleQuickQuestion"
        />

        <!-- 消息列表 -->
        <div class="space-y-4 mt-4">
          <MessageCard
            v-for="msg in messages"
            :key="msg.id"
            :message="msg"
          />
        </div>

        <!-- 加载动画 -->
        <LoadingDots v-if="isLoading" />
      </div>
    </main>

    <!-- Footer Input -->
    <footer class="fixed bottom-0 w-full bg-white border-t">
      <ChatInput
        v-model="inputText"
        :disabled="isLoading"
        @send="handleSend"
      />
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useChat } from '@/composables/useChat'
import ChatInput from '@/components/ChatInput.vue'
import MessageCard from '@/components/MessageCard.vue'
import QuickQuestions from '@/components/QuickQuestions.vue'
import LoadingDots from '@/components/LoadingDots.vue'

const { messages, isLoading, sendMessage, clearMessages } = useChat()
const inputText = ref('')

const handleSend = () => {
  if (!inputText.value.trim()) return
  sendMessage(inputText.value)
  inputText.value = ''
}

const handleQuickQuestion = (question: string) => {
  sendMessage(question)
}
</script>