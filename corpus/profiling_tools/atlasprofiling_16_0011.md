---
title: "采集Host侧系统数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0011.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0011.html"
---

# 采集Host侧系统数据

msprof支持采集Host侧的系统数据（CPU利用率、内存利用率、磁盘I/O利用率、网络I/O利用率等），并且在采集后可以自动进行性能数据解析和文件落盘。

#### 依赖AI任务运行时采集命令示例

以运行用户登录CANN Toolkit开发套件包和ops算子包所在环境，执行性能数据采集命令。
****************
```
msprof --output=/home/projects/output --host-sys=cpu /home/projects/MyApp/out/main
```

#### 依赖昇腾AI处理器系统采集命令示例

以运行用户登录CANN Toolkit开发套件包和ops算子包所在环境，执行性能数据采集命令。
**********************************
```
msprof --output=/home/projects/output --sys-devices=<ID> --sys-period=<period> --sys-hardware-mem=on --host-sys-pid=<pid> --host-sys=cpu
```

#### 参数说明
**表1**参数说明
参数

描述

**可选/必选**

结果文件

--host-sys

**Host侧系统数据采集开关，取值包括cpu、mem、disk、network和osrt，可选其中的一项或多项，选多项时用英文逗号隔开。配置该项必须配置host-sys-pid**参数或传入用户程序。各项取值含义如下：

- cpu：进程级别的CPU利用率。
- mem：进程级别的内存利用率。
- disk：进程级别的磁盘I/O利用率。
- network：系统级别的网络I/O利用率。
- osrt：进程级别的syscall和pthreadcall。

**配置示例：--host-sys**=cpu,mem,disk,network。
说明：
- [采集Host侧disk性能数据需要安装第三方开源工具iotop，采集osrt性能数据需要安装第三方开源工具perf和ltrace，其安装方法参见安装perf、iotop、ltrace工具](atlasprofiling_16_0210.html#ZH-CN_TOPIC_0000002504358452)[。完成安装后须参见配置用户权限](atlasprofiling_16_0211.html#ZH-CN_TOPIC_0000002536038405)完成用户权限配置，且每次重新安装CANN软件包需要重新配置。
- 使用开源工具ltrace采集osrt性能数据会导致CPU占用率过高，其与应用工程的pthread加解锁相关，会影响进程运行速度。
- x86_64架构的KylinV10SP1操作系统支持--host-sys=osrt参数， aarch64架构的KylinV10SP1操作系统下不支持--host-sys=osrt参数。
- 虚拟化环境Euler2.9系统下不支持--host-sys=network参数。

--host-sys和--host-sys-usage二者必选其一

[msprof_*.json中的CPU Usage层级和host_cpu_usage_*.csv文件](atlasprofiling_16_0190.html#ZH-CN_TOPIC_0000002504358442)

[msprof_*.json中的Memory Usage层级和host_mem_usage_*.csv文件](atlasprofiling_16_0191.html#ZH-CN_TOPIC_0000002536038393)

[msprof_*.json中的Disk Usage层级和host_disk_usage_*.csv文件](atlasprofiling_16_0192.html#ZH-CN_TOPIC_0000002536158423)

[msprof_*.json中的Network Usage层级和host_network_usage_*.csv文件](atlasprofiling_16_0193.html#ZH-CN_TOPIC_0000002504198606)

[msprof_*.json中的OS Runtime API层级和os_runtime_statistic_*.csv文件](atlasprofiling_16_0194.html#ZH-CN_TOPIC_0000002504358444)

[db文件的CPU_USAGE表](atlasprofiling_16_0142.html#ZH-CN_TOPIC_0000002504358416__zh-cn_topic_0000002534398437_section730161613343)

[db文件的HOST_MEM_USAGE表](atlasprofiling_16_0142.html#ZH-CN_TOPIC_0000002504358416__zh-cn_topic_0000002534398437_section17298155016408)

[db文件的HOST_DISK_USAGE表](atlasprofiling_16_0142.html#ZH-CN_TOPIC_0000002504358416__zh-cn_topic_0000002534398437_section32136221402)

[db文件的HOST_NETWORK_USAGE表](atlasprofiling_16_0142.html#ZH-CN_TOPIC_0000002504358416__zh-cn_topic_0000002534398437_section223093643915)

[db文件的OSRT_API表](atlasprofiling_16_0142.html#ZH-CN_TOPIC_0000002504358416__zh-cn_topic_0000002534398437_section7238121863614)

--host-sys-usage

**Host侧系统和所有进程的性能数据采集开关，取值包括cpu和mem，可选其中的一项或多项，选多项时用英文逗号隔开。配置该项时如果配置host-sys-pid**参数，则采集Host侧指定进程的CPU或内存利用率。取值含义如下：

- cpu：系统和所有进程的CPU利用率。
- mem：系统和所有进程的内存利用率。

**配置示例：--host-sys-usage**=cpu,mem。

--host-sys和--host-sys-usage二者必选其一

[Host侧系统CPU利用率数据](atlasprofiling_16_0195.html#ZH-CN_TOPIC_0000002536038397)

[Host侧进程CPU利用率数据](atlasprofiling_16_0196.html#ZH-CN_TOPIC_0000002536158425)

[Host侧系统内存利用率数据](atlasprofiling_16_0197.html#ZH-CN_TOPIC_0000002504198610)

[Host侧进程内存利用率数据](atlasprofiling_16_0198.html#ZH-CN_TOPIC_0000002504358446)

--host-sys-pid

指定需要采集的Host侧应用程序的pid。

依赖AI任务运行时该参数无需配置，且配置无效。

可选

-

--host-sys-usage-freq

CPU利用率、内存利用率的采集频率，范围[1,50]，默认值50，单位Hz。

可选

-
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
**父主题：**[性能数据采集和自动解析](atlasprofiling_16_0007.html)