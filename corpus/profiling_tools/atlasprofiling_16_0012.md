---
title: "采集msproftx数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0012.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0012.html"
---

# 采集msproftx数据

当用户需要定位应用程序或上层框架程序的性能瓶颈时，可使用如下接口进行性能数据采集：

- [mstx API（MindStudio Tools Extension API）接口详细操作请参见mstx API使用示例](atlasprofiling_16_0300.html#ZH-CN_TOPIC_0000002536158477)。
- [msproftx扩展接口详细操作请参见《应用开发指南 (C&C++)](https://www.hiascend.com/document/detail/zh/canncommercial/850/appdevg/acldevg/aclcppdevg_000000.html)[》中的“Profiling性能数据采集](https://www.hiascend.com/document/detail/zh/canncommercial/850/appdevg/acldevg/aclcppdevg_000089.html)”。

以上两种接口二选一即可，推荐使用mstx API。

通过记录应用程序执行期间特定事件发生的时间跨度，写入性能数据文件。

#### 采集步骤（mstx API）

1. 在用户程序代码内调用mstx API。

接口通过记录应用程序执行期间特定事件发生的时间跨度，写入性能数据文件。

2. 以运行用户登录CANN Toolkit开发套件包和ops算子包所在环境，执行性能数据采集命令，命令示例如下：

  - 采集所有的打点数据（包括默认domain和用户自定义domain范围内的数据）：**************
```
msprof --msproftx=on /home/projects/MyApp/out/main
```

  - 若需要自定义采集某些domain的打点数据，可增加配置--mstx-domain-include或--mstx-domain-exclude开关：********************
```
# 用户程序调用前缀为“mstxDomain”的接口，指定domain进行打点，可配置--mstx-domain-include，输出需要的domain数据
msprof --msproftx=on --mstx-domain-include=a,b,c /home/projects/MyApp/out/main
# a,b,c表示用户想采集的domain范围，用逗号隔开
```

或
******************
```
# 用户程序调用前缀为“mstxDomain”的接口，指定domain进行打点，配置--mstx-domain-exclude，过滤不需要的domain数据
msprof --msproftx=on --mstx-domain-exclude=a,b,c /home/projects/MyApp/out/main
# a,b,c表示用户不想采集的domain范围，用逗号隔开
```

采集mstx数据必须传入用户程序。

#### 采集步骤（msproftx API）

1. 在采集进程内（aclprofStart接口、aclprofStop接口之间）调用msproftx API。

接口通过记录应用程序执行期间特定事件发生的时间跨度，写入性能数据文件。

2. 以运行用户登录CANN Toolkit开发套件包和ops算子包所在环境，执行性能数据采集命令，命令示例如下：
**************
```
msprof --msproftx=on /home/projects/MyApp/out/main
```

采集msproftx数据必须传入用户程序。

#### 参数说明
**表1**参数说明
参数

描述

**可选/必选**

--msproftx

控制msproftx用户应用程序和上层框架输出性能数据的开关，可选on或off，默认值为off。

必选

--mstx-domain-include

输出需要的domain数据。用户程序调用前缀为“mstxDomain”的接口，指定domain进行打点时，可选择只输出本参数配置的domain数据。

开关内容填写mstxDomainCreateA接口的“name”。可指定多个domain，使用逗号隔开，default表示默认domain。

需配置--msproftx=on。

与--mstx-domain-exclude参数互斥，不可同时配置。

和--mstx-domain-exclude参数都不配置时，会采集所有domain数据。

若配置了程序中不存在的domain，则采集结果无该数据。

可选

--mstx-domain-exclude

过滤不需要的domain数据。用户程序调用前缀为“mstxDomain”的接口，指定domain进行打点时，可选择不输出本参数配置的domain数据。

开关内容填写mstxDomainCreateA接口的“name”。可指定多个domain，使用逗号隔开，default表示默认domain。

需配置--msproftx=on。

与--mstx-domain-include参数互斥，不可同时配置。

和--mstx-domain-include参数都不配置时，会采集所有domain数据。

可选
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

[配置采集msproftx数据参数后生成的性能数据请参见msproftx数据说明](atlasprofiling_16_0145.html#ZH-CN_TOPIC_0000002504198582)[和db文件的MSTX_EVENTS表](atlasprofiling_16_0142.html#ZH-CN_TOPIC_0000002504358416__zh-cn_topic_0000002534398437_section13564192610142)。
**父主题：**[性能数据采集和自动解析](atlasprofiling_16_0007.html)