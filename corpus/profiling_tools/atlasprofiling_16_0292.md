---
title: "msptiApiCallbackSite"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0292.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0292.html"
---

# msptiApiCallbackSite

[msptiApiCallbackSite为msptiCallbackData](atlasprofiling_16_0296.html#ZH-CN_TOPIC_0000002536158475)调用的枚举类。

指定API调用中发出回调的点。定义如下：

```
1
2
3
4
5
```

```
typedef enum {
	MSPTI_API_ENTER = 0,    // 在进入API时回调
	MSPTI_API_EXIT = 1,    // 退出API后回调
	MSPTI_API_CBSITE_FORCE_INT = 0x7fffffff
} msptiApiCallbackSite;

```
|  |  |
| --- | --- |
**父主题：**[Enumeration类型](atlasprofiling_16_0290.html)