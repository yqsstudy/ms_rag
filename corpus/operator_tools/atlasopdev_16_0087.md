---
title: "指令流水图"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0087.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0087.html"
---

# 指令流水图

[通过msprof op simulator](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section8684154219309)生成的visualize_data.bin文件或trace.json文件，并进行可视化呈现。指令流水图以指令维度展示时序关系，并关联调用栈快速定位瓶颈位置。支持以下两种可视化呈现方式：

- 添加-g编译选项会在生成的二进制文件中附带调试信息，建议限制带有调试信息的用户程序的访问权限，确保只有授权人员可以访问该二进制文件。
- 若不使用llvm-symbolizer组件提供的相关功能，输入msProf的程序编译时不包含-g即可，msProf工具则不会调用llvm-symbolizer组件的相关功能。
- [若用户仅需关注部分算子性能时，可在
 Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 、
 Atlas 推理系列产品
 和
 Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品
 的单核内调用TRACE_START](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendcopapi/atlasascendc_api_07_1212.html)[和TRACE_STOP](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendcopapi/atlasascendc_api_07_1213.html)[接口。并在编译配置文件中添加-DASCENDC_TRACE_ON，具体操作请参见添加-DASCENDC_TRACE_ON的方法](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_li0770510267)[。然后，才能生成该范围内的流水图信息，具体流水图显示内容可参考指令流水图](atlasopdev_16_0087.html#ZH-CN_TOPIC_0000002504880808)。
- 用户需在编译配置文件中添加-DASCENDC_TRACE_ON，具体修改方法可参考以下样例工程。[AddKernelInvocationNeo算子工程](https://gitee.com/ascend/samples/tree/master/operator/ascendc/0_introduction/3_add_kernellaunch/AddKernelInvocationNeo/cmake)，需在${git_clone_path}/samples/operator/ascendc/0_introduction/3_add_kernellaunch/AddKernelInvocationNeo/cmake/npu_lib.cmake文件中新增以下代码。************************
```
ascendc_compile_definitions
(
    ...
    -DASCENDC_TRACE_ON
)
```

- Chrome浏览器
[在Chrome浏览器中输入“chrome://tracing”地址，并将通过msprof op simulator](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section8684154219309)生成指令流水图文件（trace.json）拖到空白处打开，键盘上输入快捷键（W：放大，S：缩小，A：左移，D：右移）可进行查看。关键字段说明如表1。
**表1**关键字段说明
字段名

字段含义

VECTOR

向量运算单元。

SCALAR

标量运算单元。

Cube

矩阵乘运算单元。

MTE1

数据搬运流水，数据搬运方向为：L1 ->{L0A/L0B, UBUF}。

MTE2

数据搬运流水，数据搬运方向为：{DDR/GM, L2} ->{L1, L0A/B, UBUF}。

MTE3

数据搬运流水，数据搬运方向为：UBUF -> {DDR/GM, L2, L1}、L1->{DDR/L2}。

FIXP

数据搬运流水，数据搬运方向为：FIXPIPE L0C -> OUT/L1。（仅
 Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品
 支持展示）

FLOWCTRL

控制流指令。

CACHEMISS

未命中ICache。

USEMASK

自定义打点范围。
说明：
若同一个USEMASK内存在范围嵌套或只有TRACE_START无TRACE_STOP时，不能正常绘制指令流水图。

ALL

表示在这个通道的指令在所有通道都执行。
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

- [MindStudio Insight
 
 通过msprof op simulator](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section8684154219309)生成的trace.json文件或visualize_data.bin文件可导入MindStudio Insight进行可视化呈现。
  - [若要使用MindStudio Insight进行查看时，需要单独安装MindStudio Insight软件包，具体下载链接请参见“安装与卸载](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0005.html)”。
  - 将visualize_data.bin文件导入MindStudio Insight的具体操作请参考导入性能数据。
  - [MindStudio Insight具体操作和详细字段解释请参考《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)[》的“系统调优 > 时间线（Timeline）](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0034.html)”章节。
  - 添加-g编译选项会在生成的二进制文件中附带调试信息，建议限制带有调试信息的用户程序的访问权限，确保只有授权人员可以访问该二进制文件。

#### 指令流水图介绍（以MindStudio Insight为例）

MindStudio Insight工具以时序图方式为用户提供指令在昇腾AI处理器上的运行情况，用户可通过分析时序图中的指令详情、指令执行时间、指令关联代码的调用栈及指令/流水间同步连线等信息，识别微观指令的时序优化点。
**图1**
![](figure/zh-cn_image_0000002502746524.png "点击放大")时间线界面
- 展示各PIPE中各指令的运行时长以及不同PIPE间的指令依赖关系，帮助用户分析流水排布间可能存在的性能优化点。
- 支持将流水指令信息与代码关联，指导用户如何基于代码去优化流水排布。
- 支持在选中详情展示与GM有关指令的数据搬运量。

通过观察Timeline的流水排布等信息判断算子运行过程中可能存在的性能问题，如指令间未能有效并行等。
**父主题：**[算子调优（msProf）](atlasopdev_16_0081.html)