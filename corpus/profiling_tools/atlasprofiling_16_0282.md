---
title: "msptiSubscribe"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0282.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0282.html"
---

# msptiSubscribe

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

通过该接口向MSPTI注册回调函数。用户（订阅者）在调用MSPTI接口前，需要预先调用该接口，同一时刻只支持一个订阅者。

#### 函数原型

```
1
```

```
msptiResult msptiSubscribe(msptiSubscriberHandle *subscriber, msptiCallbackFunc callback, void *userdata)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

subscriber

输入

订阅者的句柄地址。

callback

输入

回调函数。

userdata

输入

订阅者自定义的数据地址。订阅者数据将通过该参数传递给回调函数。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

#### 返回值说明

返回MSPTI_SUCCESS表示成功，无法初始化MSPTI时返回MSPTI_ERROR_INNER、已存在MSPTI用户时返回MSPTI_ERROR_MULTIPLE_SUBSCRIBERS_NOT_SUPPORTED或如果用户为空时返回MSPTI_ERROR_INVALID_PARAMETER，表示失败。
**父主题：**[Function类型](atlasprofiling_16_0281.html)