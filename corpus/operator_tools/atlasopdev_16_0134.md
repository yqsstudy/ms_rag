---
title: "msSanitizer工具异常报告中未打印正确的文件名和行号"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0134.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0134.html"
---

# msSanitizer工具异常报告中未打印正确的文件名和行号

#### 现象描述

文件名和行号显示为"<unknown>:0"，或文件名显示正确，但行号显示为"0"。

#### 解决措施

- 文件名和行号显示为"<unknown>:0"说明msSanitizer工具没有解析到正确的文件名和行号，根据用户的检测场景有以下两种解决方法：
  - [如果启用了"--check-cann-heap=yes"选项，对CANN软件栈内存进行检测，则可以通过引入Sanitizer API头文件并重新编译用户程序使检测工具获取到正确的文件名和行号，具体可参考通过msSanitizer检测工具中提供的新接口...](atlasopdev_16_0047.html#ZH-CN_TOPIC_0000002505040574__zh-cn_topic_0000002502746432_zh-cn_topic_0000001748761501_li1423525185711)。
  - [如果正在对算子进行异常检测，那么可能是在算子编译阶段未启用"-g"编译选项，启用"-g"编译选项后才能生成正确的文件名和行号，具体可参考内核调用符场景准备](atlasopdev_16_0040.html#ZH-CN_TOPIC_0000002536800523__zh-cn_topic_0000002534506457_li159191517103114)。

- 文件名显示正确，但行号显示为"0"
这种情况一般是因为使用了"-O2"或"-O3"编译选项进行算子代码编译，编译器对算子代码进行优化时导致代码行变化，可通过在算子编译阶段使用"-O0"禁用编译器优化来解决这个问题。

**父主题：**[FAQ](atlasopdev_16_0133.html)