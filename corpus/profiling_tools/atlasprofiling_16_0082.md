---
title: "示例代码"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0082.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0082.html"
---

# 示例代码

以下是关键步骤的代码示例，不可以直接拷贝编译运行，仅供参考。

```
 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
```

```
// 设置全局资源属性
if (msServiceProfiler::Tracer::IsEnable()) {
    msServiceProfiler::TraceContext::addResAttribute("service.name", "my-service");
    msServiceProfiler::TraceContext::addResAttribute("service.version", "1.0.0");
}
auto& ctx = msServiceProfiler::TraceContext::GetTraceCtx();
size_t indexHeader = ctx.ExtractAndAttach(traceParentHeader, b3Header);
size_t index = ctx.Attach(TraceId{1, 1}, SpanId{1}, true);  // Span 会自动Attach，一般不需要主动调用该函数
// 创建跨度
auto span = msServiceProfiler::Tracer::StartSpanAsActive("MyOperation", "MyModule");
// 设置属性
span.SetAttribute("key", "value")
    .SetStatus(true, "Operation completed successfully");
span.End();
ctx.Unattach(index);
ctx.Unattach(indexHeader);

```
|  |  |
| --- | --- |
**父主题：**[Trace数据监控](atlasprofiling_16_0080.html)