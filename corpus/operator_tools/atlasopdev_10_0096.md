---
title: "简介"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_10_0096.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_10_0096.html"
---

# 简介

#### 功能描述
CANN开发套件包中提供了ST测试工具：msOpST，支持生成算子的ST测试用例并在硬件环境中执行。具有如下功能：
- 根据算子信息库定义文件（*.ini）生成算子测试用例定义文件（*.json），作为算子ST测试用例的输入。
- 根据算子测试用例定义文件生成ST测试数据及测试用例执行代码，在硬件环境上执行算子测试用例。
- 自动生成运行报表（st_report.json）功能，报表记录了测试用例信息及各阶段运行情况。
- 根据用户定义并配置的算子期望数据生成函数，回显期望算子输出和实际算子输出的对比测试结果。

#### 使用前提

- 使用此工具生成算子测试用例前，需要将要测试的算子部署到算子库中。
- [PyTorch框架的安装请参见《Ascend Extension for PyTorch 软件安装指南](https://www.hiascend.com/document/detail/zh/Pytorch/730/configandinstg/instg/docs/zh/installation_guide/installation_description.md)》。

#### 补充说明

msOpST工具其他参数说明可参考表1。
**表1**参数说明
参数名称

参数描述

说明

get_shape

获取shape。

机机接口，用户无需关注。

change_shape

修改shape。

gen

生成acl_op.json。

gen_testcase

生成测试文件及数据。

compare

结果比对。

compare_by_path

指定路径文件结果比对。

-h，

--help

帮助提示参数。

可选参数。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
**父主题：**[基于msOpST工具进行算子ST测试](atlasopdev_10_0095.html)