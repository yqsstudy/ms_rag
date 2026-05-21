# 前端详细设计文档

## 一、技术选型

当前前端已实现流式问答、Markdown 安全渲染、来源文档展示、图片展示、缓存命中标识和知识图谱相关主题推荐。流式处理集中在 `useChat.ts`，后端通过 `/api/v1/qa/stream` 返回 `metadata`、`answer`、`done` 和 `error` 事件。

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue 3 | 3.4+ | 前端框架 |
| Vite | 5.0+ | 构建工具 |
| TypeScript | 5.0+ | 类型安全 |
| Tailwind CSS | 3.4+ | 样式框架 |
| Marked | 12.0+ | Markdown渲染 |
| DOMPurify | 3.0+ | XSS防护 |

---

## 二、项目结构

```
frontend/
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
├── tsconfig.json
└── src/
    ├── main.ts                    # 入口文件
    ├── App.vue                    # 根组件
    ├── style.css                  # 全局样式
    │
    ├── components/                # 组件目录
    │   ├── ChatInput.vue          # 输入框组件
    │   ├── MessageCard.vue        # 消息卡片组件
    │   ├── SourceCard.vue         # 来源文档卡片
    │   ├── ImageGallery.vue       # 图片展示组件
    │   ├── QuickQuestions.vue     # 快捷问题组件
    │   ├── RelatedTopics.vue      # 相关主题推荐组件
    │   └── LoadingDots.vue        # 加载动画组件
    │
    ├── composables/               # 组合式函数
    │   └── useChat.ts             # 聊天逻辑与SSE流式处理
    │
    ├── types/                     # 类型定义
    │   └── index.ts               # 接口类型
    │
    └── assets/                    # 静态资源
        └── logo.svg
```

---

## 三、界面布局设计

### 3.1 整体布局

```
┌─────────────────────────────────────────────────────────────┐
│  Header (固定顶部)                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🎯 性能定位指南RAG系统              [清除对话]      │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Main Content (可滚动区域)                                   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  QuickQuestions (快捷问题)                           │   │
│  │  [如何定位通信问题?] [msprof怎么用?] [什么是快慢卡?]  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  MessageCard (用户问题)                              │   │
│  │  模型训练慢怎么定位？                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  MessageCard (AI回答)                                │   │
│  │  ─────────────────────────────────────────────────  │   │
│  │  针对模型训练速度慢的问题，建议按以下步骤定位...      │   │
│  │  ─────────────────────────────────────────────────  │   │
│  │  📄 来源文档                                         │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐            │   │
│  │  │性能定位  │ │工具使用  │ │通信分析  │            │   │
│  │  │⭐ 0.92   │ │⭐ 0.85   │ │⭐ 0.78   │            │   │
│  │  └──────────┘ └──────────┘ └──────────┘            │   │
│  │  ─────────────────────────────────────────────────  │   │
│  │  🖼️ 相关图片                                         │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │ 图1: 详细排查流程图                           │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Footer (固定底部)                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  [输入问题...]                              [发送]   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 响应式设计

```
桌面端 (≥1024px):
┌────────────────────────────────────┐
│  内容最大宽度: 900px，居中显示      │
└────────────────────────────────────┘

平板端 (768px - 1023px):
┌──────────────────────────┐
│  内容宽度: 100%，内边距   │
└──────────────────────────┘

