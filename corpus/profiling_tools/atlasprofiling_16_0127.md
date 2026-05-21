---
title: "采集并落盘性能数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0127.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0127.html"
---

# 采集并落盘性能数据

[通过调用API方式使能性能数据采集功能，从而自动采集性能原始数据。采集性能原始数据成功后，可将采集的原始数据拷贝到装有CANN-Toolkit开发套件包和ops算子包的开发环境上进行原始性能数据解析](atlasprofiling_16_0015.html#ZH-CN_TOPIC_0000002536038287)，可视化展示原始性能数据解析结果。

#### API简介
**表1**API简介
接口

说明

aclprofCreateConfig

创建Profiling配置。与aclprofDestroyConfig成对使用。

aclprofInit

初始化Profiling，目前用于设置保存性能数据的文件的路径。与aclprofFinalize成对使用。

aclprofSetConfig

aclprofCreateConfig的扩展接口，用于设置采集配置参数。

aclprofStart

下发Profiling请求，使能对应数据的采集。与aclprofStop成对使用。

aclprofStop

停止Profiling数据采集。与aclprofStart成对使用。

aclprofFinalize

结束Profiling。与aclprofInit成对使用。

aclprofDestroyConfig

销毁通过aclprofCreateConfig接口创建的aclprofConfig类型的数据。与aclprofCreateConfig成对使用。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

aclprofInit接口传入的性能采集数据的落盘路径，需要确保用户进程具有读写权限。

[接口详细说明，请参见“Profiling数据采集](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/appdevgapi/aclcppdevg_03_1257.html)”。

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
```

```
// 1.调用aclInit初始化

// 2.申请运行管理资源，包括设置用于计算的Device、创建Context、创建Stream

// 3.Profiling初始化
// 设置数据落盘路径
const char *aclProfPath = "./output";
aclprofInit(aclProfPath, strlen(aclProfPath));

// 4.进行Profiling配置
uint32_t deviceIdList[1] = {0};    // 须根据实际环境的Device ID配置
// 创建配置结构体
aclprofConfig *config = aclprofCreateConfig(deviceIdList, 1, ACL_AICORE_ARITHMETIC_UTILIZATION, 
    nullptr,ACL_PROF_ACL_API | ACL_PROF_TASK_TIME);
const char *memFreq = "15";
ret = aclprofSetConfig(ACL_PROF_SYS_HARDWARE_MEM_FREQ, memFreq, strlen(memFreq));
aclprofStart(config);

// 5.模型加载，加载成功后，返回标识模型的modelId

// 6.创建aclmdlDataset类型的数据，用于描述模型的输入数据input、输出数据output
 
// 7.执行模型
ret = aclmdlExecute(modelId, input, output);

// 8.处理模型推理结果

// 9.释放描述模型输入/输出信息、内存等资源，卸载模型

// 10.关闭Profiling配置, 释放配置资源, 释放Profiling组件资源
aclprofStop(config);
aclprofDestroyConfig(config);
aclprofFinalize();

// 11.释放运行管理资源

// 12.调用aclFinalize去初始化
//......

```
|  |  |
| --- | --- |
上述API调用示例中接口的配置参数取值参考以下，请根据实际情况选择需要的采集参数。
- **aclprofCreateConfig**接口：
```
1
```

```
ACL_PROF_ACL_API | ACL_PROF_TASK_TIME | ACL_PROF_OP_ATTR | ACL_PROF_AICORE_METRICS | ACL_PROF_AICPU | ACL_PROF_L2CACHE | ACL_PROF_HCCL_TRACE | ACL_PROF_MSPROFTX | ACL_PROF_RUNTIME_API | ACL_PROF_TASK_MEMORY | ACL_PROF_TRAINING_TRACE

```
|  |  |
| --- | --- |

[参数详细介绍请参见“aclprofCreateConfig](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/appdevgapi/aclcppdevg_03_1610.html)**”接口的dataTypeConfig**参数说明。

- **aclprofSetConfig**接口：
```
1
```

```
ACL_PROF_STORAGE_LIMIT | ACL_PROF_SYS_HARDWARE_MEM_FREQ | ACL_PROF_LLC_MODE | ACL_PROF_SYS_IO_FREQ | ACL_PROF_SYS_INTERCONNECTION_FREQ | ACL_PROF_DVPP_FREQ | ACL_PROF_HOST_SYS | ACL_PROF_HOST_SYS_USAGE | ACL_PROF_HOST_SYS_USAGE_FREQ

```
|  |  |
| --- | --- |

[参数详细介绍请参见“aclprofSetConfig](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/appdevgapi/aclcppdevg_03_1259.html)**”接口的configType**参数说明。

**父主题：**[使用acl C&C++接口采集性能数据](atlasprofiling_16_0125.html)