---
title: "功能介绍"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0173.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0173.html"
---

# 功能介绍

[当前，部分算子开源仓中，采用了msOpGen提供的工程模板。然而，基于此模板进行算子调用较为复杂，且难以实现算子的轻量化调测。为了解决此类问题，我们可以利用msKPP工具提供的mskpp.tiling_func](atlasopdev_16_0185.html#ZH-CN_TOPIC_0000002536920433)[和mskpp.get_kernel_from_binary](atlasopdev_16_0186.html#ZH-CN_TOPIC_0000002504880688)接口，直接调用msOpGen工程中的tiling函数以及用户自定义的Kernel函数。

- 使用本功能时，算子输入输出仅支持numpy.Tensor、torch.Tensor。
- 若CANN中曾经部署过相同类型的算子（op_type），用户修改了tiling函数并重新编译，则需要在CANN环境中重新部署该算子。
- [调用mskpp.tiling_func](atlasopdev_16_0185.html#ZH-CN_TOPIC_0000002536920433)[和mskpp.get_kernel_from_binary](atlasopdev_16_0186.html#ZH-CN_TOPIC_0000002504880688)接口时，系统会在当前目录下的mindstudio_mskpp_gen文件夹中生成以下中间文件，该文件仅供开发定位使用，用户无需关注。请勿修改该文件夹及其子文件的内容，以免造成工具功能异常。
```
(p39) root@ubuntu:~/project/add_custom/CustomOp$ ll mindstudio_mskpp_gen/
total 388
drwxr-x---  2 root root    314 Jul 24 09:40 ./
drwxr-x--- 10 root root   4096 Jul 24 09:40 ../
-rw-------  1 root root  13042 Jul 24 09:40 _mskpp_gen_binary_launch.1.cpp
-rw-------  1 root root  13231 Jul 24 09:40 _mskpp_gen_binary_launch.2.cpp
-rw-------  1 root root  26640 Jul 24 09:40 _mskpp_gen_binary_module.1.so
-rw-------  1 root root  26640 Jul 24 09:40 _mskpp_gen_binary_module.2.so
-rw-------  1 root root   4878 Jul 24 09:40 _mskpp_gen_tiling.1.cpp
-rw-------  1 root root 141432 Jul 24 09:40 _mskpp_gen_tiling.1.so
-rw-------  1 root root   5127 Jul 24 09:40 _mskpp_gen_tiling.2.cpp
-rw-------  1 root root 141432 Jul 24 09:40 _mskpp_gen_tiling.2.so
```

**父主题：**[调用msOpGen算子工程](atlasopdev_16_0172.html)