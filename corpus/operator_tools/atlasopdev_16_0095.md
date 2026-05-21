---
title: "Memory（内存读写带宽速率）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0095.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0095.html"
---

# Memory（内存读写带宽速率）

UB/L1/L2/主存储器采集内存读写带宽速率数据Memory.csv。详情介绍请参见下表中的字段说明。

单位GB/s表示每秒传输1GB的数据量。

#### Atlas A3 训练系列产品/Atlas A3 推理系列产品及Atlas A2 训练系列产品/Atlas A2 推理系列产品
**图1**
![](figure/zh-cn_image_0000002534426555.png "点击放大")Memory.csv文件
 
 
 
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

aiv_ub_to_gm_bw(GB/s)

代表ub向gm写入的数据量对应total cycle的带宽速率，单位GB/s。

aiv_gm_to_ub_bw(GB/s)

代表gm向ub写入的数据量对应total cycle的带宽速率，单位GB/s。

aic_l1_read_bw(GB/s)

代表本算子中l1单元读取其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

aic_l1_write_bw(GB/s)

代表本算子中l1单元写入其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

ai*_main_mem_read_bw(GB/s)

代表主存储器读取其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

ai*_main_mem_write_bw(GB/s)

代表主存储器写入其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

aic_mte1_instructions

代表MTE1类型指令条数。

aic_mte1_ratio

代表MTE1类型指令的cycle数在total cycle数中的占用比。

ai*_mte2_instructions

代表MTE2类型指令条数。

ai*_mte2_ratio

代表MTE2类型指令的cycle数在total cycle数中的占用比。

ai*_mte3_instructions

代表MTE3类型指令条数。

ai*_mte3_ratio

代表MTE3类型指令的cycle数在total cycle数中的占用比。

read_main_memory_datas(KB)

读主存储器数据总量。

write_main_memory_datas(KB)

写主存储器数据总量。

GM_to_L1_datas(KB)

GM到L1的数据搬运量。

L1_to_GM_datas(KB)(estimate)

L1到GM的数据搬运量，估算值。

L0C_to_L1_datas(KB)

L0C到L1的数据搬运量。

L0C_to_GM_datas(KB)

L0C到GM的数据搬运量。

GM_to_UB_datas(KB)

GM到UB的数据搬运量。

UB_to_GM_datas(KB)

UB到GM的数据搬运量。

GM_to_L1_bw_usage_rate(%)

GM到L1通路带宽使用率。

L1_to_GM_bw_usage_rate(%)(estimate)

L1到GM通路带宽使用率，估算值。

L0C_to_L1_bw_usage_rate(%)

L0C到L1通路带宽使用率。

L0C_to_GM_bw_usage_rate(%)

L0C到GM通路带宽使用率。

GM_to_UB_bw_usage_rate(%)

GM到UB通路带宽使用率。

UB_to_GM_bw_usage_rate(%)

UB到GM通路带宽使用率。
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
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### Atlas 推理系列产品
**图2**
![](figure/zh-cn_image_0000002534506591.png "点击放大")Memory.csv文件
 
 
 
 关键字段说明如下。**表2**字段说明
字段名

字段解释

aic_time(us)

该Task被分配到每个AI Core计算单元上后，每个AI Core计算单元上的执行时间，单位us。

aic_total_cycles

该Task被分配到每个AI Core计算单元上后，每个AI Core计算单元上的执行的cycle总数。

aic_ub_to_gm_bw(GB/s)

代表ub向gm写入的数据量对应total cycle的带宽速率，单位GB/s。

aic_gm_to_ub_bw(GB/s)

代表gm向ub写入的数据量对应total cycle的带宽速率，单位GB/s。

aic_l1_read_bw(GB/s)

代表本算子中l1单元读取其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

aic_l1_write_bw(GB/s)

代表本算子中l1单元写入其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

aic_main_mem_read_bw(GB/s)

代表主存储器读取其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

aic_main_mem_write_bw(GB/s)

代表主存储器写入其他所有单元数据时，对应的total cycle的带宽速率，单位GB/s。

aic_mte1_instructions

代表MTE1类型指令条数。

aic_mte1_ratio

代表MTE1类型指令的cycle数在total cycle数中的占用比。

aic_mte2_instructions

代表MTE2类型指令条数。

aic_mte2_ratio

代表MTE2类型指令的cycle数在total cycle数中的占用比。

aic_mte3_instructions

代表MTE3类型指令条数。

aic_mte3_ratio

代表MTE3类型指令的cycle数在total cycle数中的占用比。
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
|  |  |
**父主题：**[msprof op](atlasopdev_16_0131.html)