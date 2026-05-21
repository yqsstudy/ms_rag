---
title: "msptiResult"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0299.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0299.html"
---

# msptiResult

msptiResult是MSPTI返回的错误和结果代码，为枚举类。定义如下：

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
```

```
typedef enum {
	MSPTI_SUCCESS = 0,    // MSPTI执行成功，无错误
	MSPTI_ERROR_INVALID_PARAMETER = 1,    // funcBufferRequested或funcBufferCompleted为NULL时返回，表示MSPTI执行失败
	MSPTI_ERROR_MULTIPLE_SUBSCRIBERS_NOT_SUPPORTED = 2,    // 已存在MSPTI用户时返回，表示MSPTI执行失败
	MSPTI_ERROR_MAX_LIMIT_REACHED = 3,    // Activity Buffer没有更多的Record数据时返回，表示MSPTI执行失败
	MSPTI_ERROR_DEVICE_OFFLINE = 4,    // 无法获取DEVICE侧信息
	MSPTI_ERROR_INNER = 999,    // 无法初始化MSPTI时返回，表示MSPTI执行失败
	MSPTI_ERROR_FORCE_INT = 0x7fffffff
} msptiResult;

```
|  |  |
| --- | --- |
**父主题：**[Enumeration类型](atlasprofiling_16_0298.html)