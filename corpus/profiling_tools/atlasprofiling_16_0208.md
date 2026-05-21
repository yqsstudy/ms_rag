---
title: "MindSpore场景特有数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0208.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0208.html"
---

# MindSpore场景特有数据

#### ascend_mindspore_profiler_{Rank_ID}.db

[文件主要汇总所有性能数据的.db格式文件。字段说明以msprof导出db格式数据说明](atlasprofiling_16_0142.html#ZH-CN_TOPIC_0000002504358416)为参考，实际结果略有不同，请以实际情况为准。

#### communication_analyzer.db

[文件主要统一通信类的分段耗时、拷贝、带宽等信息，以便进行通信类数据分析。通信类数据只有在多卡、多节点或集群场景下存在。字段说明以analysis.db数据](atlasprofiling_16_0207.html#ZH-CN_TOPIC_0000002536038403)为参考，实际结果略有不同，请以实际情况为准。

#### communication.json

[文件记录通信类算子的通信耗时、带宽等详细信息。字段说明以解析结果](atlasprofiling_16_0019.html#ZH-CN_TOPIC_0000002536038289__zh-cn_topic_0000002534398409_section023216238448)为参考，实际结果略有不同，请以实际情况为准。

#### communication_matrix.json

[文件记录通信小算子基本信息，包含通信size、通信带宽、通信Rank等信息。字段说明以解析结果](atlasprofiling_16_0019.html#ZH-CN_TOPIC_0000002536038289__zh-cn_topic_0000002534398409_section023216238448)为参考，实际结果略有不同，请以实际情况为准。

#### dataset.csv

[文件记录dataset算子的信息。字段说明请参见dataset.csv](https://www.mindspore.cn/tutorials/zh-CN/master/debug/profiler.html#dataset-csv)。

#### minddata_pipeline_raw_{Rank_ID}.csv

[记录dataset数据集操作的性能指标。字段说明请参见minddata_pipeline_raw_{Rank_ID}.csv](https://www.mindspore.cn/tutorials/zh-CN/master/debug/profiler.html#minddata-pipeline-raw-{rank-id}-csv)。

#### minddata_pipeline_summary_{Rank_ID}.csv

[记录更详细的dataset数据集操作性能指标，并根据性能指标给出优化建议。字段说明请参见minddata_pipeline_summary_{Rank_ID}.csv](https://www.mindspore.cn/tutorials/zh-CN/master/debug/profiler.html#minddata-pipeline-summary-{rank-id}-csv)。

#### minddata_pipeline_summary_{Rank_ID}.json

[与minddata_pipeline_summary_{Rank_ID}.json文件内容相同，字段说明请参见minddata_pipeline_summary_{Rank_ID}.csv](https://www.mindspore.cn/tutorials/zh-CN/master/debug/profiler.html#minddata-pipeline-summary-{rank-id}-csv)。

**父主题：**[MindSpore&PyTorch框架性能数据文件参考](atlasprofiling_16_0203.html)