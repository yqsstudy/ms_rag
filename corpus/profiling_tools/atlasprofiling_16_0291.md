---
title: "msptiCallbackDomain"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0291.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0291.html"
---

# msptiCallbackDomain

[msptiCallbackDomain为msptiEnableCallback](atlasprofiling_16_0284.html#ZH-CN_TOPIC_0000002536158469)[、msptiEnableDomain](atlasprofiling_16_0285.html#ZH-CN_TOPIC_0000002504198654)[和msptiCallbackFunc](atlasprofiling_16_0287.html#ZH-CN_TOPIC_0000002536038443)调用的回调领域枚举类。

每个枚举值代表一组相关API函数或CANN驱动程序活动的回调点。定义如下：

```
1
2
3
4
5
6
7
```

```
typedef enum {
	MSPTI_CB_DOMAIN_INVALID = 0,    // 非法值
	MSPTI_CB_DOMAIN_RUNTIME = 1,    // Runtime API相关回调点
	MSPTI_CB_DOMAIN_HCCL = 2,    // 通信API相关回调点
	MSPTI_CB_DOMAIN_SIZE,
	MSPTI_CB_DOMAIN_FORCE_INT = 0x7fffffff
} msptiCallbackDomain;

```
|  |  |
| --- | --- |
**父主题：**[Enumeration类型](atlasprofiling_16_0290.html)