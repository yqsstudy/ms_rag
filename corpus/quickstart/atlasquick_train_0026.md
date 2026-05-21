---
title: "精度预检"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0026.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0026.html"
---

# 精度预检

#### 前提条件

- [完成环境准备](atlasquick_train_0002.html#ZH-CN_TOPIC_0000002502572164__section68892049173411)。
- [完成精度数据采集](atlasquick_train_0025.html)，得到PyTorch训练场景昇腾NPU环境的精度数据。

#### 执行预检

1. 数据准备。
将昇腾NPU环境下dump的精度数据拷贝至GPU环境。（用于保证预检执行的精度数据一致）

2. 启动预检。**分别在GPU和昇腾NPU环境下使用run_ut**命令执行预检操作。（预检场景GPU环境需要使用昇腾NPU环境拷贝的精度数据）****
```
msprobe -f pytorch run_ut -api_info ./dump_data/step0/rank/dump.json -o ./checker_result
```

出现如下日志表示预检完成。

```
Successfully completed run_ut/multi_run_ut
```

**此时-o**参数指定的路径下会生成两个csv文件，分别为accuracy_checking_details_{timestamp}.csv和accuracy_checking_result_{timestamp}.csv。

这两个文件是预检的中间结果，需要完成下一步，才能得到预检的最终结果。

3. 预检结果比对。
将NPU和GPU的预检结果进行比对，查看NPU数据中是否存在精度问题的API。
可以将GPU上的accuracy_checking_details_{timestamp}.csv文件传到昇腾NPU环境，执行如下命令。******
```
msprobe -f pytorch api_precision_compare -npu ./npu/accuracy_checking_details_{timestamp}.csv -gpu ./gpu/accuracy_checking_details_{timestamp}.csv -o ./compare_result/accuracy_checking
```

4. 预检结果分析。
api_precision_compare会在./compare_result/accuracy_checking目录下生成两个csv文件。

  - **api_precision_compare_result_{timestamp}.csv文件会详细标明API在各种比对算法下的达标情况，示例如下。图1**
api_precision_compare_result_{timestamp}
  - **api_precision_compare_details_{timestamp}.csv文件会标明每个API是否通过测试，示例如下。图2**
**api_precision_compare_details_1
图3**
api_precision_compare_details_2
[更多比对结果字段含义请参见“预检结果比对](https://gitcode.com/Ascend/mstt/blob/br_release_MindStudio_8.3.0_20261231/debug/accuracy_tools/msprobe/docs/07.accuracy_checker_PyTorch.md#5-预检结果比对)”。

**父主题：**[模型精度调试](atlasquick_train_0021.html)