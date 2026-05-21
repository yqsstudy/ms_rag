---
title: "使用msproftx扩展接口采集并落盘性能数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0128.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0128.html"
---

# 使用msproftx扩展接口采集并落盘性能数据

为了获取用户和上层框架程序的性能数据，Profiling开启msproftx功能之前，需要在程序内调用msproftx相关接口来对用户程序进行打点以输出对应的性能数据。

#### API简介
**表1**API简介
接口

说明

aclprofCreateStamp

创建msproftx事件标记，用于描述瞬时事件。

aclprofSetStampTraceMessage

为msproftx事件标记携带描述信息，在Profiling解析结果中msprof_tx summary数据展示。

aclprofMark

msproftx标记瞬时事件。

aclprofMarkEx

aclprofMarkEx打点接口。

aclprofPush

msproftx用于记录事件发生的时间跨度的开始时间。与aclprofPop成对使用，仅能在单线程内使用。

aclprofPop

msproftx用于记录事件发生的时间跨度的结束时间。与aclprofPush成对使用，仅能在单线程内使用。

aclprofRangeStart

msproftx用于记录事件发生的时间跨度的开始时间。与aclprofRangeStop成对使用，可跨线程使用。

aclprofRangeStop

msproftx用于记录事件发生的时间跨度的结束时间。与aclprofRangeStart成对使用，可跨线程使用。

aclprofDestroyStamp

释放msproftx事件标记。
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

当只开启msproftx功能时，aclCreateProfConfig接口的deviceIdList参数值需设为空，deviceNums参数值设为0。

[接口详细说明，请参见“Profiling数据采集](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/appdevgapi/aclcppdevg_03_1257.html)”。

#### API调用示例

- 示例一（aclprofMark示例）
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
48
49
50
51
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
    nullptr,ACL_PROF_ACL_API | ACL_PROF_TASK_TIME | ACL_PROF_MSPROFTX);
const char *memFreq = "15";
ret = aclprofSetConfig(ACL_PROF_SYS_HARDWARE_MEM_FREQ, memFreq, strlen(memFreq));
aclprofStart(config);

aclprofStepInfo *stepInfo = aclprofCreateStepInfo();
int ret = aclprofGetStepTimestamp(stepInfo, ACL_STEP_START, stream_);

// 5.模型加载，加载成功后，返回标识模型的modelId
stamp = aclprofCreateStamp();
aclprofSetStampTraceMessage(stamp, "model_load_mark", strlen("model_load_mark"));
aclprofMark(stamp);    // 标记模型加载事件
aclprofDestroyStamp(stamp);

// 6.创建aclmdlDataset类型的数据，用于描述模型的输入数据input、输出数据output

// 7.执行模型
stamp = aclprofCreateStamp();
aclprofSetStampTraceMessage(stamp, "model_exec_mark", strlen("model_exec_mark"));
aclprofMark(stamp);    // 标记模型执行事件
aclprofDestroyStamp(stamp);
ret = aclmdlExecute(modelId, input, output);

// 8.处理模型推理结果

// 9.释放描述模型输入/输出信息、内存等资源，卸载模型
int ret = aclprofGetStepTimestamp(stepInfo, ACL_STEP_END, stream_);
aclprofDestroyStepInfo(stepInfo);

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

- 示例二（aclprofMarkEx示例，标识用户funcA接口）
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
```

```
aclrtStream stream;
aclrtCreateStream(&stream);
aclError markRet;
markRet = aclprofMarkEx("funcA", strlen("funcA"), stream);
if (markRet != ACL_ERROR_NONE) {
    printf("mark execute start failed");
}
// 用户业务接口
funcA();

```
|  |  |
| --- | --- |

- 示例三（aclprofPush/aclprofPop示例，适用于单线程）
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
48
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
    nullptr,ACL_PROF_ACL_API | ACL_PROF_TASK_TIME | ACL_PROF_MSPROFTX);
const char *memFreq = "15";
ret = aclprofSetConfig(ACL_PROF_SYS_HARDWARE_MEM_FREQ, memFreq, strlen(memFreq));
aclprofStart(config);

aclprofStepInfo *stepInfo = aclprofCreateStepInfo();
int ret = aclprofGetStepTimestamp(stepInfo, ACL_STEP_START, stream_);

// 5.模型加载，加载成功后，返回标识模型的modelId

// 6.创建aclmdlDataset类型的数据，用于描述模型的输入数据input、输出数据output

// 7.执行模型（模型仅在单线程执行）
stamp = aclprofCreateStamp();
aclprofSetStampTraceMessage(stamp, "aclmdlExecute_duration", strlen("aclmdlExecute_duration"));
aclprofPush(stamp);
ret = aclmdlExecute(modelId, input, output);
aclprofPop();
aclprofDestroyStamp(stamp);

// 8.处理模型推理结果

// 9.释放描述模型输入/输出信息、内存等资源，卸载模型
int ret = aclprofGetStepTimestamp(stepInfo, ACL_STEP_END, stream_);
aclprofDestroyStepInfo(stepInfo);

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

- 示例四（aclprofRangeStart/aclprofRangeStop示例，适用于单线程或跨线程）
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
48
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
    nullptr,ACL_PROF_ACL_API | ACL_PROF_TASK_TIME | ACL_PROF_MSPROFTX);
const char *memFreq = "15";
ret = aclprofSetConfig(ACL_PROF_SYS_HARDWARE_MEM_FREQ, memFreq, strlen(memFreq));
aclprofStart(config);

aclprofStepInfo *stepInfo = aclprofCreateStepInfo();
int ret = aclprofGetStepTimestamp(stepInfo, ACL_STEP_START, stream_);

// 5.模型加载，加载成功后，返回标识模型的modelId

// 6.创建aclmdlDataset类型的数据，用于描述模型的输入数据input、输出数据output

// 7.执行模型（模型在跨线程执行）
stamp = aclprofCreateStamp();
aclprofSetStampTraceMessage(stamp, "aclmdlExecute_duration", strlen("aclmdlExecute_duration"));
aclprofRangeStart(stamp, &rangeId);
ret = aclmdlExecute(modelId, input, output);
aclprofRangeStop(rangeId);
aclprofDestroyStamp(stamp);

// 8.处理模型推理结果

// 9.释放描述模型输入/输出信息、内存等资源，卸载模型
int ret = aclprofGetStepTimestamp(stepInfo, ACL_STEP_END, stream_);
aclprofDestroyStepInfo(stepInfo);

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


msproftx扩展接口在main函数内调用。
**父主题：**[使用acl C&C++接口采集性能数据](atlasprofiling_16_0125.html)