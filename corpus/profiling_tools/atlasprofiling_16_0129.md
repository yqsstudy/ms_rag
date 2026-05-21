---
title: "订阅算子信息"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0129.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0129.html"
---

# 订阅算子信息

通过调用消息订阅接口实现将采集到的Profiling数据解析后写入管道，由用户读入内存，再由用户调用API获取性能数据。当前支持获取网络模型中算子的性能数据，包括算子名称、算子类型名称、算子执行时间等。

#### API简介
**表1**API简介
接口

说明

aclprofCreateSubscribeConfig

创建aclprofSubscribeConfig类型的数据，表示创建订阅配置信息。

aclprofModelSubscribe

订阅算子的基本信息，包括算子名称、算子类型、算子执行耗时等。同步接口。

与aclprofModelUnSubscribe成对使用。

aclprofGet*

获取算子的基本信息。“*”包括：

OpDescSize：算子数据结构大小。

OpNum：算子个数。

OpTypeLen：算子类型的字符串长度。

OpType：算子类型。

OpNameLen：算子名称的字符串长度。

OpName：算子名称。

OpStart：算子执行开始时间。

OpEnd：算子执行结束时间。

OpDuration：算子执行耗时。

ModelId：算子所在模型ID。

以上信息通过INFO_LOG接口将Profiling结果显示在屏幕上。

aclprofModelUnSubscribe

网络场景下，取消订阅算子的基本信息，包括算子名称、算子类型、算子执行耗时等。同步接口。

需要与aclprofModelSubscribe接口配对使用。

aclprofDestroySubscribeConfig

销毁通过aclprofCreateSubscribeConfig接口创建的aclprofSubscribeConfig类型的数据。同步接口。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

[接口详细说明，请参见“Profiling数据采集](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/appdevgapi/aclcppdevg_03_1257.html)”。

#### API调用示例

示例如下：

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
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
```

```
// 1.调用aclInit初始化

// 2.申请运行管理资源，包括设置用于计算的Device、创建Context、创建Stream

// 3.模型加载，加载成功后，返回标识模型的modelId

// 4.创建aclmdlDataset类型的数据，用于描述模型的输入数据input、输出数据output

// 5.创建管道（UNIX操作系统下需要引用C++标准库头文件unistd.h），用于读取以及写入模型订阅的数据
int subFd[2];
// 读管道指针指向subFd[0]，写管道指针指向subFd[1] 
pipe(subFd);

// 6.创建模型订阅的配置并且进行模型订阅
aclprofSubscribeConfig *config = aclprofCreateSubscribeConfig(1, ACL_AICORE_NONE, &subFd[1]);
//模型订阅需要传入模型的modelId
aclprofModelSubscribe(modelId, config);

// 7.实现管道读取订阅数据的函数
// 7.1自定义函数，实现从用户内存中读取订阅数据的函数
void getModelInfo(void *data, uint32_t len) {
    uint32_t opNumber = 0;
    uint32_t dataLen = 0;
    // 读取算子信息个数
    aclprofGetOpNum(data, len, &opNumber);
    // 遍历用户内存的算子信息
    for (int32_t i = 0; i < opNumber; i++){
        // 获取算子的模型id
        uint32_t modelId = aclprofGetModelId(data,len, i);
        // 获取算子的类型名称长度
        size_t opTypeLen = 0;
        aclprofGetOpTypeLen(data, len, i, &opTypeLen);
        // 获取算子的类型名称
        char opType[opTypeLen];
        aclprofGetOpType(data, len, i, opType, opTypeLen);
        // 获取算子的详细名称长度
        size_t opNameLen = 0;
        aclprofGetOpNameLen(data, len, i, &opNameLen);
        // 获取算子的详细名称
        char opName[opNameLen];
        aclprofGetOpName(data, len, i, opName, opNameLen);
        // 获取算子的执行开始时间
        uint64_t opStart = aclprofGetOpStart(data, len, i);
        // 获取算子的执行结束时间
        uint64_t opEnd = aclprofGetOpEnd(data, len, i);
        uint64_t opDuration = aclprofGetOpDuration(data, len, i);
    }
}

// 7.2自定义函数，实现从管道中读取数据到用户内存的函数
void *profDataRead(void *fd) {
    // 设置每次从管道中读取的算子信息个数
    uint64_t N = 10;
    // 获取单位算子信息的大小（Byte）
    uint64_t bufferSize = 0;
    aclprofGetOpDescSize(&bufferSize);
    // 计算存储算子信息的内存的大小，并且申请内存
    uint64_t readbufLen = bufferSize * N;
    char *readbuf = new char[readbufLen];
    // 从管道中读取数据到申请的内存中，读取到的实际数据大小dataLen可能小于bufferSize * N，如果管道中没有数据，默认会阻塞直到读取到数据为止
    auto dataLen = read(*(int*)fd, readbuf, readbufLen);
    // 读取数据到readbuf成功
    while (dataLen > 0) {
        // 调用5.1实现的函数解析内存中的数据
        getModelInfo(readbuf, dataLen);
        memset(readbuf, 0, bufferSize);
        dataLen = read(*(int*)fd, readbuf, readbufLen);
    }
    delete []readbuf;
}

// 8.启动线程读取管道数据并解析
pthread_t subTid = 0;
pthread_create(&subTid, NULL, profDataRead, &subFd[0]);

// 9.执行模型
ret = aclmdlExecute(modelId, input, output);

// 10.处理模型推理结果

// 11.释放描述模型输入/输出信息、内存等资源，卸载模型

// 12.取消订阅，释放订阅相关资源
aclprofModelUnSubscribe(modelId);
pthread_join(subTid, NULL);
// 关闭读管道指针
close(subFd[0]);
// 释放config指针
aclprofDestroySubscribeConfig(config);

// 13.释放运行管理资源

// 14.调用aclFinalize去初始化
//......

```
|  |  |
| --- | --- |
**父主题：**[使用acl C&C++接口采集性能数据](atlasprofiling_16_0125.html)