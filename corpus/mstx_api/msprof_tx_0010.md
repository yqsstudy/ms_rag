---
title: "mstxDomainRangeEnd"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0010.html"
date_collected: "2026-05-04"
category: "mstx_api"
original_path: "zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0010.html"
---

# mstxDomainRangeEnd

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

在指定的domain内，标识时间段事件的结束。

如果传入的domain已被销毁，日志打印告警提示，接口不再执行打点流程。

#### 函数原型

```
1
```

```
void mstxDomainRangeEnd(mstxDomainHandle_t domain, mstxRangeId id)

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

指定的domain句柄。

id

输入

通过mstxDomainRangeStartA接口返回的id。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值

无