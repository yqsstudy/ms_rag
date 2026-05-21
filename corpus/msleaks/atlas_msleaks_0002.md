---
title: "使用前准备"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0002.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0002.html"
---

# 使用前准备

#### 环境准备

[安装配套版本的NPU驱动、固件、CANN Toolkit开发套件包和ops算子包，并配置CANN环境变量，具体请参见《CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0000.html?Mode=PmIns&InstallType=local&OS=openEuler)》。

#### 约束

请在使用工具前，仔细阅读以下安全使用说明，以防范潜在风险。

- 权限约束
  1. 出于安全性及权限最小化考虑，msLeaks工具不建议使用root等高权限用户安装使用，推荐使用普通用户权限。
  2. 遵循最小权限原则（如禁止other用户可写，常见如禁止666、777）。
  3. 请确保执行用户的umask值大于等于0027，否则会导致获取的性能数据所在目录和文件权限过大。
  4. 请确保性能数据保存在当前用户目录下，且该目录不含软链接，以防止可能的安全问题。

- 安装使用约束
  - 由于msLeaks工具是集成在CANN软件包中，安装时应遵循CANN软件包的安装要求。在使用msLeaks工具前，使用同一低权限用户以默认方式安装CANN软件包和Driver包，并设置环境变量，且不得随意修改set_env.sh中环境变量配置。
  - msLeaks为开发调测工具，不应在生产环境中使用。

- 文件校验约束
请对下载的文件（特别是模型权重等文件）使用SHA256等校验方法进行完整性校验，保证文件来源安全可信，从而有效避免潜在的安全风险。

- 兼容性约束
msLeaks工具在生成db格式文件时，需确保当前用户环境中已安装libsqlite3.so包等相关文件，并确保group和others用户组无修改权限。