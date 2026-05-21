---
title: "输出结果说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0056.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0056.html"
---

# 输出结果说明

[完成发送请求](atlasprofiling_16_0055.html#ZH-CN_TOPIC_0000002536038317)后，可以在支持OTLP协议的开源监控平台（例如Jaeger，须先开启Jaeger平台服务）查看可视化结果，示例如下。
**图1**
可视化结果
字段说明如下：
**表1**基础信息
字段

说明

traceID

Trace链路的唯一标识符，string类型，示例值79f92f3577b34da6a3ce929d0e0e4703。

spanID

当前Span的唯一标识符，string类型，示例值4736e32cc09f0000。

operationName

操作/接口名称，string类型，示例值server.Request。

startTime

Span开始时间，int类型，单位us，示例值1763784983019248。

duration

Span持续时间，int类型，单位us，示例值328。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
**表2**服务信息
字段

说明

tags[key=otel.scope.name]

服务/模块名称，string类型，示例值LLM。

tags[key=server.method]

HTTP请求方法，string类型，示例值POST。

tags[key=server.path]

请求路径，string类型，示例值/v1/chat/completions。

tags[key=span.kind]

Span类型，string类型，示例值server。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
**表3**网络信息
字段

说明

tags[key=server.net.host.ip]

服务端IP地址，string类型，示例值127.0.0.7。

tags[key=server.net.host.port]

服务端端口，string类型，示例值7025。

tags[key=server.net.peer.ip]

客户端IP地址，string类型，示例值127.0.0.1。

tags[key=server.net.peer.port]

客户端端口，string类型，示例值36694。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
**表4**状态信息
字段

说明

tags[key=error]

是否发生错误（仅当请求返回错误时存在），bool类型。

示例值：

- 请求错误时为true。
- 请求正确时不出现该值。

tags[key=otel.status_code]

OpenTelemetry状态码，string类型。

示例值：

- 请求正确时为OK。
- 请求错误时为ERROR。

tags[key=otel.status_description]

错误详细描述（仅当请求返回错误时存在），string类型，示例值{"error":"Request param contains not messages or messages null","error_type":"Input Validation Error"}。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
**父主题：**[msServiceProfiler Trace数据监控](atlasprofiling_16_0048.html)