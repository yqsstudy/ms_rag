# 前端开发指南

前端基于 Vue 3、TypeScript、Vite 和 Tailwind CSS，开发模式运行在 3000 端口，生产构建输出到仓库根目录的 `static/`，由 FastAPI 后端托管。

## 安装依赖

```bash
cd frontend
npm install
```

## 开发模式

```bash
# 终端 1：启动后端 API，端口 8000
python -m src.main

# 终端 2：启动前端开发服务器，端口 3000
cd frontend
npm run dev
```

访问 http://localhost:3000。Vite 会把 `/api` 和 `/corpus` 请求代理到 http://localhost:8000。

## 构建生产版本

```bash
cd frontend
npm run build
```

`npm run build` 会先执行 `vue-tsc -b` 类型检查，再由 Vite 构建，产物输出到 `../static/`。

生产模式启动：

```bash
python -m src.main
```

访问 http://localhost:8000。

## 项目结构

```text
frontend/
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
├── tsconfig.json
└── src/
    ├── main.ts                    # 入口
    ├── App.vue                    # 根组件、页面布局和会话入口
    ├── style.css                  # 全局样式
    ├── components/
    │   ├── ChatInput.vue          # 输入框
    │   ├── MessageCard.vue        # 用户/助手消息卡片
    │   ├── SourceCard.vue         # 来源文档卡片
    │   ├── ImageGallery.vue       # 来源图片展示
    │   ├── QuickQuestions.vue     # 快捷问题
    │   ├── RelatedTopics.vue      # 相关主题推荐
    │   └── LoadingDots.vue        # 加载动画
    ├── composables/
    │   └── useChat.ts             # 聊天状态、SSE 请求和消息组装
    └── types/
        └── index.ts               # Message、Source、SSE 事件等类型
```

## 前端数据流

1. 用户通过 `ChatInput.vue` 或 `QuickQuestions.vue` 提交问题。
2. `App.vue` 调用 `useChat.ts` 的发送逻辑。
3. `useChat.ts` 请求 `/api/v1/qa/stream`，按 SSE 事件更新当前助手消息。
4. `metadata` 事件写入问题类型、关键词、来源文档、相关主题和缓存信息。
5. `answer` 事件持续追加 Markdown 内容。
6. `done` 事件写入响应时间和模型信息。
7. `MessageCard.vue` 渲染回答、来源、图片、缓存标识和相关主题。

## 后端 SSE 事件约定

### metadata

```ts
interface SSEMetadata {
  question_type: string
  keywords: string[]
  sources: Source[]
  related_topics?: RelatedTopic[]
  cached?: boolean
  cache_level?: string
}
```

### answer

```ts
interface SSEAnswer {
  content: string
}
```

### done

```ts
interface SSEDone {
  tokens_used: number
  response_time_ms: number
  model: string
}
```

### error

```ts
interface SSEError {
  error: string
}
```

## 常用命令

```bash
npm run dev       # 开发服务器
npm run build     # 类型检查 + 生产构建
npm run preview   # 预览构建产物
```

## 注意事项

- 生产模式下后端只托管 `static/` 中的构建产物，前端改动后需要重新执行 `npm run build`。
- Markdown 内容使用 `marked` 渲染，并通过 `DOMPurify` 做 XSS 清理。
- 与后端字段变更相关的类型集中维护在 `src/types/index.ts`。
- 相关主题点击会作为新问题发送，后端返回的 `related_topics` 需要包含 `title`、`doc_id`、`relation`。
