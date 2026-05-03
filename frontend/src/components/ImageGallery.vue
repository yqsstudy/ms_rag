<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
    <div
      v-for="image in images"
      :key="image.path"
      class="border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow cursor-pointer bg-white"
      @click="openImage(image)"
    >
      <div class="aspect-video bg-gray-100 flex items-center justify-center">
        <img
          :src="getImageUrl(image.path)"
          :alt="image.caption"
          class="max-w-full max-h-full object-contain"
          loading="lazy"
          @error="handleImageError"
        />
      </div>
      <p class="p-2 text-sm text-gray-600 text-center bg-white">
        {{ imageCaption(image) }}
      </p>
    </div>
  </div>

  <!-- 图片弹窗 -->
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="selectedImage"
        class="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
        @click="selectedImage = null"
      >
        <div class="relative max-w-full max-h-full">
          <img
            :src="getImageUrl(selectedImage.path)"
            :alt="selectedImage.caption"
            class="max-w-[90vw] max-h-[90vh] object-contain"
          />
          <button
            class="absolute top-2 right-2 w-8 h-8 bg-white/20 hover:bg-white/40 rounded-full flex items-center justify-center text-white"
            @click.stop="selectedImage = null"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <p class="absolute bottom-0 left-0 right-0 bg-black/60 text-white text-center py-2 text-sm">
            {{ imageCaption(selectedImage) }}
          </p>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Image } from '@/types'

defineProps<{
  images: Image[]
}>()

const selectedImage = ref<Image | null>(null)

const getImageUrl = (path: string) => {
  // 图片路径转换
  return `/corpus/performance_guide/${path}`
}

const imageCaption = (image: Image) => {
  if (image.figure_num) {
    return `图${image.figure_num}: ${image.caption}`
  }
  return image.caption
}

const openImage = (image: Image) => {
  selectedImage.value = image
}

const handleImageError = (e: Event) => {
  const target = e.target as HTMLImageElement
  target.style.display = 'none'
  target.parentElement!.innerHTML = '<span class="text-gray-400 text-sm">图片加载失败</span>'
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>