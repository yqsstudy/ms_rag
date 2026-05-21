---
title: "解析结果"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0035.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0035.html"
---

# 解析结果

生成的结果保存在--output-path指定的路径下。
**表1**采集domain域与解析结果对照表
解析结果

采集domain域

profiler.db

"BatchSchedule; ModelExecute; Request; KVCache"

chrome_tracing.json

无强制限制。若要查看请求间flow event，需采集"Request"。

batch.csv

"BatchSchedule; ModelExecute"

kvcache.csv

"KVCache"

request.csv

"Request"

forward.csv

"BatchSchedule; ModelExecute"

pd_split_communication.csv

"Communication"

pd_split_kvcache.csv

"KVCache"

coordinator.csv

"Coordinator"

{host_name}_eplb_{i}_summed_hot_map_by_expert.png

"eplb_observe"

{host_name}_eplb_{i}_summed_hot_map_by_rank.png

"eplb_observe"

{host_name}_eplb_{i}_summed_hot_map_by_model_expert.png

"eplb_observe"
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

[上表中未列出acl_prof_task_time_level、aclDataTypeConfig和aclprofAicoreMetrics参数采集数据的解析结果，这三个参数的详细结果介绍请参见采集数据说明](atlasprofiling_16_0130.html#ZH-CN_TOPIC_0000002504358410)[和op_summary（算子详细信息）](atlasprofiling_16_0151.html#ZH-CN_TOPIC_0000002536038367)，但具体采集结果请以实际情况为准。其中op_statistic_*.csv和op_summary_*.csv文件会在--output-path参数指定目录下的PROF_XXX目录落盘；而其他由这三个参数采集的性能数据文件仍保存在prof_dir参数指定路径的PROF_XXX/mindstudio_profiler_output目录下。

包括如下文件：

#### profiler.db

用于生成可视化折线图的SQLite数据库文件。

其中含有下述数据库表，具体作用如下：
**表2**profiler.db
Table名称

含义

batch

用于在MindStudio Insight展示batch表格数据。

decode_gen_speed

用于生成decode阶段，服务化数据不同时刻吞吐的token平均时延折线图。

first_token_latency

用于生成服务化框架首token时延折线图。

kvcache

用于生成服务化kvcache显存使用情况折线图可视化。

prefill_gen_speed

用于生成prefill阶段，服务化数据不同时刻吞吐的token平均时延折线图。

req_latency

用于生成服务化框架请求端到端时延使用折线图。

request_status

用于生成服务化采集数据不同时刻请求状态折线图。

request

用于在MindStudio Insight展示请求表格数据。

batch_exec

用于反映batch和模型执行关系对应表。

batch_req

用于反映batch和请求对应关系表。

data_table

用于在MindStudio Insight展示表格数据。

counter

用于在trace图显示counter类数据。

flow

用于在trace图显示flow类数据。

process

用于在trace图显示二级泳道数据。

thread

用于在trace图显示三级泳道数据。

slice

用于在trace图显示色块数据。

pd_split_kvcache

用于在MindStudio Insight展示PD分离场景下D节点拉取kvcache表格数据（只在PD分离场景下涉及）。

pd_split_communication

用于在MindStudio Insight展示PD分离场景下PD节点通信的表格数据（只在PD分离场景下涉及）。

ep_balance

记录DeepSeek专家模型服务化推理时，基于MSPTI采集的GroupedMatmul算子负载不均的分析结果。

moe_analysis

记录DeepSeek专家模型服务化推理时，基于MSPTI采集的MoeDistributeCombine算子和MoeDistributeDispatch算子快慢卡分析结果。

data_link

用于在trace图显示forward的时候支持单击rid显示请求输入长度信息。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

此文件主要用于可视化阶段连接Grafana展示图像，不对各表项细节做具体解释说明。

#### chrome_tracing.json

[记录推理服务化请求trace数据，可使用不同可视化工具进行查看，详细介绍请参见数据可视化](atlasprofiling_16_0036.html#ZH-CN_TOPIC_0000002536158331)。

#### batch.csv

记录服务化推理batch为粒度的详细数据。
**表3**batch.csv
字段

说明

name

用于区分组batch和执行batch。

name为batchFrameworkProcessing表示组batch；name为modelExec表示执行batch。

res_list

batch组合情况。

start_time(ms)

组batch或执行batch的开始时间，单位ms。

end_time(ms)

组batch或执行batch的结束时间，单位ms。

batch_size

batch中的请求数量。

batch_type

batch中的请求状态（prefill和decode）。

during_time(ms)

执行时间，单位ms。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### kvcache.csv

记录推理过程的显存使用情况。
**表4**kvcache.csv
字段

说明

domain

标注KVCache事件。

rid

请求ID。

timestamp(ms)

发生显存使用情况变更的时间，单位ms。

name

具体改变显存使用的方法。

device_kvcache_left

显存中剩余blocks数量。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### request.csv

记录服务化推理请求为粒度的详细数据。
**表5**request.csv
字段

说明

http_rid

HTTP请求ID。

start_time(ms)

请求到达的时间，单位ms。

recv_token_size

请求的输入长度。

reply_token_size

请求的输出长度。

execution_time(ms)

请求端到端耗时，单位ms。

queue_wait_time(ms)

请求在整个推理过程中在队列中等待的时间，这里包括waiting状态和pending状态的时间，单位ms。

first_token_latency(ms)

首Token时延，单位ms。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### forward.csv

记录服务化推理模型前向执行过程的详细数据。
**表6**forward.csv
字段

说明

name

标注forward事件，代表模型前向执行过程。

relative_start_time(ms)

每台机器上forward与第一个forward之间的时间。

start_time(ms)

forward的开始时间，单位ms。

end_time(ms)

forward的结束时间，单位ms。

during_time(ms)

forward的执行时间，单位ms。

bubble_time(ms)

forward之间的空泡时间，单位ms。

batch_size

forward处理的请求数量。

batch_type

forward中的请求状态。

forward_iter

不同卡上forward的迭代序号。

dp_rank

标识forward的DP信息，相同DP域该列的值相同。

prof_id

标识不同卡，相同的卡该列的值相同。

hostname

标识不同机器，相同机器该列的值相同。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### pd_split_communication.csv

[PD分离部署场景通信类数据。PD分离部署场景属于多机多卡（集群）场景之一，需要在执行采集](atlasprofiling_16_0031.html#ZH-CN_TOPIC_0000002536038299)时使用共享配置文件。

PD分离部署场景及概念详细介绍请参见《MindIE Motor开发指南》中的“集群服务部署 > PD分离服务部署”章节。
**表7**pd_split_communication.csv
字段

说明

rid

请求ID。

http_req_time(ms)

请求到达时间，单位ms。

send_request_time(ms)

P节点开始向D节点发送请求时间，单位ms。

send_request_succ_time(ms)

请求发送成功时间，单位ms。

prefill_res_time(ms)

prefill执行完成时间，单位ms。

request_end_time(ms)

请求执行完毕的时间，单位ms。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### pd_split_kvcache.csv

[记录PD分离推理过程的KVCache在PD节点间的传输情况。PD分离部署场景属于多机多卡（集群）场景之一，需要在执行采集](atlasprofiling_16_0031.html#ZH-CN_TOPIC_0000002536038299)时使用共享配置文件。

PD分离部署场景及概念详细介绍请参见《MindIE Motor开发指南》中的“集群服务部署 > PD分离服务部署”章节。
**表8**pd_split_kvcache.csv
字段

说明

domain

标注PullKVCache事件。

rank

设备ID。

rid

请求ID。

block_tables

block_tables信息。

seq_len

请求长度。

during_time(ms)

KVCache从P节点传输到D节点的执行时间，单位ms。

start_datetime(ms)

KVCache从P节点传输到D节点的开始时间，显示为具体日期，单位ms。

end_datetime(ms)

KVCache从P节点传输到D节点的结束时间，显示为具体日期，单位ms。

start_time(ms)

KVCache从P节点传输到D节点的开始时间，显示为时间戳，单位ms。

end_time(ms)

KVCache从P节点传输到D节点的结束时间，显示为时间戳，单位ms。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### coordinator.csv

[记录PD分离推理过程的请求分发到各个节点数量变化情况。PD分离部署场景属于多机多卡（集群）场景之一，需要在执行采集](atlasprofiling_16_0031.html#ZH-CN_TOPIC_0000002536038299)时使用共享配置文件。

PD分离部署场景及概念详细介绍请参见《MindIE Motor开发指南》中的“集群服务部署 > PD分离服务部署”章节。
**表9**coordinator.csv
字段

说明

time

请求数量变化的时刻。

address

分发给节点的地址。格式为：IP地址:端口号。

node_type

节点的类型。prefill或decode。

add_count

当前节点增加的请求数量。

end_count

当前节点结束的请求数量。

running_count

当前节点正在运行的请求数量。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### ep_balance.csv

记录DeepSeek专家模型服务化推理时，基于MSPTI采集的GroupedMatmul算子负载不均的分析结果。

只要有ep_balance分析能力对应的数据，执行解析命令，结果目录下默认会生成该分析结果的热力图图1，图中横轴为各个Device对应的Process ID，纵轴为模型的Decoder Layer层。图中像素点越亮说明耗时越久，各行色差越大说明负载不均现象越明显。
**表10**ep_balance.csv
字段

说明

<Process ID>（行表头）

该文件中的行表头显示的是各个Device运行时的进程ID。

<Decoder Layer>（列取值）

该文件中的列取值为各个Device运行的模型Decoder Layer层的序号。
|  |  |
| --- | --- |
|  |  |
|  |  |
**图1**
![](figure/zh-cn_image_0000002534427447.png "点击放大")ep_balance.png
#### moe_analysis.csv

记录DeepSeek专家模型服务化推理时，基于MSPTI采集的MoeDistributeCombine算子和MoeDistributeDispatch算子快慢卡分析结果。

只要有moe_analysis分析能力对应的数据，执行解析命令，结果目录下默认会生成该分析结果的箱型图图2，图中横轴为各个Device对应的Process ID，纵轴为耗时之和。图中展示耗时之和的均值和上下2.5%分位点，各个卡之间差距越大，上下分位点间隔越远，说明快慢卡现象越明显。
**表11**moe_analysis.csv
字段

说明

Dataset

对应Device的Process ID。

Mean

该Device上MoeDistributeCombine算子和MoeDistributeDispatch算子的耗时之和的平均值。

CI Lower

该Device上MoeDistributeCombine算子和MoeDistributeDispatch算子之和的下2.5%分位数。

CI Upper

该Device上MoeDistributeCombine算子和MoeDistributeDispatch算子之和的上2.5%分位数。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
**图2**
![](figure/zh-cn_image_0000002534507483.png "点击放大")moe_analysis.png
#### request_status.csv

统计服务化推理过程中，各个时刻的请求状态（处于waiting、running或swapped状态的请求个数）。可以根据统计的数据，绘制折线图，反映请求状态的变化趋势。
**表12**request_status.csv
字段

说明

hostuid

节点ID。

pid

进程ID。

timestamp(ms)

时间戳，单位ms。

relative_timestamp(ms)

相对时间戳，单位ms。

waiting

处于waiting状态的请求个数。

running

处于running状态的请求个数。

swapped

处于swapped状态的请求个数。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### {host_name}_eplb_{i}_summed_hot_map_by_expert.png

专家热点信息热力图，图3中的像素点可以根据右侧图例的亮度判断，亮度越高代表热度越高。

- host_name表示所在的设备名称。
- i表示MindIE开启动态负载均衡场景时，服务化profiling采集周期内，负载均衡表更新的次数；不开启动态负载均衡时，i为0。
**图3**
![](figure/zh-cn_image_0000002502587632.png "点击放大")热力图
横轴为专家编号，纵轴代表模型的moe层。

专家编号为模型实例中，Rank_ID从小到大排序，每个Rank内按照顺序进行编号，例如16张卡，每张卡17个专家，专家编号为42的专家代表Rank_2（第三张卡）的expert_7（第8个专家）。

#### {host_name}_eplb_{i}_summed_hot_map_by_rank.png

专家热点信息热力图，图4中的像素点可以根据右侧图例的亮度判断，亮度越高代表热度越高。

- host_name表示所在的设备名称。
- i表示MindIE开启动态负载均衡场景时，服务化profiling采集周期内，负载均衡表更新的次数；不开启动态负载均衡时，i为0。
**图4**
![](figure/zh-cn_image_0000002534427449.png "点击放大")热力图
横轴为Rank_ID，纵轴代表模型的moe层。

#### {host_name}_eplb_{i}_summed_hot_map_by_model_expert.png

专家热点信息热力图，图5中的像素点可以根据右侧图例的亮度判断，亮度越高代表热度越高。

- host_name表示所在的设备名称。
- i表示MindIE开启动态负载均衡场景时，服务化profiling采集周期内，负载均衡表更新的次数；不开启动态负载均衡时，i为0。
- 该图需要开启MindIE的动态负载均衡特性才会生成。
**图5**
![](figure/zh-cn_image_0000002534507485.png "点击放大")热力图
横轴为模型的专家编号，其中共享专家编号排列在最后，纵轴代表模型的MoE层。
**父主题：**[数据解析](atlasprofiling_16_0032.html)