移动端 (<768px):
┌────────────────┐
│  紧凑布局       │
│  来源文档折叠   │
└────────────────┘
```

---

## 四、组件详细设计

### 4.1 App.vue - 根组件

```vue
<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="fixed top-0 w-full bg-white shadow-sm z-10">
      <div class="max-w-4xl mx-auto px-4 py-3 flex justify-between items-center">
        <h1 class="text-xl font-bold text-primary">
          🎯 性能定位指南RAG系统
        </h1>
        <button @click="clearMessages" class="text-gray-500 hover:text-gray-700">
          清除对话
        </button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="pt-16 pb-24">
      <div class="max-w-4xl mx-auto px-4">
        <!-- 快捷问题 -->
        <QuickQuestions v-if="messages.length === 0" @select="handleQuickQuestion" />

        <!-- 消息列表 -->
        <div class="space-y-4">
          <MessageCard
            v-for="(msg, index) in messages"
            :key="index"
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
```

### 4.2 ChatInput.vue - 输入框组件

```vue
<template>
  <div class="max-w-4xl mx-auto px-4 py-3">
    <div class="flex gap-2">
      <input
        v-model="inputValue"
        type="text"
        placeholder="输入性能相关问题，如：模型训练慢怎么定位？"
        class="flex-1 px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
        @keyup.enter="handleSend"
        :disabled="disabled"
      />
      <button
        @click="handleSend"
        :disabled="disabled || !inputValue.trim()"
        class="px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary-dark disabled:opacity-50"
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
```

### 4.3 MessageCard.vue - 消息卡片组件

```vue
<template>
  <div class="bg-white rounded-lg shadow-sm overflow-hidden">
    <!-- 用户问题 -->
    <div v-if="message.type === 'user'" class="p-4 bg-blue-50">
      <div class="flex items-start gap-2">
        <span class="text-blue-600">👤</span>
        <p class="text-gray-800">{{ message.content }}</p>
      </div>
    </div>

    <!-- AI回答 -->
    <div v-else class="p-4">
      <!-- 回答内容 -->
      <div class="flex items-start gap-2 mb-4">
        <span class="text-green-600">🤖</span>
        <div class="flex-1 prose prose-sm max-w-none" v-html="renderedContent"></div>
      </div>

      <!-- 来源文档 -->
      <div v-if="message.sources?.length" class="mt-4 pt-4 border-t">
        <h4 class="text-sm font-medium text-gray-500 mb-2">📄 来源文档</h4>
        <div class="flex flex-wrap gap-2">
          <SourceCard
            v-for="source in message.sources"
            :key="source.doc_id"
            :source="source"
          />
        </div>
      </div>

      <!-- 相关图片 -->
      <div v-if="message.images?.length" class="mt-4 pt-4 border-t">
        <h4 class="text-sm font-medium text-gray-500 mb-2">🖼️ 相关图片</h4>
        <ImageGallery :images="message.images" />
      </div>

      <!-- 元信息 -->
      <div class="mt-4 pt-4 border-t text-xs text-gray-400 flex gap-4">
        <span>问题类型: {{ message.questionType }}</span>
        <span>响应时间: {{ message.responseTime }}ms</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import type { Message } from '@/types'
import SourceCard from './SourceCard.vue'
import ImageGallery from './ImageGallery.vue'

const props = defineProps<{
  message: Message
}>()

const renderedContent = computed(() => {
  const raw = marked.parse(props.message.content || '') as string
  return DOMPurify.sanitize(raw)
})
</script>
```

### 4.4 SourceCard.vue - 来源文档卡片

```vue
<template>
  <a
    :href="source.source_url"
    target="_blank"
    class="inline-flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
  >
    <div class="flex-1">
      <p class="text-sm font-medium text-gray-800 line-clamp-1">
        {{ source.title }}
      </p>
      <p class="text-xs text-gray-500">
        相关度: {{ (source.relevance_score * 100).toFixed(0) }}%
      </p>
    </div>
    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
    </svg>
  </a>
</template>

<script setup lang="ts">
import type { Source } from '@/types'

