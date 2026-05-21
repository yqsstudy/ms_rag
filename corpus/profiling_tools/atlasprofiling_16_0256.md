---
title: "msptiBuffersCallbackRequestFunc"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0256.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0256.html"
---

# msptiBuffersCallbackRequestFunc

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

向MSPTI注册回调函数，申请Activity Buffer的存储空间。用户（订阅者）在使用Activity API时，需要自定义该函数并在MSPTI注册，当Activity Buffer的存储空间不足时，MSPTI会调用该函数申请新的存储空间。

#### 函数原型

```
1
```

```
typedef void(*msptiBuffersCallbackRequestFunc)(uint8_t **buffer, size_t *size, size_t *maxNumRecords)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

buffer

输出

设置Activity Buffer的地址。

size

输出

设置Activity Buffer的大小。（建议用户申请至少2MB大小的内存）

maxNumRecords

输出

设置Activity Buffer中Records的数量。一般设置为0。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

#### 返回值说明

无
**父主题：**[Typedef类型](atlasprofiling_16_0255.html)