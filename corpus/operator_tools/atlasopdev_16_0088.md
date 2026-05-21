---
title: "算子代码热点图"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0088.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0088.html"
---

# 算子代码热点图

[通过msprof op](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section0449171943115)[或msprof op simulator](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section8684154219309)生成的visualize_data.bin文件可通过MindStudio Insight进行可视化呈现。界面支持查看算子源码与指令集的映射关系、耗时情况等功能，可协助开发者识别热点代码分布，并分析热点函数优化的可行性。

- [若要使用MindStudio Insight进行查看时，需要单独安装MindStudio Insight软件包，具体下载链接请参见“安装与卸载](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0005.html)”。
- 将visualize_data.bin文件导入MindStudio Insight的具体操作请参考导入性能数据。
- [MindStudio Insight具体操作和详细字段解释请参考源码（Source）](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0068.html)。
- 添加-g编译选项会在生成的二进制文件中附带调试信息，建议限制带有调试信息的用户程序的访问权限，确保只有授权人员可以访问该二进制文件。
- 算子程序编译时需要包含-g，否则msprof不会展示热点图，也不调用llvm-symbolizer组件的相关功能实现代码-PC映射。
- msprof op算子代码热点图功能不适用于
 Atlas 推理系列产品
 。
- [MC2算子和LCCL算子均不支持生成算子代码热点图](atlasopdev_16_0088.html#ZH-CN_TOPIC_0000002504880812)。

#### msprof op热点图
**图1**
![](figure/zh-cn_image_0000002502586748.png "点击放大")msprof op源码界面
- 在界面顶部，可切换计算单元和核函数文件。
- 在左侧界面，提供算子核函数各行代码模拟L2Cache命中率、与GM有关的数据搬运量及对应的指令数，帮助开发者快速定位瓶颈代码行。
- 在右侧界面，提供具体的指令维度模拟L2Cache命中率、与GM有关的数据搬运量、执行次数及与代码相关联，帮助开发者进一步分析代码耗时长的原因。
- MindStudio Insight时间线和详情页面中L2Cache命中率的差异请参见表1。**表1**MindStudio Insight L2Cache命中率对比表
页面位置

数据来源

维度

时间线

工具模拟

代码行和指令维度。

详情

真实存在

核维度。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

查看与GM有关的数据搬运量（Process Bytes）时，不涉及GM单元的情况都显示为NA。

- msprof op具体特性支持情况请参见表2。
**表2**msprof op热点图的功能介绍
列名

Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品

Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品

Atlas 推理系列产品

说明

源码

支持

支持

不支持

-

指令PC地址

支持

支持

不支持

-

PIPE

支持

支持

不支持

-

执行指令数

支持

支持

不支持

查看算子源码与指令的执行次数。

GPR Count

不支持

不支持

不支持

查看寄存器使用情况。
说明：
[不支持使用TRACE_START](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendcopapi/atlasascendc_api_07_1212.html)[和TRACE_STOP](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendcopapi/atlasascendc_api_07_1213.html)接口查看部分算子的寄存器使用情况。

L2Cache命中率

支持

支持

不支持

模拟代码行和指令维度。

Process Bytes

支持

支持

不支持

查看与GM有关的数据搬运量。
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

#### msprof op simulator热点图
**图2**
![](figure/zh-cn_image_0000002534426563.png "点击放大")msprof op simulator源码界面
- 在界面顶部，可切换计算单元和核函数文件。
- 在左侧界面，提供算子核函数各行代码对应的耗时、寄存器使用情况、Vector计算类指令在UB Bank上读和写的冲突情况、Vector计算单元利用率、与GM有关的数据搬运量及对应的指令数，帮助开发者快速定位瓶颈代码行。
- 在右侧界面，提供具体的指令耗时、寄存器使用情况、与GM有关的数据搬运量、Vector计算类指令在UB Bank上读和写的冲突情况、Vector计算单元利用率、执行次数及与代码相关联，帮助开发者进一步分析代码耗时长的原因。

- 通用寄存器的最大数量为32，当寄存器的使用数量达到32时，仿真过程需等到使用中的寄存器释放后才能运行。
- [不支持使用TRACE_START](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendcopapi/atlasascendc_api_07_1212.html)[和TRACE_STOP](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendcopapi/atlasascendc_api_07_1213.html)接口查看部分算子的寄存器使用情况。
- 查看与GM有关的数据搬运量（Process Bytes）时，不涉及GM单元的情况都显示为NA。

- msprof op simulator具体特性支持情况请参见表3。
**表3**msprof op simulator热点图的功能介绍
列名

Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品

Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品

Atlas 推理系列产品

说明

源码

支持

支持

支持

-

指令PC地址

支持

支持

支持

-

PIPE

支持

支持

支持

-

耗时cycle

支持

支持

支持

查看算子源码与指令的耗时情况。

执行指令数

支持

支持

支持

查看算子源码与指令的执行次数。

GPR Count

支持

支持

支持

查看寄存器使用情况。
说明：
[不支持使用TRACE_START](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendcopapi/atlasascendc_api_07_1212.html)[和TRACE_STOP](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendcopapi/atlasascendc_api_07_1213.html)接口查看部分算子的寄存器使用情况。

UB Bank读冲突

支持

支持

支持

-

UB Bank写冲突

支持

支持

支持

-

vec计算单元利用率百分比

支持

支持

支持

-

Process Bytes

支持

支持

不支持

查看与GM有关的数据搬运量。
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
**父主题：**[算子调优（msProf）](atlasopdev_16_0081.html)