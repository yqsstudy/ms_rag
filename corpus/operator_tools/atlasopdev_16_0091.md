---
title: "通过指令流水图优化算子"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0091.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0091.html"
---

# 通过指令流水图优化算子

展示如何通过msProf工具的指令流水图特性，分析算子的瓶颈点，并实现Vector算子的性能优化。

#### 操作步骤

1. [参考msprof op simulator](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section8684154219309)[节点，将算子仿真性能数据采集得到的visualize_data.bin文件导入MindStudio Insight，具体导入操作请参考《MindStudio Insight用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/70RC2/msinsightug/msascendinsightug/AscendInsight_0002.html)》的“导入性能数据”章节。
2. 查看算子指令流水图。

可以发现MTE2流水在VADD计算时，没有执行搬运指令，且MTE2流水为该算子的性能瓶颈，需提高MTE2的搬运效率以实现算子性能优化。

![](figure/zh-cn_image_0000002502746534.png "点击放大")

3. 对于MTE2搬运效率的提升有多种方式，此处以开启Ascend C算子的double buffer机制为例。

例如样例算子核函数中，可通过将TPipe中InitBuffer的第二个参数（BUFFER_NUM）值从1修改为2，开启double buffer，InitBuffer的使用可参考InitBuffer。****
```
constexpr int32_t BUFFER_NUM = 2;        // tensor num for each queue
...
pipe.InitBuffer(inQueueY, BUFFER_NUM, 1024 * sizeof(half));
...
```

4. 重新执行步骤1，查看优化后的指令流水图。

在VADD指令计算时，MTE2上的搬运指令也同步执行，实现了更高效的数据搬运。

![](figure/zh-cn_image_0000002534506573.png "点击放大")

**父主题：**[典型案例](atlasopdev_16_0089.html)