---
title: "离线解析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0119.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0119.html"
---

# 离线解析

若需要重新解析MindSpore Profiler接口采集的性能数据，可以使用mindspore.profiler.profiler.analyse接口进行离线解析。

[mindspore.profiler.profiler.analyse接口详细介绍请参见mindspore.profiler.profiler.analyse](https://www.mindspore.cn/docs/zh-CN/master/api_python/mindspore/mindspore.profiler.profiler.analyse.html)。

1. *创建{file_name}**.py文件，{file_name}*自定义，并编辑如下代码。

```
1
2
3
```

```
from mindspore.profiler.profiler import analyse

analyse("./profiler_data_path") # './profiler_data_path'为离线解析数据路径

```
|  |  |
| --- | --- |

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

**父主题：**[MindSpore调优工具](atlasprofiling_16_0117.html)