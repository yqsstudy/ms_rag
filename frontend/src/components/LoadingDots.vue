<template>
  <div class="flex items-center justify-center py-4">
    <div class="flex gap-1">
      <span class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 0ms"></span>
      <span class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 150ms"></span>
      <span class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 300ms"></span>
    </div>
    <span class="ml-3 text-gray-500 text-sm">思考中...</span>
  </div>
</template>

<style scoped>
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-6px);
  }
}

.animate-bounce {
  animation: bounce 0.6s infinite;
}
</style>