---
title: "简介"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0049.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0049.html"
---

# 简介

msServiceProfiler Trace提供基于OpenTelemetry Protocol（OTLP）协议的Trace数据转发服务，该服务用于接收、处理和转发分布式Trace数据，帮助用户监控和分析微服务架构的性能表现。

msServiceProfiler Trace采集MindIE Motor服务中的请求响应时间、响应状态、客户端IP/端口、服务端IP/端口等数据，最后将采集到的数据推送至Jaeger等支持OTLP协议的开源监控平台进行可视化分析。

- 当前版本主要面向MindIE推理框架，支持单机及多机PD竞争部署模式。
- [当前仅支持对MindIE的/v1/chat/completions](https://www.hiascend.com/document/detail/zh/mindie/22RC1/mindieservice/servicedev/mindie_service0078.html)[和/v1/completions](https://www.hiascend.com/document/detail/zh/mindie/22RC1/mindieservice/servicedev/mindie_service0323.html)两个请求发送的核心接口进行Trace监控。
- [msServiceProfiler Trace数据监控接口包括“msServiceProfiler API参考（C++） > Trace数据监控](atlasprofiling_16_0080.html#ZH-CN_TOPIC_0000002536158359)”。
- [有关MindIE Motor相关介绍请参见《MindIE Motor开发指南](https://www.hiascend.com/document/detail/zh/mindie/22RC1/mindieservice/servicedev/mindie_service0001.html)》。
**父主题：**[msServiceProfiler Trace数据监控](atlasprofiling_16_0048.html)