---
title: "PipeUtilization（计算单元和搬运单元耗时占比）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0099.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0099.html"
---

# PipeUtilization（计算单元和搬运单元耗时占比）

采集计算单元和搬运单元耗时和占比数据PipeUtilization.csv。建议优化数据搬运逻辑，提高带宽利用率。详情介绍请参见下表中的字段说明。

- 单位GB/s表示每秒传输1GB的数据量。

- 表中的字段说明里每一个ratio的total cycle表示的是 cube核 或者 vector核上的cycle数，其中ai* 分为aic 和 aiv ，aic 指的是cube，aiv 指的是vector。

#### Atlas A3 训练系列产品/Atlas A3 推理系列产品和Atlas A2 训练系列产品/Atlas A2 推理系列产品
**图1**
![](figure/zh-cn_image_0000002534426537.png "点击放大")PipeUtilization.csv文件
 
 
 
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

aiv_vec_time(us)

代表vec类型指令（向量类运算指令）耗时。

aiv_vec_ratio

代表vec类型指令（向量类运算指令）的cycle数在total cycle数中的占用比。

aic_cube_time(us)

代表Cube类型指令（fp16及s16矩阵类运算指令）耗时。

aic_cube_ratio

代表Cube类型指令（fp16及s16矩阵类运算指令）的cycle数在total cycle数中的占用比。

ai*_scalar_time(us)

代表scalar类型指令（标量类运算指令）耗时。

ai*_scalar_ratio

代表scalar类型指令（标量类运算指令）的cycle数在total cycle数中的占用比。

aic_fixpipe_time(us)

代表fixpipe类型指令（L0C->GM/L1搬运类指令）耗时。

aic_fixpipe_ratio

代表fixpipe类型指令（L0C->GM/L1搬运类指令）的cycle数在total cycle数中的占用比。

aic_mte1_time(us)

代表MTE1类型指令（L1->L0A/L0B搬运类指令）耗时，不包括搬运等待时间。

aic_mte1_ratio

代表MTE1类型指令（L1->L0A/L0B搬运类指令）的cycle数在total cycle数中的占用比。

ai*_mte2_time(us)

代表MTE2类型指令（GM->AICORE搬运类指令）耗时。

ai*_mte2_ratio

代表MTE2类型指令（GM->AICORE搬运类指令）的cycle数在total cycle数中的占用比。

ai*_mte3_time(us)

代表MTE3类型指令（AICORE->GM搬运类指令）耗时。

ai*_mte3_ratio

代表MTE3类型指令（AICORE->GM搬运类指令）的cycle数在total cycle数中的占用比。

ai*_icache_miss_rate

代表ICache缺失率，即未命中instruction的L1 cache，数值越小越好。

aic_mte3_active_bw(GB/s)

代表MTE3类型指令（AICORE->DDR CUBE搬运类指令）数据量对应active cycle的活跃带宽。

aiv_mte3_active_bw(GB/s)

代表MTE3类型指令（AICORE->DDR AIV搬运类指令）数据量对应active cycle的活跃带宽。

aic_fixpipe_active_bw(GB/s)

代表fixpipe类型指令（L0C->OUT/L1搬运类指令）数据量对应active cycle的活跃带宽。

aiv_mte2_active_bw(GB/s)

代表MTE2类型指令（DDR->AICORE AIV搬运类指令）数据量对应active cycle的活跃带宽。

aic_mte1_active_bw(GB/s)

代表Cube单元MTE1类型指令数据量对应active cycle的活跃带宽，具体涉及L1->L0A、L1->L0B这2个部分的通路数据。
说明：
Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 和
 Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品
 仅开启动态插桩（设置--aic-metrics=MemoryDetail时）会显示。

aic_mte2_active_bw(GB/s)

代表Cube单元MTE2类型指令数据量对应active cycle的活跃带宽，具体涉及GM->L1、GM->L0A、GM->L0B这3条通路的数据。
说明：
Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 和
 Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品
 仅开启动态插桩（设置--aic-metrics=MemoryDetail时）会显示。

