---
title: "AICPU自定义算子日志解析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0058.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0058.html"
---

# AICPU自定义算子日志解析

#### 概述

dump数据文件解析功能通过解析dump数据文件，获取dump数据文件中的信息。

当前该功能支持从dump数据文件中解析AICPU自定义算子的日志，并将其保存到日志文件内。

#### 命令格式说明

```
python3 dump_parser.py save_log -d <dump_file> [-out <output>]
```

命令行参数说明如表1所示。

该功能通过dump_parser.py脚本实现，脚本存放在${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
**表1**命令行参数说明
**参数名**

**参数说明**

**是否必选**

-d

--dump_file

待解析的dump数据文件。

是

-out

*--output*

AICPU自定义算子的日志存放目录。默认为当前目录。

结果文件名格式为：dump_file_name.{index}.log

不建议配置与当前用户不一致的其它用户目录，避免提权风险。

否
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 操作步骤

1. 登录CANN工具安装环境。
2. 进入${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
3. **执行save_log**解析命令。
****
```
python3 dump_parser.py save_log -d my_dump_path/dump_file -out /MyApp20/out
```

**命令执行完成后在-out**指定目录下生成日志文件。

**父主题：**[扩展功能](atlasaccuracy_16_0051.html)