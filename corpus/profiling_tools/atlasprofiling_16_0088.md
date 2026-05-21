---
title: "Unattach"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0088.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0088.html"
---

# Unattach

#### 产品支持情况

[昇腾AI处理器与昇腾产品的对应关系，请参见《昇腾产品形态说明](https://www.hiascend.com/document/detail/zh/AscendFAQ/ProduTech/productform/hardwaredesc_0001.html)》

产品

是否支持

Atlas A3 训练系列产品/Atlas A3 推理系列产品

x

Atlas A2 训练系列产品/Atlas A2 推理系列产品

√

Atlas 200I/500 A2 推理产品

x

Atlas 推理系列产品

√

Atlas 训练系列产品

x
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

针对Atlas A2 训练系列产品/Atlas A2 推理系列产品，当前仅支持该系列产品中的Atlas 800I A2 推理产品。

针对Atlas 推理系列产品，当前仅支持该系列产品中的Atlas 300I Duo 推理卡+Atlas 800 推理服务器（型号：3000）。

#### 功能说明

解除指定索引Trace的上下文。

#### 函数原型

```
1
```

```
void Unattach(const size_t index)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

index

输入

要解除的上下文索引。
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 返回值说明

无
**父主题：**[TraceContext类](atlasprofiling_16_0083.html)