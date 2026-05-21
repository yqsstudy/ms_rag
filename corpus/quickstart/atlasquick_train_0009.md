---
title: "精度预检"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0009.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0009.html"
---

# 精度预检

#### 前提条件

- [完成环境准备](atlasquick_train_0002.html#ZH-CN_TOPIC_0000002502572164__section68892049173411)。
- [完成精度数据采集](atlasquick_train_0008.html)，得到MindSpore训练场景昇腾NPU环境的精度数据。

#### 执行预检
直接在昇腾NPU环境下执行预检。****
```
msprobe -f mindspore run_ut -api_info ./dump_data/step0/rank/dump.json -o ./checker_result
```

**此时-o**参数指定的路径下会生成两个csv文件，分别为accuracy_checking_details_{timestamp}.csv和accuracy_checking_result_{timestamp}.csv。
**accuracy_checking_result_{timestamp}.csv标明每个API是否通过测试。对于其中没有通过测试的或者特定感兴趣的API，根据其API Name字段在accuracy_checking_details_{timestamp}.csv中查询其各个输出的达标情况以及比较指标。图1**
**accuracy_checking_result
图2**
accuracy_checking_details
[预检结果详细介绍请参见“预检结果](https://gitcode.com/Ascend/mstt/blob/br_release_MindStudio_8.3.0_20261231/debug/accuracy_tools/msprobe/docs/09.accuracy_checker_MindSpore.md#4-预检结果)”。
**父主题：**[模型精度调试](atlasquick_train_0004.html)