defineProps<{
  source: Source
}>()
</script>
```

### 4.5 ImageGallery.vue - 图片展示组件

```vue
<template>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
    <div
      v-for="image in images"
      :key="image.path"
      class="border rounded-lg overflow-hidden hover:shadow-md transition-shadow cursor-pointer"
      @click="openImage(image)"
    >
      <div class="aspect-video bg-gray-100 flex items-center justify-center">
        <img
          :src="getImageUrl(image.path)"
          :alt="image.caption"
          class="max-w-full max-h-full object-contain"
          loading="lazy"
        />
      </div>
      <p class="p-2 text-sm text-gray-600 text-center">
        {{ image.figure_num ? `图${image.figure_num}: ` : '' }}{{ image.caption }}
      </p>
    </div>
  </div>

  <!-- 图片弹窗 -->
  <Teleport to="body">
    <div
      v-if="selectedImage"
      class="fixed inset-0 bg-black/80 flex items-center justify-center z-50"
      @click="selectedImage = null"
    >
      <img
        :src="getImageUrl(selectedImage.path)"
        :alt="selectedImage.caption"
        class="max-w-[90vw] max-h-[90vh] object-contain"
      />
    </div>
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
  return `/api/v1/images/${path.replace('images/', '')}`
}

const openImage = (image: Image) => {
  selectedImage.value = image
}
</script>
```

### 4.6 QuickQuestions.vue - 快捷问题组件

```vue
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
        class="px-4 py-2 bg-white border rounded-full hover:bg-primary hover:text-white hover:border-primary transition-colors text-sm"
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
```

### 4.7 LoadingDots.vue - 加载动画

```vue
<template>
  <div class="flex items-center justify-center py-4">
    <div class="flex gap-1">
      <span class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 0ms"></span>
      <span class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 150ms"></span>
      <span class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 300ms"></span>
    </div>
    <span class="ml-2 text-gray-500 text-sm">思考中...</span>
  </div>
</template>
```

---

## 五、类型定义

### types/index.ts

```typescript
// 消息类型
export interface Message {
  id: string
  type: 'user' | 'assistant'
  content: string
  sources?: Source[]
  images?: Image[]
  questionType?: string
  responseTime?: number
}

// 来源文档
export interface Source {
  doc_id: string
  title: string
  section: string
  source_url: string
  relevance_score: number
  images?: Image[]
}

// 图片
export interface Image {
  figure_num?: string
  caption: string
  path: string
}

// API响应
export interface QAResponse {
  code: number
  message: string
  data: {
    answer: string
    question_type: string
    keywords: string[]
    sources: Source[]
    metadata: {
      response_time_ms: number
      model: string
    }
  }
}

// SSE事件类型
export type SSEEvent = 'metadata' | 'answer' | 'done' | 'error'
```

---

## 六、核心逻辑

### composables/useChat.ts

```typescript
import { ref } from 'vue'
import type { Message, Source, Image } from '@/types'

