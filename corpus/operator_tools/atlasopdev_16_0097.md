---
title: "MemoryUB（UB读写带宽速率）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0097.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0097.html"
---

# MemoryUB（UB读写带宽速率）

mte/vector/scalar采集ub读写带宽速率数据MemoryUB.csv。详情介绍请参见下表中的字段说明。

单位GB/s表示每秒传输1GB的数据量。

#### Atlas A3 训练系列产品/Atlas A3 推理系列产品及Atlas A2 训练系列产品/Atlas A2 推理系列产品
**图1**
![](figure/zh-cn_image_0000002534506555.png "点击放大")MemoryUB.csv文件
 
 
 
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

aiv_ub_read_bw_vector(GB/s)

代表Vector从UB读取的数据量对应total cycle的带宽速率，单位GB/s。

aiv_ub_write_bw_vector(GB/s)

代表Vector向UB写入的数据量对应total cycle的带宽速率，单位GB/s。

aiv_ub_read_bw_scalar(GB/s)

代表Scalar从UB读取的数据量对应total cycle的带宽速率，单位GB/s。

aiv_ub_write_bw_scalar(GB/s)

代表Scalar向UB写入的数据量对应total cycle的带宽速率，单位GB/s。
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

#### Atlas 推理系列产品
**图2**
![](figure/zh-cn_image_0000002534506559.png "点击放大")MemoryUB.csv文件
 
 
 
 关键字段说明如下。**表2**字段说明
字段名

字段解释

aic_time(us)

该Task被分配到每个AI Core计算单元上后，每个AI Core计算单元上的执行时间，单位us。

aic_total_cycles

该Task被分配到每个AI Core计算单元上后，每个AI Core计算单元上的执行的cycle总数。

aic_ub_read_bw_vector(GB/s)

代表Vector从UB读取的数据量对应total cycle的带宽速率，单位GB/s。

aic_ub_write_bw_vector(GB/s)

代表Vector向UB写入的数据量对应total cycle的带宽速率，单位GB/s。

aic_ub_read_bw_scalar(GB/s)

代表Scalar从UB读取的数据量对应total cycle的带宽速率，单位GB/s。

aic_ub_write_bw_scalar(GB/s)

代表Scalar向UB写入的数据量对应total cycle的带宽速率，单位GB/s。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
**父主题：**[msprof op](atlasopdev_16_0131.html)