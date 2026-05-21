---
title: "msSanitizer工具提示--cache-size异常"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0138.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0138.html"
---

# msSanitizer工具提示--cache-size异常

#### 现象描述

*使用msSanitizer工具进行异常检测时，提示"113023 records undetected, please use --cache-size=xx*to run the operator again" 。

#### 原因分析

算子执行信息的大小超过工具默认分配GM内存的大小，导致部分信息丢失。

#### 解决措施

根据提示修改--cache-size值，并重新拉起算子，进行异常检测。
**父主题：**[FAQ](atlasopdev_16_0133.html)