---
title: "mstxRangeEnd"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0118.html"
date_collected: "2026-05-04"
category: "mstx_api"
original_path: "zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0118.html"
---

# mstxRangeEnd

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

mstx range指定范围能力的结束位置标记。

#### 函数原型

C/C++函数原型：

```
void mstxRangeEnd(mstxRangeId id)
```

Python函数：

```
mstx.range_end(range_id)
```

#### 参数说明
**表1**参数说明
参数

输入/输出

说明

id（C/C++）

输入

通过mstxRangeStartA返回的ID（C/C++）。

range_id（Python）

输入

通过mstx.range_start返回的range_id（Python）。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值

如果返回0，则表示失败。

#### 调用示例

[C/C++调用：mstxRangeEnd接口需要与mstxRangeStartA配合使用，具体示例请参考C/C++调用方法](atlasopdev_16_0117.html#ZH-CN_TOPIC_0000002503927654__zh-cn_topic_0000002016210401_li2335161515348)。

[Python调用：mstx.range_end接口需要与mstx.range_start配合使用，具体示例请参考Python调用方法](atlasopdev_16_0117.html#ZH-CN_TOPIC_0000002503927654__zh-cn_topic_0000002016210401_li19799155136)。