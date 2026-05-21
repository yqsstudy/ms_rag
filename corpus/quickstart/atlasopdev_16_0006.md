---
title: "算子异常检测（msSanitizer）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasopdev_16_0006.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasopdev_16_0006.html"
---

# 算子异常检测（msSanitizer）

msSanitizer工具作用于算子开发的整个周期，帮助开发者确保算子的质量和稳定性。通过在早期阶段发现并修复异常，msSanitizer大大减少了产品上线后的潜在风险和后期维护成本。

- *启动工具后，将会在当前目录下自动生成工具运行日志文件mssanitizer_{TIMESTAMP}**_{PID****}.log，当用户程序运行完成后，界面将会打印异常报告。***
- ${git_clone_path}为sample仓的路径。

1. 在${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch目录下执行以下命令，生成自定义算子工程，进行host侧和kernel侧的算子实现。
****
```
bash install.sh -v Ascendxxxyy    # xxxyy为用户实际使用的具体芯片类型
```

2. 在${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/CustomOp目录下执行以下命令，重新编译部署算子。
********
```
bash build.sh
./build_out/custom_opp_<target_os>_<target_architecture>.run   // 当前目录下run包的名称
```

3. 切换到${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation目录，拉起算子API运行脚本，进行内存检测。

  1. 启用内存检测：
    - 可显式指定内存检测，默认会开启非法读写、多核踩踏、非对齐访问和非法释放的检测功能：
```
mssanitizer --tool=memcheck bash run.sh
```

    - 执行如下命令，可手动启用内存泄漏的检测功能：
```
mssanitizer --tool=memcheck --leak-check=yes bash run.sh
```

  2. [定位内存异常，具体请参见《算子开发工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0002.html)[》的“异常检测（msSanitizer）> 内存检测](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0042.html)”章节。

4. 进行竞争检测。

  1. 执行如下命令，启用竞争检测。
```
mssanitizer --tool=racecheck bash run.sh
```

  2. [定位内存竞争，具体请参见《算子开发工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0002.html)[》的“异常检测（msSanitizer）> 竞争检测](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0043.html)”章节。
*当前目录下会自动生成工具运行日志文件mssanitizer_{TIMESTAMP}**_{PID*}.log，当用户程序运行完成后，界面将会打印异常报告。

5. 进行未初始化检测。

  1. 执行如下命令，可手动启用未初始化的检测。
```
mssanitizer --tool=initcheck bash run.sh 
```

  2. [定位内存异常，具体请参见《算子开发工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0002.html)[》的“异常检测（msSanitizer）> 未初始化检测](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0128.html)”章节。

**父主题：**[算子开发工具快速入门](tools_qucikstart_0006.html)