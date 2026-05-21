---
title: "离线解析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0122.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0122.html"
---

# 离线解析

当使用Ascend PyTorch Profiler接口采集的性能数据较大时，若在当前环境直接使用on_trace_ready接口进行自动解析，则可能导致资源占用过大出现卡顿，那么可以取消on_trace_ready接口，并通过环境变量ASCEND_WORK_PATH设置落盘目录（例如：export ASCEND_WORK_PATH=xx/xx），在采集完成性能数据后，使用如下方式进行离线解析：

1. *创建{file_name}**.py文件，{file_name}*自定义，并编辑如下代码。

```
1
2
3
4
```

```
from torch_npu.profiler.profiler import analyse

if __name__ == "__main__":
    analyse(profiler_path="./result_data", max_process_number=max_process_number, export_type=export_type)

```
|  |  |
| --- | --- |
**表1**参数说明
参数

描述

**可选/必选**

profiler_path

PyTorch性能数据路径。路径格式仅支持由字母、数字、下划线和连字符组成的字符串，不支持软链接。指定的目录下保存PyTorch性能数据目录{worker_name}_{时间戳}_ascend_pt。

必选

max_process_number

离线解析最大进程数。取值范围为1~CPU核数，默认为CPU核数的一半。若设置超过该环境的CPU核数，则自动取CPU核数；若设置为非法值，则取默认值CPU核数的一半。

可选

export_type

设置导出的性能数据结果文件格式，List类型。取值：

  - text：表示解析为.json和.csv格式的timeline和summary文件以及汇总所有性能数据的.db格式文件（ascend_pytorch_profiler_{Rank_ID}.db、analysis.db）。
  - [db：表示仅解析为汇总所有性能数据的.db格式文件（ascend_pytorch_profiler_{Rank_ID}.db、analysis.db），使用MindStudio Insight工具展示。仅支持on_trace_ready接口导出和离线解析](atlasprofiling_16_0122.html#ZH-CN_TOPIC_0000002504358406)导出，需配套安装支持导出db格式的CANN Toolkit开发套件包和ops算子包。

设置无效值或未配置时，则读取profiler_info.json中的export_type字段，确定导出格式。

[解析结果数据请参见MindSpore&PyTorch框架性能数据文件参考](atlasprofiling_16_0203.html#ZH-CN_TOPIC_0000002536038401)。

可选
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

  - 离线解析接口支持多性能数据目录并行解析，当性能数据量较大且数据目录较多的情况下，可能因环境内存不足导致解析失败，此时可以通过自定义最大进程数（max_process_number）来控制资源的占用。
  - 解析过程日志存放在{worker_name}_{时间戳}_ascend_pt/logs目录下。

2. 保存文件后执行如下命令解析性能数据：
**
```
python3 {file_name}.py
```

3. 查看性能数据结果文件和性能数据分析。

[性能数据结果文件详细介绍请参见MindSpore&PyTorch框架性能数据文件参考](atlasprofiling_16_0203.html#ZH-CN_TOPIC_0000002536038401)。

[请参见《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》将解析后的性能数据文件进行可视化展示和分析。

[可以使用性能分析工具（msprof-analyze）](https://gitcode.com/Ascend/mstt/tree/master/profiler/msprof_analyze)辅助分析性能数据。

**父主题：**[Ascend PyTorch调优工具](atlasprofiling_16_0120.html)