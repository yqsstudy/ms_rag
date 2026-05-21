---
title: "功能介绍"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0154.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0154.html"
---

# 功能介绍

在进行模板库算子开发时，利用msKPP提供的接口在Python脚本中快速实现Kernel下发代码生成、编译及运行Kernel。

[在对模板库算子进行性能调优时，通常需要对Kernel的模板参数（比如L0shape大小）进行多次调整并对比性能结果。为提升调优效率，msKPP工具提供了autotune](atlasopdev_16_0163.html#ZH-CN_TOPIC_0000002536800469)系列接口支持开发者可以高效地针对多个调优点进行代码替换、编译、运行以及性能对比。

自动调优功能仅支持Atlas A2 训练系列产品/Atlas A2 推理系列产品。

#### 使用约束

- 单Device仅支持使用单个msKPP工具进行自动调优，且不推荐同时运行其他算子程序。
- 需确保先import mskpp再import acl，否则需要在运行前设置环境变量。
```
export LD_PRELOAD=${INSTALL_DIR}/lib64/libmspti.so
```

**父主题：**[自动调优](atlasopdev_16_0153.html)