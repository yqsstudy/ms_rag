---
title: "执行解析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0034.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0034.html"
---

# 执行解析

- 数据采集时会锁定落盘文件，需要等待采集结束之后才能启动解析，否则将提示报错“db is lock”。
- 数据解析没有结束前，不可再次开启动态采集，否则可能出现降低采集性能等问题。

#### 基础解析

执行解析命令示例：

```
python3 -m ms_service_profiler.parse --input-path ${PATH}/prof_dir/
```
**表1**参数说明
**参数**

说明

**是否必选**

--input-path

指定性能数据所在路径，会遍历读取该路径下所有名为msproftx.db、ascend_service_profiler_*.db和ms_service_*.db的数据库。

是

--output-path

指定解析后文件生成路径，默认为当前路径下的output目录。

否

--log-level

设置日志级别，取值为：

- debug：调试级别。该级别的日志记录了调试信息，便于开发人员或维护人员定位问题。
- info：正常级别。记录工具正常运行的信息。默认值。
- warning：警告级别。记录工具和预期的状态不一致，但不影响整个进程运行的信息。
- error：一般错误级别。
- fatal：严重错误级别。
- critical：致命错误级别。

否

--format

设置性能数据输出文件的导出格式，取值为：

- csv：表示只导出csv格式的结果文件。一般用于原始落盘数据量过大（通常为>10G）场景，仅导出该格式文件可减少数据解析耗时，该格式文件包含每轮请求调度耗时、模型执行耗时、KVCache显存占用情况等。
- json：表示只导出json格式的结果文件。一般用于仅需使用trace数据进行分析的场景，仅导出该格式文件可减少数据解析耗时，该格式文件包含服务化框架推理全过程timeline图。
- db：表示只导出db格式的结果文件。一般用于仅通过MindStudio Insight工具分析结果数据场景，该格式文件包含全量数据解析结果，可直接在MindStudio Insight中完全展示。

不使用format则默认全部导出，可以配置一个或多个参数，配置示例：--format db，--format db csv。
说明：
若数据采集时，配置acl_task_time参数值为2，则解析结果文件仅支持导出json和db格式。

否
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

[进行基础解析的同时，可对性能数据按照不同维度（request维度、batch维度、总体服务维度）进行多维度解析](https://gitcode.com/Ascend/msit/blob/master/msserviceprofiler/docs/msserviceprofiler_multi_analyze_instruct.md)[，也可对不同batch数据进行细粒度性能拆解](https://gitcode.com/Ascend/msit/blob/master/msserviceprofiler/docs/service_performance_split_tool_instruct.md)。
**父主题：**[数据解析](atlasprofiling_16_0032.html)