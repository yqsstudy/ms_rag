---
title: "使用前准备"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0050.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0050.html"
---

# 使用前准备

#### 环境准备

1. [在昇腾NPU环境安装配套版本的CANN Toolkit开发套件包和ops算子包并配置CANN环境变量，具体请参见《CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0000.html?Mode=PmIns&InstallType=local&OS=openEuler)》。
2. 安装环境依赖，命令如下：

```
pip install opentelemetry-exporter-otlp-proto-grpc==1.33.1
pip install opentelemetry-exporter-otlp-proto-http==1.33.1
```

3. 完成MindIE的安装和配置并确认MindIE Motor可以正常运行，具体请参见《MindIE安装指南》。
4. MindIE Motor服务所在的昇腾NPU环境与OTLP采集器（Jaeger等）需建立稳定网络连接。

#### 约束

msServiceProfiler Trace转发数据最大支持400并发，超过400并发可能出现请求积压，请求积压超过100W，将出现数据丢失。

相关日志提示（下述日志每小时只上报1次）：

```
1
2
3
4
```

```
# 积压请求数量超过10w出现请求积压告警
2025-11-26 15:45:59,038 - 4059906 - msServiceProfiler - WARNING - Trace data is being stacked: {积压数量}
# 积压请求数量超过100w出现数据丢失告警
2025-11-26 15:45:59,522 - 4059906 - msServiceProfiler - WARNING - Trace data queue is full, discarding the oldest data.

```
|  |  |
| --- | --- |
**父主题：**[msServiceProfiler Trace数据监控](atlasprofiling_16_0048.html)