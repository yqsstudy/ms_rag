---
title: "msptiCallbackData"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0296.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0296.html"
---

# msptiCallbackData

[msptiCallbackData为msptiCallbackFunc](atlasprofiling_16_0287.html#ZH-CN_TOPIC_0000002536038443)**的cbdata**对应的结构体，用于指定传递到回调函数的数据。

定义如下：

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
```

```
typedef struct {
    msptiApiCallbackSite callbackSite;    // 回调触发点的位置（开始或结束）
    const char *functionName;    // 当前函数名称
    const void *functionParams;    // 当前函数的参数
    const void *functionReturnValue;    // 指向Runtime或驱动API返回值的指针
    const char *symbolName;    // 当前函数所操作的符号的名称
    uint64_t correlationId;    // 本ID可以用于关联msptiCallbackData和activity记录。在runtime回调函数调用场景中activity记录为msptiActivityApi数据，本ID与记录runtime函数调用的msptiActivityApi数据中的correlationId相同，可以用于数据关联
    uint64_t reserved1;    // 内部预留，未定义
    uint64_t reserved2;    // 内部预留，未定义
    uint64_t *correlationData;    // 提供一个用于在runtime或者驱动API的入口和出口共享数据的指针。这个字段可以用于将64位数据从入口回调函数传递到出口回调函数

} msptiCallbackData;

```
|  |  |
| --- | --- |
**父主题：**[Data Structure类型](atlasprofiling_16_0295.html)