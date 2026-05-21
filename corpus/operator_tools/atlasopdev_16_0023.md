---
title: "算子开发"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0023.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0023.html"
---

# 算子开发

#### 操作步骤

1. [完成算子相关的开发适配，包括算子核函数的开发和tiling实现等，详细内容请参考中工程化算子开发](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_10_0059.html)的章节。
2. [可参考Link](https://gitee.com/ascend/samples/tree/master/operator/ascendc/0_introduction/1_add_frameworklaunch/AddCustom)进行开发，完成op_host/add_custom_tiling.h、op_host/add_custom.cpp和op_kernel/add_custom.cpp的实现。
3. [算子实现完成后，进入算子编译部署](atlasopdev_16_0024.html#ZH-CN_TOPIC_0000002504880720)。
**父主题：**[算子工程创建（msOpGen）](atlasopdev_16_0017.html)