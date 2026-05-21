// 消息类型
export interface Message {
  id: string
  type: 'user' | 'assistant'
  content: string
  sources?: Source[]
  images?: Image[]
  questionType?: string
  responseTime?: number
  relatedTopics?: RelatedTopic[]
  cached?: boolean
  cacheLevel?: string
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

// 相关主题
export interface RelatedTopic {
  title: string
  doc_id: string
  relation: string
}

// SSE事件数据
export interface SSEMetadata {
  question_type: string
  keywords: string[]
  sources: Source[]
  related_topics?: RelatedTopic[]
  cached?: boolean
  cache_level?: string
}

export interface SSEAnswer {
  content: string
}

export interface SSEDone {
  tokens_used: number
  response_time_ms: number
  model: string
}

export interface SSEError {
  error: string
}