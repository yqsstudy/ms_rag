# 前端开发指南

## 安装依赖

```bash
cd frontend
npm install
```

## 开发模式

```bash
# 启动前端开发服务器 (端口 3000)
npm run dev

# 同时需要启动后端 API 服务 (端口 8000)
cd ..
python -m src.main
```

访问 http://localhost:3000

## 构建生产版本

```bash
npm run build
```

构建产物输出到 `../static/` 目录。

## 生产模式

```bash
# 构建前端
cd frontend
npm run build

# 启动后端 (自动托管静态文件)
cd ..
python -m src.main
```

访问 http://localhost:8000

## 项目结构

```
frontend/
├── src/
│   ├── main.ts              # 入口
│   ├── App.vue              # 根组件
│   ├── style.css            # 全局样式
│   ├── components/          # 组件
│   │   ├── ChatInput.vue
│   │   ├── MessageCard.vue
│   │   ├── SourceCard.vue
│   │   ├── ImageGallery.vue
│   │   ├── QuickQuestions.vue
│   │   └── LoadingDots.vue
│   ├── composables/         # 组合式函数
│   │   └── useChat.ts
│   └── types/               # 类型定义
│       └── index.ts
├── index.html
├── package.json
└── vite.config.ts
```
