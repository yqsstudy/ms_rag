---
title: "compare精度比对"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0011.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0011.html"
---

# compare精度比对

#### 前提条件

- [完成环境准备](atlasquick_train_0002.html#ZH-CN_TOPIC_0000002502572164__section68892049173411)。
- [以MindSpore框架内，不同版本下的cell模块比对场景为例，参见精度数据采集](atlasquick_train_0008.html)，完成不同框架版本的cell模块dump，其中不同框架版本以MindSpore 2.6.0和MindSpore 2.7.0为例。

#### 执行比对

1. 数据准备。
在同一昇腾NPU环境安装MindSpore 2.6.0和MindSpore 2.7.0版本，分别执行dump操作，获得两份精度数据。注意区分dump_path指定的目录名称，以dump_data_2.6.0和dump_data_2.7.0为例。

2. 创建比对配置文件。以在训练脚本所在目录创建compare.json配置文件为例，文件内容拷贝如下示例配置。
```
1
2
3
4
5
6
```

```
{
"npu_path": "./dump_data_2.7.0/step0/rank/dump.json",
"bench_path": "./dump_data_2.6.0/step0/rank/dump.json",
"stack_path": "./dump_data_2.7.0/step0/rank/stack.json",
"is_print_compare_log": true
}

```
|  |  |
| --- | --- |

其中"npu_path"和"bench_path"对应的路径需要在同一环境下。

3. 执行比对。命令如下：****
```
msprobe -f mindspore compare -i ./compare.json -o ./compare_result/accuracy_compare -s
```
出现如下打印说明比对成功：
```
1
2
3
4
5
6
7
```

```
...
Compare result is /xxx/compare_result/accuracy_compare/compare_result_{timestamp}.xlsx
...
The advisor summary is saved in: /xxx/compare_result/accuracy_compare/advisor_{timestamp}.txt
************************************************************************************
*                        msprobe compare ends successfully.                        *
************************************************************************************

```
|  |  |
| --- | --- |

4. 比对结果文件分析。
compare会在./compare_result/accuracy_compare生成如下文件。

  - advisor_{timestamp}.txt：文件中给出了可能存在精度问题的API的专家建议。
  - compare_result_{timestamp}.xlsx：文件列出了所有执行精度比对的API详细信息和比对结果，可通过颜色标记、比对结果（Result）、计算精度达标情况（Accuracy Reached or Not）、错误信息提示（Err_Message）定位可疑算子，但鉴于每种指标都有对应的判定标准，还需要结合实际情况进行判断。**示例如下：图1**
**compare_result_1
图2**
compare_result_2

[更多比对结果分析请参见“精度比对结果分析](https://gitcode.com/Ascend/mstt/blob/br_release_MindStudio_8.3.0_20261231/debug/accuracy_tools/msprobe/docs/10.accuracy_compare_PyTorch.md#3-精度比对结果分析)”。

**父主题：**[精度比对](atlasquick_train_0010.html)