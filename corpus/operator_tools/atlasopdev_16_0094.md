---
title: "L2Cache（L2 Cache命中率）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0094.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0094.html"
---

# L2Cache（L2 Cache命中率）

L2 Cache命中率数据L2Cache.csv，影响MTE2（Memory Transfer Engine，数据搬入单元），建议合理规划数据搬运逻辑，增加命中率。详情介绍请参见下表中的字段说明。

#### Atlas A3 训练系列产品/Atlas A3 推理系列产品和Atlas A2 训练系列产品/Atlas A2 推理系列产品
**图1**
![](figure/zh-cn_image_0000002502746522.png "点击放大")L2Cache.csv文件
 
 
 
 关键字段说明如下。**表1**字段说明
字段名

字段解释

block_id

Task运行切分数量，对应Task运行时配置的核数。

sub_block_id

Task运行使用的每个block名称和序号。

aic_time(us)

该Task被分配到每个AI Cube Core计算单元上后，每个AI Cube Core计算单元上的执行时间，单位us。

aic_total_cycles

该Task被分配到每个AI Cube Core计算单元上后，每个AI Cube Core计算单元上的执行的cycle总数。

aiv_time(us)

该Task被分配到每个AI Vector Core计算单元上后，每个AI Vector Core计算单元上的执行时间，单位us。

aiv_total_cycles

该Task被分配到每个AI Vector Core计算单元上后，每个AI Vector Core计算单元上的执行的cycle总数。

ai*_write_cache_hit

写cache命中的次数。

ai*_write_cache_miss_allocate

写cache缺失后重新分配缓存的次数。

ai*_r*_read_cache_hit

读r*通道cache命中次数。

ai*_r*_read_cache_miss_allocate

读r*通道cache缺失后重新分配的次数。

ai*_write_hit_rate(%)

写cache命中率。

ai*_read_hit_rate(%)

读cache命中率。

ai*_total_hit_rate(%)

读/写cache命中率。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### Atlas 推理系列产品
**图2**
L2Cache.csv文件
 
 
 
 关键字段说明如下。**表2**字段说明
字段名

字段解释

aic_l2_cache_hit_rate(%)

内存访问请求命中L2次数与总次数的比值。
|  |  |
| --- | --- |
|  |  |
**父主题：**[msprof op](atlasopdev_16_0131.html)