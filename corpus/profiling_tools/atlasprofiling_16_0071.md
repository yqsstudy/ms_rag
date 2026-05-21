---
title: "Link"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0071.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0071.html"
---

# Link

#### 产品支持情况

产品

是否支持

Atlas 800I A2 推理产品

√

Atlas 200T A2 Box16 异构子框

√

Atlas 300I Duo 推理卡+Atlas 800 推理服务器（型号：3000）

√

注：暂不支持其他产品。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |

#### 功能说明

记录不同资源之间的关联，实际应用时不同模块对同一个请求使用不同的编号。将两个系统的编号关联起来。

#### 函数原型

```
1
```

```
void Link(const ResID &fromRid, const ResID &toRid)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

fromRid

输入

ResID类型，ResID可以由字符串或数值隐式转换。

toRid

输入

ResID类型，ResID可以由字符串或数值隐式转换。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值说明

无
**父主题：**[服务化调优](atlasprofiling_16_0059.html)