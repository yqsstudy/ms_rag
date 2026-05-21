---
title: "比对结果分析指导"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0038.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0038.html"
---

# 比对结果分析指导

- 显示“*”，表示在NPU侧新增独有的算子；无对应的标准算子，无法进行比对，结果显示为“NaN”。
- 余弦相似度和KL散度比对结果为NaN，其他算法有比对数据，则表明该算子的待比对或标杆数据为0；KL散度比对结果为Inf，则表明该算子的标杆数据中有一个为0。

1. [针对常见精度问题，通过输出“Advisor”专家建议](atlasaccuracy_16_0039.html#ZH-CN_TOPIC_0000002536143813)，快速定位问题算子。
2. [针对专家建议无法覆盖的复杂场景，通过查看整网比对结果中不同的算法指标，根据计算精度评价指标](atlasaccuracy_16_0045.html#ZH-CN_TOPIC_0000002504343840)，定位存在精度问题的算子。
3. [在多次比对或存在模糊问题定界场景中，可以通过配置-r或-s参数，实现任意选定范围内的算子精度比对，尤其针对偏大型网络，可以实现快速定位精度问题，-r或-s参数详细介绍请参见命令格式说明](atlasaccuracy_16_0063.html#ZH-CN_TOPIC_0000002536143825)。
4. [针对存疑的比对结果可以先进行npy与npy文件之间的精度比对](atlasaccuracy_16_0046.html#ZH-CN_TOPIC_0000002536023783)进行精度问题排查。
5. [针对精度差异较大算子，可通过单算子比对](atlasaccuracy_16_0047.html#ZH-CN_TOPIC_0000002536143817)功能进一步分析对应张量的详细精度差异。
6. 针对问题算子，根据具体场景，通过算子本身的修改、算子替换、算子融合等方式进行详细优化。
**父主题：**[比对结果分析](atlasaccuracy_16_0037.html)