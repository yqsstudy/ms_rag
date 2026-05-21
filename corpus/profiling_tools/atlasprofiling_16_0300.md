---
title: "mstx API使用示例"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0300.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0300.html"
---

# mstx API使用示例

本节中提供的代码仅为示例，非完整代码，完整样例代码获取请参照如下步骤：

1. 请确保安装CANN-Toolkit开发套件包和ops算子包。
[参见《CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0000.html?Mode=PmIns&InstallType=local&OS=openEuler)》。

2. mstx API样例代码集成在CANN-Toolkit开发套件包中，路径为${INSTALL_DIR}/tools/mstx/samples。
${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。若安装的Ascend-cann-toolkit软件包，以root安装举例，则安装后文件存储路径为：/usr/local/Ascend/ascend-toolkit/latest。

3. 根据路径下的README文档使用样例。

[更多mstx API介绍请参见《MindStudio mstx API参考](https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0001.html)》。

使用mstx API执行采集操作示例代码如下：

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
```

```
aclrtContext context_;
aclrtStream stream_;
 
// 1.AscendCL初始化
aclError ret = ACL_ERROR_NONE;
ret = aclInit(nullptr);
if (ret != ACL_SUCCESS) {
    ERROR_LOG("aclInit failed");
    return FAILED;
}
 
// 2.申请运行管理资源，包括设置用于计算的Device、创建Context、创建Stream
ret = aclrtSetDevice(0);
if (ret != ACL_ERROR_NONE) {
    ERROR_LOG("aclrtSetDevice failed");
    return FAILED;
}
ret = aclrtCreateContext(&context_, 0);
if (ret != ACL_ERROR_NONE) {
    ERROR_LOG("acl create context failed");
    return FAILED;
}
ret = aclrtCreateStream(&stream_);
if (ret != ACL_ERROR_NONE) {
    ERROR_LOG("acl create stream failed");
    return FAILED;
}
....
 
// 3.在想采集耗时的代码位置添加打点代码，比如在执行模型前后打点，获取模型执行耗时
mstxRangeId rangeId = mstxRangeStartA("model execute", nullptr); // 第二个入参设置nullptr，只记录host侧range耗时(适用于纯host侧代码段)；设置有效的stream，同时记录host侧和对应device侧耗时(适用于下发计算任务或通信任务)
ret = aclmdlExecute(modelId, input, output); // 执行模型样例代码
mstxRangeEnd(rangeId);

// 4.步骤3里的打点数据属于默认domain；可调用mstx domain相关接口，创建自定义domain，并指定domain进行打点
mstxDomainHandle_t selfDomain = mstxDomainCreateA("self_domain");
mstxRangeId domainRangeId = mstxDomainRangeStartA(selfDomain, "model execute", nullptr);
ret = aclmdlExecute(modelId, input, output); // 执行模型样例代码
mstxDomainRangeEnd(selfDomain, domainRangeId);
 
// 5.释放运行管理资源
 
// 6.AscendCL去初始化

```
|  |  |
| --- | --- |
**父主题：**[附录](atlasprofiling_16_0209.html)