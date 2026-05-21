---
title: "SetAttribute"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0093.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0093.html"
---

# SetAttribute

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

设置跨度属性。

#### 函数原型

```
1
```

```
Span& SetAttribute(const char* attrName, const char* value)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

attrName

输入

属性名 |。

value

输入

属性值。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值说明

返回Span类对象的引用，该引用支持链式调用。
**父主题：**[Span类](atlasprofiling_16_0090.html)