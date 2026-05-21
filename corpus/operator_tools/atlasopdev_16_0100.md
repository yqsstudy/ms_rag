---
title: "ResourceConflictRatio（资源冲突占比）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0100.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0100.html"
---

# ResourceConflictRatio（资源冲突占比）

UB上的bank group、bank conflict和资源冲突在所有指令中的占比数据ResourceConflictRatio.csv，建议减少对于同一个bank的读写冲突或bank group的读读冲突。

bank group是指UB中的一组bank，每个bank group包含多个bank。bank conflict是指在UB中同时访问相同bank的多个线程之间的竞争。

详情介绍请参见下表中的字段说明。

#### Atlas A3 训练系列产品/Atlas A3 推理系列产品及Atlas A2 训练系列产品/Atlas A2 推理系列产品
**图1**
![](figure/zh-cn_image_0000002502586712.png "点击放大")ResourceConflictRatio.csv文件
 
 
 
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

aic_cube_wait_ratio

代表Cube单元被阻塞的cycle数在所有指令执行cycle数中占比。

aiv_vec_total_cflt_ratio

代表所有Vector执行的指令被阻塞的cycle数在所有指令执行cycle数中占比。

aiv_vec_bankgroup_cflt_ratio

代表Vector执行的指令被bankgroup冲突阻塞的cycle数在所有指令执行cycle数中占比。由于Vector指令的block stride的值设置不合理，造成bankgroup冲突。

aiv_vec_bank_cflt_ratio

代表Vector执行的指令被bank冲突阻塞的cycle数在所有指令执行cycle数中占比。由于Vector指令操作数的读写指针地址不合理，造成bank冲突。

aiv_vec_resc_cflt_ratio

代表Vector执行的指令被执行单元资源冲突阻塞的cycle数在所有指令执行cycle数中占比。当算子中涉及多个计算单元，应该尽量保证多个单元并发调度。当某个计算单元正在运行，但算子逻辑仍然往该单元下发指令，就会造成整体的算力没有得到充分应用。

aiv_vec_mte_cflt_ratio

代表Vector执行的指令被MTE冲突阻塞的cycle数在所有指令执行cycle数中占比。

aiv_vec_wait_ratio

代表Vector单元被阻塞的cycle数在所有指令执行cycle数中占比。

ai*_mte1_wait_ratio

代表MTE1被阻塞的cycle数在所有指令执行cycle数中占比。

ai*_mte2_wait_ratio

代表MTE2被阻塞的cycle数在所有指令执行cycle数中占比。

ai*_mte3_wait_ratio

代表MTE3被阻塞的cycle数在所有指令执行cycle数中占比。
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

#### Atlas 推理系列产品
**图2**
![](figure/zh-cn_image_0000002534426527.png "点击放大")ResourceConflictRatio.csv文件
 
 
 
 关键字段说明如下。**表2**字段说明
字段名

字段解释

aic_time(us)

该Task被分配到每个AI Core计算单元上后，每个AI Core计算单元上的执行时间，单位us。

aic_total_cycles

该Task被分配到每个AI Core计算单元上后，每个AI Core计算单元上的执行的cycle总数。

aic_cube_wait_ratio

代表Cube单元被阻塞的cycle数在所有指令执行cycle数中占比。

aic_vec_total_cflt_ratio

代表所有Vector执行的指令被阻塞的cycle数在所有指令执行cycle数中占比。

aic_vec_bankgroup_cflt_ratio

代表Vector执行的指令被bankgroup冲突阻塞的cycle数在所有指令执行cycle数中占比。由于Vector指令的block stride的值设置不合理，造成bankgroup冲突。

aic_vec_bank_cflt_ratio

代表Vector执行的指令被bank冲突阻塞的cycle数在所有指令执行cycle数中占比。由于Vector指令操作数的读写指针地址不合理，造成bank冲突。

aic_vec_resc_cflt_ratio

代表Vector执行的指令被执行单元资源冲突阻塞的cycle数在所有指令执行cycle数中占比。当算子中涉及多个计算单元，应该尽量保证多个单元并发调度。当某个计算单元正在运行，但算子逻辑仍然往该单元下发指令，就会造成整体的算力没有得到充分应用。

aic_vec_mte_cflt_ratio

代表Vector执行的指令被MTE冲突阻塞的cycle数在所有指令执行cycle数中占比。

aic_vec_wait_ratio

代表Vector单元被阻塞的cycle数在所有指令执行cycle数中占比。

aic_mte1_wait_ratio

代表MTE1被阻塞的cycle数在所有指令执行cycle数中占比。

aic_mte2_wait_ratio

代表MTE2被阻塞的cycle数在所有指令执行cycle数中占比。

aic_mte3_wait_ratio

代表MTE3被阻塞的cycle数在所有指令执行cycle数中占比。
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
**父主题：**[msprof op](atlasopdev_16_0131.html)