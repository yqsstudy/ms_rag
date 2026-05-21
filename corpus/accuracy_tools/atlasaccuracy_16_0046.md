---
title: "npy与npy文件之间的精度比对"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0046.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0046.html"
---

# npy与npy文件之间的精度比对

#### 概述

精度比对工具支持单个npy与npy文件之间的精度比对。基本要求如下：

- [对于dump数据文件需要先完成执行dump数据文件Format转换](atlasaccuracy_16_0054.html#ZH-CN_TOPIC_0000002536023787__zh-cn_topic_0000002534483563_zh-cn_topic_0244646216_section19803552124011)。
- 需要确保两个比对文件内的Shape一致。
- 仅支持CosineSimilarity（余弦相似度）、MaxAbsoluteError（最大绝对误差）、AccumulatedRelativeError（累积相对误差）、RelativeEuclideanDistance（欧氏相对距离）、MeanAbsoluteError（平均绝对误差）、RootMeanSquareError（均方根误差）、MaxRelativeError（最大相对误差）、MeanRelativeError（平均相对误差）比对算法。

#### 命令格式说明
******
```
python3 msaccucmp.py file_compare -m my_dump_path -g golden_dump_path -out output
```

命令行参数说明如表1所示。

该功能通过msaccucmp.py脚本实现，脚本存放在${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
**表1**命令行参数说明
**参数名**

**参数说明**

**是否必选**

-m

--my_dump_path

待比对的npy文件。

是

-g

--golden_dump_path

待比对的npy标杆数据文件。

是

-out

--output

比对数据结果存放目录。

结果文件名格式为：file_result_{timestamp}.txt

不建议配置与当前用户不一致的其它用户目录，避免提权风险。

是
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

#### 操作步骤

1. 登录CANN工具安装环境。
2. 进入${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
3. **执行file_compare**比对命令。
******
```
python3 msaccucmp.py file_compare -m my_dump_path/a.npy -g golden_dump_path/b.npy -out output
```

命令执行完成后输出比对结果。如图1所示。
**图1**
比对结果
[比对结果可根据计算精度评价指标](atlasaccuracy_16_0045.html#ZH-CN_TOPIC_0000002504343840)判断是否符合精度要求。

**父主题：**[比对结果分析](atlasaccuracy_16_0037.html)