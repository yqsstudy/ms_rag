---
title: "使用前准备"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0002.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0002.html"
---

# 使用前准备

#### 使用约束

数据dump功能会采集算子输入输出信息，由于可能存在客户敏感信息，请在开发和调测场景下使用该功能，生产上线后建议关闭数据dump开关，避免被攻击者利用，造成安全风险。

- 精度调试工具推荐环境配置：CPU 8核2.6GHz，内存16GB，低于该配置则工具执行迟缓。
- 本文中举例路径均需要确保运行用户具有读或读写权限。
- 出于安全性及权限最小化角度考虑，本工具不应使用root等高权限账户，建议使用普通用户权限执行。
- **本工具依赖CANN软件包，使用本工具前，请先安装CANN软件包，并使用source**命令执行CANN的set_env.sh环境变量文件，为保证安全，source后请勿擅自修改set_env.sh中涉及的环境变量。
- 使用本工具前请确保执行用户的umask值大于等于0027，否则可能会导致工具生成的精度数据文件和目录权限过大。
- 用户须自行保证使用最小权限原则，如给工具输入的文件要求other用户不可写，在一些对安全要求更严格的功能场景下还需确保输入的文件group用户不可写。
- 本工具为开发调测工具，不建议在生产环境使用。
- 单算子网络不支持精度比对。
- [Python版本支持情况请参见《CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0000.html?Mode=PmIns&InstallType=local&OS=openEuler)》。
- 精度比对支持的dump数据类型：
  - FLOAT
  - FLOAT16
  - DT_INT8
  - DT_UINT8
  - DT_INT16
  - DT_UINT16
  - DT_INT32
  - DT_INT64
  - DT_UINT32
  - DT_UINT64
  - DT_BOOL
  - DT_DOUBLE
  - DT_BFLOAT16
**若网络中存在DT_BFLOAT16数据类型，则需要使用pip3 install bfloat16ext**安装依赖。

#### 环境准备

[安装配套版本的CANN Toolkit开发套件包和ops算子包并配置CANN环境变量，具体请参见《CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0000.html?Mode=PmIns&InstallType=local&OS=openEuler)》。

CANN组合包提供进程级环境变量设置脚本，供用户在进程中引用，以自动完成环境变量设置。执行命令参考如下，以下示例均为root或非root用户默认安装路径，请以实际安装路径为准。

```
# 存在多个python3版本时，以指定python3.7.5为例，请根据实际修改
export PATH=/usr/local/python3.7.5/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/python3.7.5/lib:$LD_LIBRARY_PATH
```