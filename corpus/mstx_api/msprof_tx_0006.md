---
title: "mstxDomainCreateA"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0006.html"
date_collected: "2026-05-04"
category: "mstx_api"
original_path: "zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0006.html"
---

# mstxDomainCreateA

#### 产品支持情况

产品

是否支持

Atlas A3 训练系列产品/Atlas A3 推理系列产品

√

Atlas A2 训练系列产品/Atlas A2 推理系列产品

√

Atlas 200I/500 A2 推理产品

√

Atlas 推理系列产品

√

Atlas 训练系列产品

√
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### 功能说明

创建自定义的mstx域。

**domain（域）**：用于对打点数据进行划分，便于用户自定义管理打点数据，不指定domain的打点数据均属于默认域（域名：default）。默认情况下，所有打点数据均属于默认域。

#### 函数原型

```
1
```

```
mstxDomainHandle_t mstxDomainCreateA(const char* name)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

name

输入

要创建的域的名称。

- 数据类型：const char *。
- 默认域名为globalDomain。
- 最大长度为1023字节，仅支持数字、大小写字母和_符号。
- MSPTI场景：不能超过255字节。
- 非MSPTI场景（例如msprof命令行、Ascend PyTorch Profiler）：不能超过1024字节。
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 返回值

返回有效的domain句柄，表示接口执行成功；返回nullptr，表示接口执行失败。

#### 调用示例

```
mstxDomainHandle_t domain = mstxDomainCreateA("sample")
```