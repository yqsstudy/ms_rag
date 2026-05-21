---
title: "计算精度评价指标"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0045.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0045.html"
---

# 计算精度评价指标

精度比对是以GPU的计算结果为标杆，以不同算法维度，比对算子精度差异，根据每个算法维度的结果判断算子在运行时是否存在精度问题。

[以下仅为推荐的精度评价指标，实际算子需要满足的精度请用户自行判断，判断方式请参见完整比对结果参数说明](atlasaccuracy_16_0064.html#ZH-CN_TOPIC_0000002504184012)。

计算精度评价指标：

1. CosineSimilarity：通过计算两个向量的余弦值来判断其相似度，数值越接近于1，说明计算出的两个张量越相似，实际可接受阈值为大于0.99。在计算中可能会存在nan，主要由于可能会出现其中一个向量为0。
2. RelativeEuclideanDistance：欧氏相对距离越接近于0，表明越相近，实际可接受阈值为小于0.05。
3. KullbackLeiblerDivergence：KL散度越小，真实分布与近似分布之间的匹配越好，实际可接受阈值为小于0.005。
4. MeanAbsoluteError和RootMeanSquareError：平均绝对误差和均方根误差相关联，MeanAbsoluteError越大，RootMeanSquareError等于或近似MeanAbsoluteError，说明整体偏差越集中，实际可接受阈值为等于1。
**父主题：**[比对结果分析](atlasaccuracy_16_0037.html)