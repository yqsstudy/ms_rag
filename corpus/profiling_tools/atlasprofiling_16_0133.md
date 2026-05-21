---
title: "采集并落盘性能数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0133.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0133.html"
---

# 采集并落盘性能数据

[通过调用API方式使能Profiling功能，从而自动采集性能原始数据。采集性能原始数据成功后，可将采集的原始数据拷贝到装有CANN-Toolkit开发套件包和ops算子包的开发环境上进行原始性能数据解析](atlasprofiling_16_0015.html#ZH-CN_TOPIC_0000002536038287)，可视化展示原始性能数据解析结果。

#### API简介
**表1**API简介
接口

说明

acl.prof.create_config

创建Profiling配置。与acl.prof.destroy_config成对使用。

acl.prof.init

初始化Profiling，目前用于设置保存性能数据的文件的路径。与acl.prof.finalize成对使用。

acl.prof.start

下发Profiling请求，使能对应数据的采集。与acl.prof.stop成对使用。

acl.prof.stop

停止Profiling数据采集。与acl.prof.start成对使用。

acl.prof.finalize

结束Profiling。与acl.prof.init成对使用。

acl.prof.destroy_config

销毁通过acl.prof.create_config接口创建的aclprofConfig类型。与acl.prof.create_config成对使用。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

- **调用acl.prof.init****后，会采集后续所有模型加载数据，包括Device侧、Host侧以及timeline汇总数据。如果在调用acl.prof.start**接口时，仅指定部分Device采集性能数据，那么其余Device由于仅存在模型加载数据而无法解析。
- **acl.prof.init**接口传入的Profiling性能采集数据的落盘路径，需要确保用户进程具有读写权限。

#### API调用示例

API调用示例如下：

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
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
```

```
import acl
import numpy as np
# ......

# 1.申请运行管理资源，包括设置用于计算的Device、创建Context、创建Stream
# ......

# 2.模型加载，加载成功后，返回标识模型的model_id
# ......

# 3.创建aclmdlDataset类型的数据，用于描述模型的输入数据input、输出数据output
# ......

# 4.Profiling初始化
# 设置数据落盘路径
PROF_INIT_PATH='...'
ret = acl.prof.init(PROF_INIT_PATH)

# 5.进行Profiling配置
device_list = [0]    # 须根据实际环境的Device ID配置
ACL_PROF_ACL_API = 0x0001
ACL_PROF_TASK_TIME = 0x0002
ACL_PROF_AICORE_METRICS = 0x0004
ACL_PROF_SYS_HARDWARE_MEM_FREQ = 3

# 创建配置类型指针地址
prof_config = acl.prof.create_config(device_list, 0, 0, ACL_PROF_ACL_API | ACL_PROF_TASK_TIME | ACL_PROF_AICORE_METRICS)
mem_freq = "15"
ret = acl.prof.set_config(ACL_PROF_SYS_HARDWARE_MEM_FREQ, mem_freq)
ret = acl.prof.start(prof_config)

# 6.执行模型
ret = acl.mdl.execute(model_id, input, output)

# 7.处理模型推理结果
# ......

# 8.释放描述模型输入/输出信息、内存等资源，卸载模型
# ......

# 9.关闭Profiling配置, 释放配置资源, 释放Profiling组件资源
ret = acl.prof.stop(prof_config)
ret = acl.prof.destroy_config(prof_config)
ret = acl.prof.finalize()

# 10.释放运行管理资源
# ......

```
|  |  |
| --- | --- |
上述API调用示例中接口的配置参数取值参考以下，请根据实际情况选择需要的采集参数。
- **acl.prof.create_config**接口：
```
1
```

```
ACL_PROF_ACL_API | ACL_PROF_TASK_TIME | ACL_PROF_AICORE_METRICS | ACL_PROF_AICPU | ACL_PROF_L2CACHE | ACL_PROF_HCCL_TRACE | ACL_PROF_MSPROFTX | ACL_PROF_RUNTIME_API | ACL_PROF_TRAINING_TRACE

```
|  |  |
| --- | --- |

[参数详细介绍请参见“函数：create_config](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/appdevgapi/aclpythondevg_01_0848.html)**”的data_type_config**参数说明。

- **acl.prof.set_config**接口：
```
1
```

```
ACL_PROF_STORAGE_LIMIT | ACL_PROF_SYS_HARDWARE_MEM_FREQ | ACL_PROF_LLC_MODE | ACL_PROF_SYS_IO_FREQ | ACL_PROF_SYS_INTERCONNECTION_FREQ | ACL_PROF_DVPP_FREQ | ACL_PROF_HOST_SYS | ACL_PROF_HOST_SYS_USAGE | ACL_PROF_HOST_SYS_USAGE_FREQ

```
|  |  |
| --- | --- |

[参数详细介绍请参见“函数：set_config](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/appdevgapi/aclpythondevg_01_0849.html)**”的config_type**参数说明。

**父主题：**[使用acl Python接口采集性能数据](atlasprofiling_16_0131.html)