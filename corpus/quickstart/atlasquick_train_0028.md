---
title: "compare精度比对"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0028.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0028.html"
---

# compare精度比对

#### 前提条件

- [完成环境准备](atlasquick_train_0002.html#ZH-CN_TOPIC_0000002502572164__section68892049173411)。
- [完成精度数据采集](atlasquick_train_0025.html)，得到GPU和昇腾NPU环境的精度数据。

#### 执行比对

1. 数据准备。
完成前提条件中GPU和昇腾NPU环境的数据dump后，将GPU环境下dump的精度数据拷贝至昇腾NPU环境。注意区分dump_path指定的目录名称，以dump_data_npu和dump_data_gpu为例。

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
"npu_path": "./dump_data_npu/step0/rank/dump.json",
"bench_path": "./dump_data_gpu/step0/rank/dump.json",
"stack_path": "./dump_data_npu/step0/rank/stack.json",
"is_print_compare_log": true
}

```
|  |  |
| --- | --- |

其中"npu_path"和"bench_path"对应的路径需要在同一环境下。

3. 执行比对。命令如下：****
```
msprobe -f pytorch compare -i ./compare.json -o ./compare_result/accuracy_compare -s
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

**父主题：**[精度比对](atlasquick_train_0027.html)