---
title: "msptiActivity"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0268.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0268.html"
---

# msptiActivity

**msptiActivity为Activity Record的基础结构体，Activity API使用msptiActivity作为Activity的通用表示，kind**字段用于确定特定的Activity类型，由此可以将msptiActivity对象转换为适合该类型的特定的Activity Record类型。

定义如下：

```
1
2
3
```

```
typedef struct PACKED_ALIGNMENT {
	msptiActivityKind kind;   // Activity类型
} msptiActivity;

```
|  |  |
| --- | --- |
**父主题：**[Data Structure类型](atlasprofiling_16_0267.html)