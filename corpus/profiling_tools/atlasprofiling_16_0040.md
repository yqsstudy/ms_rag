---
title: "使用前准备"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0040.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0040.html"
---

# 使用前准备

#### 数据准备

[已完成数据解析](atlasprofiling_16_0032.html#ZH-CN_TOPIC_0000002536158329)。

确认在--output-path指定的路径下存在SQLite数据库文件profiler.db。

#### 环境依赖

Grafana=11.3.0，并安装SQLite插件=11.3.0。

**安装并连接Grafana**

[Grafana安装官方网址https://grafana.com/grafana/download?platform=arm&edition=oss](https://grafana.com/grafana/download?platform=arm&edition=oss)，下载安装对应开源版本解压运行。例如：

```
tar -zxvf grafana-11.3.0.linux-arm64.tar.gz
cd grafana-v11.3.0/bin/
./grafana-server
```

配置Windows代理，需要添加Linux设备IP前缀，例如90.90.*;90.91.*，访问http://Linux设备IP:3000/即可打开Grafana的Web端，初始账号密码都为admin。


**父主题：**[Grafana可视化](atlasprofiling_16_0039.html)