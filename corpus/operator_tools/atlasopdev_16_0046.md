---
title: "检测API调用的单算子"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0046.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0046.html"
---

# 检测API调用的单算子

完成自定义算子的开发部署后，通过单算子API执行的方式调用，添加检测相关编译选项重新编译算子并部署，使用msSanitizer工具运行可执行文件实现算子进行异常检测。

#### 前提条件
[单击Link](https://gitee.com/ascend/samples/tree/master/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation)获取样例工程，为进行算子检测做准备。
- 此样例工程不支持Atlas A3 训练系列产品。
- 下载代码样例时，需执行以下命令指定分支版本。
```
git clone https://gitee.com/ascend/samples.git -b master
```

#### 操作步骤

1. 执行以下命令，生成自定义算子工程，并进行Host侧和Kernel侧的算子实现。
****
```
bash install.sh -v Ascendxxxyy    # xxxyy为用户实际使用的具体芯片类型
```

2. [请参考算子编译部署](atlasopdev_16_0024.html#ZH-CN_TOPIC_0000002504880720)，完成算子的编译部署。

在样例工程的${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/CustomOp目录下，修改在op_kernel/CMakeLists.txt文件，在Kernel侧实现中增加检测选项-sanitizer，以支持检测功能

```
add_ops_compile_options(ALL OPTIONS -sanitizer)
```

3. 单击前提条件，获取验证代码的样例工程目录。

```
 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
```

```
├──input                                                 // 存放脚本生成的输入数据目录
├──output                                                // 存放算子运行输出数据和真值数据的目录
├── inc                           // 头文件目录 
│   ├── common.h                 // 声明公共方法类，用于读取二进制文件 
│   ├── operator_desc.h          // 算子描述声明文件，包含算子输入/输出，算子类型以及输入描述与输出描述 
│   ├── op_runner.h              // 算子运行相关信息声明文件，包含算子输入/输出个数，输入/输出大小等 
├── src 
│   ├── CMakeLists.txt    // 编译规则文件
│   ├── common.cpp         // 公共函数，读取二进制文件函数的实现文件
│   ├── main.cpp    // 单算子调用应用的入口
│   ├── operator_desc.cpp     // 构造算子的输入与输出描述 
│   ├── op_runner.cpp   // 单算子调用主体流程实现文件
├── scripts
│   ├── verify_result.py    // 真值对比文件
│   ├── gen_data.py    // 输入数据和真值数据生成脚本文件
│   ├── acl.json    // acl配置文件

```
|  |  |
| --- | --- |

4. 使用检测工具拉起算子API运行脚本。

```
mssanitizer --tool=memcheck bash run.sh  # 内存检测需指定 --tool=memcheck
mssanitizer --tool=racecheck bash run.sh # 竞争检测需指定 --tool=racecheck
```

5. [参考内存异常报告解析](atlasopdev_16_0042.html#ZH-CN_TOPIC_0000002536920491__zh-cn_topic_0000002502746384_zh-cn_topic_0000001820455825_section164048925315)[、竞争异常报告解析](atlasopdev_16_0043.html#ZH-CN_TOPIC_0000002504880738__zh-cn_topic_0000002534426381_zh-cn_topic_0000001773496140_section1028444063620)[及未初始化异常报告解析](atlasopdev_16_0128.html#ZH-CN_TOPIC_0000002505040566__zh-cn_topic_0000002534506443_zh-cn_topic_0000001820455825_section164048925315)分析异常行为。
**父主题：**[典型案例](atlasopdev_16_0044.html)