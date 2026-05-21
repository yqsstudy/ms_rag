---
title: "mstxDomainDestroy"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0007.html"
date_collected: "2026-05-04"
category: "mstx_api"
original_path: "zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0007.html"
---

# mstxDomainDestroy

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

√

Atlas 训练系列产品

√
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### 功能说明

销毁指定的domain，销毁后的domain不能再次使用，需要重新创建。

#### 函数原型

```
1
```

```
void mstxDomainDestroy (mstxDomainHandle_t domain)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

domain

输入

指定要销毁的domain句柄。
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 返回值

无