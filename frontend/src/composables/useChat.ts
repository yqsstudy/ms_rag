import { ref } from 'vue'
import type { Message, Source, Image, SSEMetadata, SSEAnswer, SSEDone } from '@/types'

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

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body?.getReader()
    if (!reader) throw new Error('No reader available')

    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      let currentEvent = ''
      for (const line of lines) {
        if (line.startsWith('event: ')) {
          currentEvent = line.slice(7).trim()
        } else if (line.startsWith('data: ') && currentEvent) {
          try {
            const data = JSON.parse(line.slice(6))
            handleSSEEvent(currentEvent, data, message)
          } catch (e) {
            console.error('Failed to parse SSE data:', line)
          }
          currentEvent = ''
        }
      }
    }
  }

  // 处理SSE事件
  function handleSSEEvent(event: string, data: unknown, message: Message) {
    switch (event) {
      case 'metadata':
        {
          const metadata = data as SSEMetadata
          message.questionType = metadata.question_type
          message.sources = metadata.sources || []
          message.images = extractImages(metadata.sources)
        }
        break
      case 'answer':
        {
          const answer = data as SSEAnswer
          message.content += answer.content
        }
        break
      case 'done':
        {
          const done = data as SSEDone
          message.responseTime = done.response_time_ms
        }
        break
      case 'error':
        message.content = `错误: ${(data as { error: string }).error}`
        break
    }
  }

  // 提取图片
  function extractImages(sources: Source[]): Image[] {
    const images: Image[] = []
    const seen = new Set<string>()
    for (const source of sources) {
      if (source.images) {
        for (const img of source.images) {
          if (!seen.has(img.path)) {
            seen.add(img.path)
            images.push(img)
          }
        }
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