export function useChat() {
  const messages = ref<Message[]>([])
  const isLoading = ref(false)

  // 发送问题
  async function sendMessage(query: string) {
    if (!query.trim() || isLoading.value) return

    // 添加用户消息
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: query,
    }
    messages.value.push(userMessage)

    // 创建AI消息占位
    const aiMessage: Message = {
      id: (Date.now() + 1).toString(),
      type: 'assistant',
      content: '',
      sources: [],
      images: [],
    }
    messages.value.push(aiMessage)

    isLoading.value = true

    try {
      // 使用流式API
      await streamAnswer(query, aiMessage)
    } catch (error) {
      aiMessage.content = '抱歉，发生了错误，请稍后重试。'
      console.error('Chat error:', error)
    } finally {
      isLoading.value = false
    }
  }

  // 流式获取回答
  async function streamAnswer(query: string, message: Message) {
    const response = await fetch('/api/v1/qa/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    })

    const reader = response.body?.getReader()
    const decoder = new TextDecoder()

    if (!reader) throw new Error('No reader available')

    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (line.startsWith('event: ')) {
          const eventType = line.slice(7)
          const dataLine = lines[lines.indexOf(line) + 1]
          if (dataLine?.startsWith('data: ')) {
            const data = JSON.parse(dataLine.slice(6))
            handleSSEEvent(eventType, data, message)
          }
        }
      }
    }
  }

  // 处理SSE事件
  function handleSSEEvent(event: string, data: any, message: Message) {
    switch (event) {
      case 'metadata':
        message.questionType = data.question_type
        message.sources = data.sources || []
        // 提取图片
        message.images = extractImages(data.sources)
        break
      case 'answer':
        message.content += data.content
        break
      case 'done':
        message.responseTime = data.response_time_ms
        break
      case 'error':
        message.content = `错误: ${data.error}`
        break
    }
  }

  // 提取图片
  function extractImages(sources: Source[]): Image[] {
    const images: Image[] = []
    for (const source of sources) {
      if (source.images) {
        images.push(...source.images)
      }
    }
    return images
  }

  // 清除对话
  function clearMessages() {
    messages.value = []
  }

  return {
    messages,
    isLoading,
    sendMessage,
    clearMessages,
  }
}
```

---

## 七、样式设计

### style.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --primary: #0066CC;
  --primary-dark: #0052A3;
  --primary-light: #E6F2FF;
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

/* Markdown样式 */
.prose pre {
  background: #f6f8fa;
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
}

.prose code {
  background: #f6f8fa;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-size: 0.875em;
}

.prose table {
  width: 100%;
  border-collapse: collapse;
}

.prose th,
.prose td {
  border: 1px solid #e5e7eb;
  padding: 0.5rem;
}

.prose th {
  background: #f9fafb;
}

/* 动画 */
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
```

---

## 八、API集成

### 后端API端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/qa` | POST | 同步问答 |
| `/api/v1/qa/stream` | POST | 流式问答(SSE) |
| `/api/v1/images/{path}` | GET | 获取图片 |

### 后端需要新增的图片服务

```python
# src/api/routes.py 新增
from fastapi.responses import FileResponse

@router.get("/images/{image_path:path}")
async def get_image(image_path: str):
    """获取图片"""
    image_file = Path(f"./corpus/performance_guide/images/{image_path}")
    if not image_file.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_file)
```

---

## 九、构建配置

### vite.config.ts

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: '../static',
    emptyOutDir: true,
  },
})
```

### package.json

```json
{
  "name": "ms-rag-frontend",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "marked": "^12.0.0",
    "dompurify": "^3.0.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "typescript": "^5.0.0",
    "vite": "^5.0.0",
    "vue-tsc": "^2.0.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}
```

---

## 十、开发流程

```bash
# 1. 创建前端目录
cd ms_rag
mkdir frontend

# 2. 初始化项目
cd frontend
npm create vite@latest . -- --template vue-ts

# 3. 安装依赖
npm install marked dompurify
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# 4. 开发
npm run dev

# 5. 构建
npm run build
# 输出到 ../static/ 目录
```

---

## 十一、文件清单

需要创建的文件：

| 文件 | 说明 |
|------|------|
| `frontend/package.json` | 项目配置 |
| `frontend/vite.config.ts` | Vite配置 |
| `frontend/tailwind.config.js` | Tailwind配置 |
| `frontend/index.html` | 入口HTML |
| `frontend/src/main.ts` | 入口脚本 |
| `frontend/src/App.vue` | 根组件 |
| `frontend/src/style.css` | 全局样式 |
| `frontend/src/types/index.ts` | 类型定义 |
| `frontend/src/composables/useChat.ts` | 聊天逻辑 |
| `frontend/src/components/ChatInput.vue` | 输入组件 |
| `frontend/src/components/MessageCard.vue` | 消息卡片 |
| `frontend/src/components/SourceCard.vue` | 来源卡片 |
| `frontend/src/components/ImageGallery.vue` | 图片组件 |
| `frontend/src/components/QuickQuestions.vue` | 快捷问题 |
| `frontend/src/components/LoadingDots.vue` | 加载动画 |

---

*文档版本: v1.0*
*创建日期: 2026-05-02*
