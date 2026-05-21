---
title: "配置目标采集服务器"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0053.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0053.html"
---

# 配置目标采集服务器

出于安全考虑，推荐用户使用安全模式，建议使用TLS认证。

[在启动Trace转发进程](atlasprofiling_16_0054.html#ZH-CN_TOPIC_0000002504358370)前，需要通过环境变量设置目标采集服务器。

当前支持以下四种协议配置。

- HTTP
```
export OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf"
export OTEL_EXPORTER_OTLP_ENDPOINT=http://xxx:xxx/v1/traces    # 配置数据转发的IP和端口，例如http://localhost:4318/v1/traces
```

- HTTP + TLS
```
export OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf"
export OTEL_EXPORTER_OTLP_ENDPOINT=https://xxx:xxx/v1/traces    # 配置数据转发的IP和端口，例如https://localhost:4318/v1/traces
export OTEL_EXPORTER_OTLP_CERTIFICATE=/home/certificates/ca/ca.crt    # 设置证书的绝对路径，该目录属主、文件属主和当前用户一致，目录权限700，文件权限600
```

- gRPC
```
export OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
export OTEL_EXPORTER_OTLP_ENDPOINT=http://xxx:xxx    # 配置数据转发的IP和端口，例如http://localhost:4317
```

- gRPC + TLS
```
export OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
export OTEL_EXPORTER_OTLP_ENDPOINT=https://xxx:xxx    # 配置数据转发的IP和端口，例如https://localhost:4317
export OTEL_EXPORTER_OTLP_CERTIFICATE=/home/certificates/ca/ca.crt    # 设置证书的绝对路径，该目录属主、文件属主和当前用户一致，目录权限700，文件权限600
```


- 当前只支持单向认证，双向认证相关配置参数不支持，配置会导致功能不可用。不可用配置参数如下：
  - OTEL_EXPORTER_OTLP_TRACES_CLIENT_KEY
  - OTEL_EXPORTER_OTLP_CLIENT_KEY
  - OTEL_EXPORTER_OTLP_TRACES_CLIENT_CERTIFICATE
  - OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE

- 本工具依赖OpenTelemetry三方库实现。本文仅说明此工具使用的必备参数。更多功能接口请开发者深入其官方文档自行探索。
**父主题：**[数据采集](atlasprofiling_16_0051.html)