---
title: "msSanitizer工具使用"--cce-enable-sanitizer -g"编译算子时出现"InputSection too large"错误"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0135.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0135.html"
---

# msSanitizer工具使用"--cce-enable-sanitizer -g"编译算子时出现"InputSection too large"错误

#### 现象描述

报错ld.lld: error: InputSection too large for range extension thunk。

#### 原因分析

算子链接时输入代码段过大，超过编译器支持的指令跳转范围。

#### 解决措施

[通过增加编译选项，启用编译器扩大跳转范围的特性来解决。在算子代码编译](atlasopdev_16_0040.html#ZH-CN_TOPIC_0000002536800523__zh-cn_topic_0000002534506457_li108561313124319)选项"--cce-enable-sanitizer -g"后增加"-Xaicore-start -mcmodel=large -mllvm -cce-aicore-relax -Xaicore-end"。

```
1
2
3
4
5
6
7
```

```
target_compile_options(${smoke_testcase}_npu PRIVATE
                     -O2
                     -std=c++17
                     --cce-enable-sanitizer
                     -g 
                     -Xaicore-start -mcmodel=large -mllvm -cce-aicore-relax -Xaicore-end
)

```
|  |  |
| --- | --- |
**父主题：**[FAQ](atlasopdev_16_0133.html)