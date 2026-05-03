<template>
  <div class="max-w-4xl mx-auto px-4 py-3">
    <div class="flex gap-2">
      <input
        v-model="inputValue"
        type="text"
        placeholder="输入性能相关问题，如：模型训练慢怎么定位？"
        class="flex-1 px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
        @keyup.enter="handleSend"
        :disabled="disabled"
      />
      <button
        @click="handleSend"
        :disabled="disabled || !inputValue.trim()"
        class="px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary-dark disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        发送
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  modelValue: string
  disabled?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  'send': []
}>()

const inputValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const handleSend = () => {
  if (props.disabled || !inputValue.value.trim()) return
  emit('send')
}
</script>