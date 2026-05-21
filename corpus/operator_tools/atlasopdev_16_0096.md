---
title: "MemoryL0（L0读写带宽速率）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0096.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0096.html"
---

# MemoryL0（L0读写带宽速率）

L0A/L0B/L0C采集内存读写带宽速率数据MemoryL0.csv。详情介绍请参见下表中的字段说明。

单位GB/s表示每秒传输1GB的数据量。

#### Atlas A3 训练系列产品/Atlas A3 推理系列产品和Atlas A2 训练系列产品/Atlas A2 推理系列产品
**图1**
![](figure/zh-cn_image_0000002534426509.png "点击放大")MemoryL0.csv文件
 
 
 
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

aic_l0a_read_bw(GB/s)

代表本算子中l0a读取其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

aic_l0a_write_bw(GB/s)

代表本算子中l0a写入其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

aic_l0b_read_bw(GB/s)

代表本算子中l0b读取其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

aic_l0b_write_bw(GB/s)

代表本算子中l0b写入其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

aic_l0c_read_bw_cube(GB/s)

代表Cube从l0c读取的数据量对应total cycle的带宽速率，单位GB/s。

aic_l0c_write_bw_cube(GB/s)

代表Cube向l0c写入的数据量对应total cycle的带宽速率，单位GB/s。
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

#### Atlas 推理系列产品
**图2**
![](figure/zh-cn_image_0000002534506541.png "点击放大")MemoryL0.csv文件
 
 
 
 关键字段说明如下。**表2**字段说明
字段名

字段解释

aic_time(us)

该Task被分配到每个AI Core计算单元上后，每个AI Core计算单元上的执行时间，单位us。

aic_total_cycles

该Task被分配到每个AI Core计算单元上后，每个AI Core计算单元上的执行的cycle总数。

aic_l0a_read_bw(GB/s)

代表本算子中l0a单元读取其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

aic_l0a_write_bw(GB/s)

代表本算子中l0a单元写入其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

aic_l0b_read_bw(GB/s)

代表本算子中l0b单元读取其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

aic_l0b_write_bw(GB/s)

代表本算子中l0b单元写入其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

aic_l0c_read_bw_cube(GB/s)

代表Cube从l0c读取的数据量对应total cycle的带宽速率，单位GB/s。

aic_l0c_write_bw_cube(GB/s)

代表Cube向l0c写入的数据量对应total cycle的带宽速率，单位GB/s。

aic_l0c_read_bw(GB/s)

代表Vector从l0c读取的数据量对应total cycle的带宽速率，单位GB/s。

aic_l0c_write_bw(GB/s)

代表Vector向l0c写入的数据量对应total cycle的带宽速率，单位GB/s。
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
**父主题：**[msprof op](atlasopdev_16_0131.html)