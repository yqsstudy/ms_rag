---
title: "解析性能数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0308.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0308.html"
---

# 解析性能数据

在解析性能数据前，需采集相应的原始性能数据。

1. **以CANN-Toolkit开发套件包和ops算子包的运行用户登录开发环境**。
2. 切换至msprof.py脚本所在目录。

${INSTALL_DIR}/tools/profiler/profiler_tool/analysis/msprof，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。若安装的Ascend-cann-toolkit软件包，以root安装举例，则安装后文件存储路径为：/usr/local/Ascend/ascend-toolkit/latest。

3. 解析性能数据。

命令行格式如下：
**********
```
python3 msprof.py import -dir <dir>
```

*例如：python3 msprof.py import -dir /home/HwHiAiUser/profiler_data**/PROF_XXX*
**表1**解析命令参数说明
参数名

**描述**

**可选/必选**

import

通过import方式解析性能数据。

使用import方式解析性能数据时，即使原始性能数据目录中已经生成.db文件，该方式会重新生成.db文件。

必选

--cluster

解析集群场景的性能数据并进行汇总。仅配置import参数时支持。

**-dir**参数需指定PROF_XXX目录的父目录，指定后的解析结果在PROF_XXX目录同级目录下生成sqlite目录。

集群场景时必选

-dir或--collection-dir

*收集到的性能数据目录。须指定为PROF_**XXX目录或PROF_*XXX目录的父目录，例如：

*/home/HwHiAiUser/profiler_data**/PROF_XXX*。

必选

-h或--help

显示帮助信息，仅在获取使用方式时使用。

可选
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

*执行完上述命令，解析完成后对应的PROF_XXX的device_{**id**}*和host目录下会生成sqlite目录，sqlite目录下会有db文件生成（该db文件为中间结果，无须关注，若需要继续导出最终结果的db文件，可执行4）。

4. （可选）二次解析db数据。

该功能是对sqlite目录下的db文件进行二次解析，生成汇总所有性能数据的.db格式文件（msprof_时间戳.db）。
**********
```
python3 msprof.py export db -dir <dir> 
```

  - **执行export db**命令时，会在PROF_XXX目录下生成汇总所有性能数据的.db格式文件（msprof_时间戳.db），可以使用MindStudio Insight工具展示。
  - msprof命令行执行采集操作时，会自动调用此接口生成汇总所有性能数据的.db格式文件（msprof_时间戳.db），正常情况下用户无须手动执行本步骤。

**父主题：**[使用msprof.py脚本解析与导出性能数据](atlasprofiling_16_0306.html)