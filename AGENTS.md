# OpenCode Guidance: MS-RAG

## Architecture & Workspaces

- Monorepo with a FastAPI backend and a Vue 3/Vite frontend.
- Backend source lives in `src/`; the application entry point is `src/main.py` and should be run as `python -m src.main` from the repository root.
- Frontend source lives in `frontend/`; production builds are emitted to root `static/`, which FastAPI serves.
- Generated RAG data lives under `data/`; source Markdown knowledge documents live under `corpus/`.

## RAG Execution Flow

- `scripts/build_index.py` loads Markdown documents, cleans them, creates parent chunks and child chunks, stores parent chunks in `data/docstore/`, embeds child chunks into Chroma, rebuilds BM25, writes `data/graph.json`, and records incremental state in `data/index_state.json`.
- Online QA enters `RAGPipeline`, checks L1/L2/L3 caches, embeds the query, performs async hybrid retrieval against Chroma and BM25, reranks, applies knowledge-graph enhancement, builds context, renders the prompt, and calls the configured LLM.
- The retriever returns child chunk hits but can hydrate parent chunk content through `DocumentStore` for fuller context.
- Knowledge graph enhancement uses parent, sibling, child, and reference relationships and also returns related topics for the frontend.
- Cache endpoints are exposed at `/api/v1/cache/stats` and `/api/v1/cache/clear`.

## Critical Commands

- **Run Backend:** `python -m src.main`
- **Run Frontend Dev:** `cd frontend && npm run dev`
- **Build Frontend:** `cd frontend && npm run build`
- **Build Index Incrementally:** `python scripts/build_index.py`
- **Force Rebuild Index:** `python scripts/build_index.py --force`
- **Tests:** `pytest`
- **Lint:** `ruff check .`

## Configuration

- Main configuration is `config/system.yaml`.
- LLM settings use environment substitution: `LLM_PROVIDER`, `LLM_MODEL`, `LLM_API_KEY`, and `LLM_BASE_URL`.
- Provider-specific keys such as `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, and `DEEPSEEK_API_KEY` are also supported.
- Runtime config can be overridden with `MS_RAG_` environment variables and `__` for nesting, e.g. `MS_RAG_API__PORT=9000`.

## Frontend Notes

- Vite dev server proxies `/api` and `/corpus` requests to the backend on port 8000.
- `frontend/src/composables/useChat.ts` handles streaming chat state and SSE parsing.
- `frontend/src/components/MessageCard.vue` renders answer Markdown, sources, images, cache hit metadata, and related topics.
- `frontend/src/components/RelatedTopics.vue` renders KG-related topic suggestions.
- Any frontend change that must be visible through the FastAPI-served production app requires `cd frontend && npm run build`.

## Gotchas & Conventions

- Always run Python scripts from the repo root so `src.*` imports resolve correctly.
- Do not run scripts via `cd scripts && python build_index.py`; use `python scripts/build_index.py`.
- If the HuggingFace model download is slow, prefix index builds with `HF_ENDPOINT=https://hf-mirror.com`.
- `data/` is generated state; rebuild it with `scripts/build_index.py` instead of editing generated files by hand.
- `corpus/` contains the source knowledge base and can be large; avoid treating every corpus Markdown file as project documentation.
