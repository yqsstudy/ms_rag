---
title: "使用前准备"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0007.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0007.html"
---

# 使用前准备

- [请参考环境准备](atlasopdev_16_0003.html#ZH-CN_TOPIC_0000002536800441)[，完成相关环境变量的配置。然后，可直接使用msKPP工具的性能建模](atlasopdev_16_0151.html#ZH-CN_TOPIC_0000002536800447)功能。
  - 在任意目录下基于msKPP接口进行算子建模，实现中包括如下注意事项：
    - 进行算子建模前，需要导入Tensor、Chip以及算子实现所必要的指令（统一以小写命名）。
    - [以with语句开启算子实现代码的入口，“enable_trace”和“enable_metrics”两个接口可使能trace打点图和指令统计功能，具体请参见极限性能分析](atlasopdev_16_0011.html#ZH-CN_TOPIC_0000002536800451)章节的main.py。
    - [算子建模详细指令接口说明请参考对外接口使用说明](atlasopdev_16_0015.html#ZH-CN_TOPIC_0000002536800455)。

  - 如果需要指令占比饼图（instruction_cycle_consumption.html），则需要安装生成饼图所依赖的Python三方库plotly。
```
pip3 install plotly
```

- [若要使用自动调优](atlasopdev_16_0153.html#ZH-CN_TOPIC_0000002505040506)[功能，需要下载Link](https://gitcode.com/cann/catlass)中的Ascend C模板库。
- 二次开发请保证输入数据可信安全。
**父主题：**[算子设计（msKPP）](atlasopdev_16_0005.html)