ai*_scalar_single_time(us)

代表scalar类型指令（标量类运算指令）的单发（一拍发射一条指令）指令时间。

ai*_scalar_dual_time(us)

代表scalar类型指令（标量类运算指令）的双发（一拍发射两条指令）指令时间。

ai*_scalar_wait_time(us)

代表scalar类型指令（标量类运算指令）的核内wait指令阻塞的时间。

ai*_scalar_wait_id*_time(us)

代表scalar类型指令（标量类运算指令）的核间wait指令ID阻塞的时间。
说明：
“id*”为占位符，实际可对应ID0到ID15的任意核编号。

核间同步指标ai*_scalar_wait_id0_time到ai*_scalar_wait_id15_time仅在有数据的时候进行展示。

aic_scalar_mte1_stall_time(us)

代表scalar类型指令（标量类运算指令）因MTE1 IQ队列已满所造成的阻塞时间。

ai*_scalar_mte2_stall_time(us)

代表scalar类型指令（标量类运算指令）因MTE2 IQ队列已满所造成的阻塞时间。

ai*_scalar_mte3_stall_time(us)

代表scalar类型指令（标量类运算指令）因MTE3 IQ队列已满所造成的阻塞时间。

aic_scalar_cube_stall_time(us)

代表scalar类型指令（标量类运算指令）因CUBE IQ队列已满所造成的阻塞时间。

aic_scalar_vector_stall_time(us)

代表scalar类型指令（标量类运算指令）因VECTOR IQ队列已满所造成的阻塞时间。

ai*_scalar_wait_ib_time(us)

代表scalar类型指令（标量类运算指令）的IB等待Icache时间。

aic_scalar_stall_by_ub_time(us)

代表scalar类型指令（标量类运算指令）被UB阻塞的时间。
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
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### Atlas 推理系列产品
**图2**
![](figure/zh-cn_image_0000002502586722.png "点击放大")PipeUtilization.csv文件
 
 
 
 关键字段说明如下。**表2**字段说明
字段名

字段解释

aic_time(us)

该Task被分配到每个AI Core计算单元上后，每个AI Core计算单元上的执行时间，单位us。

aic_total_cycles

该Task被分配到每个AI Core计算单元上后，每个AI Core计算单元上的执行的cycle总数。

aic_cube_time(us)

代表Cube类型指令（fp16及s16矩阵类运算指令）耗时。

aic_cube_ratio

代表Cube类型指令（fp16及s16矩阵类运算指令）的cycle数在total cycle数中的占用比。

aic_scalar_time(us)

代表scalar类型指令（标量类运算指令）耗时。

aic_scalar_ratio

代表scalar类型指令（标量类运算指令）的cycle数在total cycle数中的占用比。

aic_mte1_time(us)

代表MTE1类型指令（L1->L0A/L0B搬运类指令）耗时，不包括搬运等待时间。

aic_mte1_ratio

代表MTE1类型指令（L1->L0A/L0B搬运类指令）的cycle数在total cycle数中的占用比。

aic_mte2_time(us)

代表MTE2类型指令（GM->AICORE搬运类指令）耗时。

aic_mte2_ratio

代表MTE2类型指令（GM->AICORE搬运类指令）的cycle数在total cycle数中的占用比。

aic_mte3_time(us)

代表MTE3类型指令（AICORE->GM搬运类指令）耗时。

aic_mte3_ratio

代表MTE3类型指令（AICORE->GM搬运类指令）的cycle数在total cycle数中的占用比。

aic_icache_miss_rate

代表ICache缺失率，即未命中instruction的L1 cache，数值越小越好。

aic_vec_time(us)

代表Vec类型指令（向量类运算指令）耗时。

aic_vec_ratio

代表Vec类型指令（向量类运算指令）的cycle数在total cycle数中的占用比。
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
**父主题：**[msprof op](atlasopdev_16_0131.html)