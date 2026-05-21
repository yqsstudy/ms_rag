---
title: "msptiEnableDomain"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0285.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0285.html"
---

# msptiEnableDomain

#### 产品支持情况

产品

是否支持

Atlas A3 训练系列产品/Atlas A3 推理系列产品

√

Atlas A2 训练系列产品/Atlas A2 推理系列产品

√

Atlas 200I/500 A2 推理产品

√

Atlas 推理系列产品

x

Atlas 训练系列产品

x
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### 功能说明

为特定domain的订阅者开启或关闭所有回调。

当这个CallbackId所在位置触发时，MSPTI会主动调用msptiSubscribe接口注册的回调函数。

#### 函数原型

```
1
```

```
msptiResult msptiEnableDomain(uint32_t enable, msptiSubscriberHandle subscriber, msptiCallbackDomain domain)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

enable

输入

回调的开关，配置该参数表示开启，未配置表示关闭。

subscriber

输入

订阅者句柄。

domain

输入

组件，当前仅支持Runtime。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

#### 返回值说明

返回MSPTI_SUCCESS表示成功，用户或域无效时返回MSPTI_ERROR_INVALID_PARAMETER，表示失败。
**父主题：**[Function类型](atlasprofiling_16_0281.html)