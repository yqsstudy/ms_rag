---
title: "ArithmeticUtilization（Cube及Vector类型指令耗时和占比）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0093.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0093.html"
---

# ArithmeticUtilization（Cube及Vector类型指令耗时和占比）

Cube及Vector类型指令的cycle占比数据ArithmeticUtilization.csv，建议优化算子逻辑，减少冗余计算指令。详情介绍请参见下表中的字段说明。

#### Atlas A3 训练系列产品/Atlas A3 推理系列产品及Atlas A2 训练系列产品/Atlas A2 推理系列产品
**图1**
![](figure/zh-cn_image_0000002502746538.png "点击放大")ArithmeticUtilization.csv文件
 
 
 
 关键字段说明如下。**表1**字段说明
字段名

字段解释

block_id

Task运行切分数量，对应Task运行时配置的核数。

sub_block_id

Block上Vector\Cube核的ID。

aic_time(us)

该Task被分配到每个AI Cube Core计算单元上后，每个AI Cube Core计算单元上的执行时间，单位us。

aic_total_cycles

该Task被分配到每个AI Cube Core计算单元上后，每个AI Cube Core计算单元上的执行的cycle总数。

aiv_time(us)

该Task被分配到每个AI Vector Core计算单元上后，每个AI Vector Core计算单元上的执行时间，单位us。

aiv_total_cycles

该Task被分配到每个AI Vector Core计算单元上后，每个AI Vector Core计算单元上的执行的cycle总数。

aic_cube_ratio

代表Cube单元指令的cycle数在total cycle数中的占用比。

aic_cube_fp16_ratio

代表Cube fp16类型指令的cycle数在total cycle数中的占用比。

aic_cube_int8_ratio

代表Cube int8类型指令的cycle数在total cycle数中的占用比。

aic_cube_fops

代表Cube类型的浮点运算数，即计算量，可用于衡量算法/模型的复杂度，其中fops表示floating point operations。

aic_cube_total_instr_number

代表Cube指令的总条数，包括fp和int类型。

aic_cube_fp_instr_number

代表Cube fp类型指令的总条数。

aic_cube_int_instr_number

代表Cube int类型指令的总条数。

aiv_vec_ratio

代表Vec单元指令的cycle数在total cycle数中的占用比。

aiv_vec_fp32_ratio

代表Vec fp32类型指令的cycle数在total cycle数中的占用比。

aiv_vec_fp16_ratio

代表Vec fp16类型指令的cycle数在total cycle数中的占用比。

aiv_vec_int32_ratio

代表Vec int32类型指令的cycle数在total cycle数中的占用比。

aiv_vec_int16_ratio

代表Vec int16类型指令的cycle数在total cycle数中的占用比。

aiv_vec_misc_ratio

代表Vec misc类型指令的cycle数在total cycle数中的占用比。

aiv_vec_fops

代表Vector类型浮点运算数，即计算量，可用于衡量算法/模型的复杂度，其中fops表示floating point operations。
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

#### Atlas 推理系列产品
**图2**
![](figure/zh-cn_image_0000002502586724.png "点击放大")ArithmeticUtilization.csv文件
 
 
 
 关键字段说明如下。**表2**字段说明
字段名

字段解释

aic_time(us)

该Task被分配到每个AI Core计算单元上后，每个AI Core计算单元上的执行时间，单位us。

aic_total_cycles

该Task被分配到每个AI Core计算单元上后，每个AI Core计算单元上的执行的cycle总数。

aic_cube_ratio

代表Cube单元指令的cycle数在total cycle数中的占用比。

aic_cube_fp16_ratio

代表Cube fp16类型指令的cycle数在total cycle数中的占用比。

aic_cube_int8_ratio

代表Cube int8类型指令的cycle数在total cycle数中的占用比。

aic_cube_fops

代表Cube类型的浮点运算数，即计算量，可用于衡量算法/模型的复杂度，其中fops表示floating point operations。

aic_cube_total_instr_number

代表Cube指令的总条数，包括fp和int类型。

aic_vec_ratio

代表Vec单元指令的cycle数在total cycle数中的占用比。

aic_vec_fp32_ratio

代表Vec fp32类型指令的cycle数在total cycle数中的占用比。

aic_vec_fp16_ratio

代表Vec fp16类型指令的cycle数在total cycle数中的占用比。

aic_vec_int32_ratio

代表Vec int32类型指令的cycle数在total cycle数中的占用比。

aic_vec_int16_ratio

代表Vec int16类型指令的cycle数在total cycle数中的占用比。

aic_vec_misc_ratio

代表Vec misc类型指令的cycle数在total cycle数中的占用比。

aic_vec_fops

代表Vector类型浮点运算数，即计算量，可用于衡量算法/模型的复杂度，其中fops表示floating point operations。
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