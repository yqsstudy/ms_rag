# 性能定位指南文档目录结构

## 整体结构概览

根据文档中的"父主题"关系，文档呈现以下层级结构：

```
性能定位指南
│
├── 文档简介 (toolsample6_001)
│
├── 概述 (toolsample6_002)
│
├── 性能问题的定位流程 (toolsample6_003)
│   └── 问题信息收集 (toolsample6_005)
│
├── 排查思路介绍 (toolsample6_006)
│   └── 性能问题排查 (toolsample6_008)
│
├── 性能工具的使用 (toolsample6_009)
│   └── 服务化工具 (toolsample6_025)
│
├── 模型调优工具 (toolsample6_011)
│   ├── 模型调优性能采集工具 (toolsample6_013)
│   └── 模型调优快速分析 (toolsample6_014)
│
├── 模型调优深入分析（MindStudio Insight） (toolsample6_015)
│
├── 集群性能分析 (toolsample6_018)
│   ├── 通信问题 (toolsample6_019)
│   └── 算子性能问题 (toolsample6_020)
│
├── 单卡性能分析 (toolsample6_021)
│   ├── 下发异常问题 (toolsample6_022)
│   ├── 集群性能问题 (toolsample6_023)
│   └── Atlas 200I/500 A2推理产品场景 (toolsample6_024)
│
├── TopN性能问题的解决方案 (toolsample6_026)
│
├── 通信问题优化方案 (toolsample6_028)
│   ├── 算子优化案例 (toolsample6_044)
│   ├── 下发优化案例 (toolsample6_046)
│   └── 集群优化案例 (toolsample6_047)
│
├── 快慢卡问题定位方法 (toolsample6_030)
│   ├── MindIE服务化调优 (toolsample6_032)
│   ├── 版本升级 (toolsample6_034)
│   └── 版本升级案例 (toolsample6_035)
│
├── 快慢卡案例补充 (toolsample6_036)
│
├── 通信重传 (toolsample6_039)
│
├── 通信小包 (toolsample6_042)
│
├── 算子性能问题优化方案 (toolsample6_048)
│   ├── 服务化优化案例 (toolsample6_050)
│   └── 服务化调优案例 (toolsample6_051)
│
├── Host Bound问题定位及解决方法 (toolsample6_052)
│   ├── 性能分析案例 (toolsample6_054)
│   └── 调优实践案例 (toolsample6_058)
│
├── 编译优化 (toolsample6_062)
│
├── 下发异常分析 (toolsample6_075)
│
├── 服务化性能调优定位案例 (toolsample6_111)
│
└── 版本升级性能劣化定位方法论 (toolsample6_116)
```

## 按主题分类

### 1. 入门概述
| 文档 | 说明 |
|------|------|
| toolsample6_001 | 文档简介 - 整体介绍 |
| toolsample6_002 | 概述 - 性能优化原则和方向 |

### 2. 定位流程
| 文档 | 父主题 | 说明 |
|------|--------|------|
| toolsample6_003 | 无 | 性能问题的定位流程 |
| toolsample6_005 | toolsample6_003 | 问题信息收集 |
| toolsample6_006 | 无 | 排查思路介绍 |
| toolsample6_008 | toolsample6_006 | 性能问题排查 |

### 3. 性能工具
| 文档 | 父主题 | 说明 |
|------|--------|------|
| toolsample6_009 | 无 | 性能工具的使用 |
| toolsample6_011 | 无 | 模型调优工具 |
| toolsample6_013 | toolsample6_011 | 模型调优性能采集工具 |
| toolsample6_014 | toolsample6_011 | 模型调优快速分析 |
| toolsample6_015 | 无 | 模型调优深入分析（MindStudio Insight） |
| toolsample6_025 | toolsample6_009 | 服务化工具 |

### 4. 性能分析
| 文档 | 父主题 | 说明 |
|------|--------|------|
| toolsample6_018 | 无 | 集群性能分析 |
| toolsample6_019 | toolsample6_018 | 通信问题 |
| toolsample6_020 | toolsample6_018 | 算子性能问题 |
| toolsample6_021 | 无 | 单卡性能分析 |
| toolsample6_022 | toolsample6_021 | 下发异常问题 |
| toolsample6_023 | toolsample6_021 | 集群性能问题 |
| toolsample6_024 | toolsample6_021 | Atlas 200I/500 A2推理产品场景 |

### 5. 问题解决方案
| 文档 | 父主题 | 说明 |
|------|--------|------|
| toolsample6_026 | 无 | TopN性能问题的解决方案 |
| toolsample6_028 | 无 | 通信问题优化方案 |
| toolsample6_030 | 无 | 快慢卡问题定位方法 |
| toolsample6_032 | toolsample6_030 | MindIE服务化调优 |
| toolsample6_034 | toolsample6_030 | 版本升级 |
| toolsample6_035 | toolsample6_030 | 版本升级案例 |
| toolsample6_036 | 无 | 快慢卡案例补充 |
| toolsample6_039 | 无 | 通信重传 |
| toolsample6_042 | 无 | 通信小包 |

### 6. 优化案例
| 文档 | 父主题 | 说明 |
|------|--------|------|
| toolsample6_044 | toolsample6_028 | 算子优化案例 |
| toolsample6_046 | toolsample6_028 | 下发优化案例 |
| toolsample6_047 | toolsample6_028 | 集群优化案例 |
| toolsample6_048 | 无 | 算子性能问题优化方案 |
| toolsample6_050 | toolsample6_048 | 服务化优化案例 |
| toolsample6_051 | toolsample6_048 | 服务化调优案例 |
| toolsample6_052 | 无 | Host Bound问题定位及解决方法 |
| toolsample6_054 | toolsample6_052 | 性能分析案例 |
| toolsample6_058 | toolsample6_052 | 调优实践案例 |

### 7. 其他专题
| 文档 | 说明 |
|------|------|
| toolsample6_062 | 编译优化 |
| toolsample6_075 | 下发异常分析 |
| toolsample6_111 | 服务化性能调优定位案例 |
| toolsample6_116 | 版本升级性能劣化定位方法论 |

## 统计信息

- **总文档数**: 41
- **根节点数**: 21（没有父主题的文档）
- **有子节点的文档数**: 10
- **图片数量**: 115

## 说明

文档的父子关系来源于每个文档末尾的"父主题"声明。部分文档的父主题指向自身，这些文档被视为根节点。实际使用时，可以根据文档标题和内容进行逻辑归类。