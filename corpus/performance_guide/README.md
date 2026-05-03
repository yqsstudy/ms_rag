# 性能定位指南语料库

本目录包含从昇腾社区网站获取的性能定位指南文档，用于RAG系统。

## 文档来源

- 来源网站: [昇腾社区 - MindStudio 8.3.0 开发文档](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_001.html?framework=pytorch)
- 采集日期: 2026-04-29

## 文档结构

### 1. 文档简介与概述
| 文件 | 标题 |
|------|------|
| [toolsample6_001.md](toolsample6_001.md) | 文档简介 |
| [toolsample6_002.md](toolsample6_002.md) | 概述 |

### 2. 性能问题定位流程
| 文件 | 标题 |
|------|------|
| [toolsample6_003.md](toolsample6_003.md) | 性能问题的定位流程 |
| [toolsample6_005.md](toolsample6_005.md) | 问题信息收集 |
| [toolsample6_006.md](toolsample6_006.md) | 排查思路介绍 |
| [toolsample6_008.md](toolsample6_008.md) | 性能问题排查 |

### 3. 性能工具使用
| 文件 | 标题 |
|------|------|
| [toolsample6_009.md](toolsample6_009.md) | 性能工具的使用 |
| [toolsample6_011.md](toolsample6_011.md) | 性能工具介绍 |
| [toolsample6_013.md](toolsample6_013.md) | 模型调优性能采集工具 |
| [toolsample6_014.md](toolsample6_014.md) | 模型调优快速分析 |
| [toolsample6_015.md](toolsample6_015.md) | 模型调优深入分析 |

### 4. 集群性能分析
| 文件 | 标题 |
|------|------|
| [toolsample6_018.md](toolsample6_018.md) | 集群性能分析 |
| [toolsample6_019.md](toolsample6_019.md) | 通信问题 |

### 5. TopN性能问题解决方案
| 文件 | 标题 |
|------|------|
| [toolsample6_020.md](toolsample6_020.md) | 算子性能问题 |
| [toolsample6_021.md](toolsample6_021.md) | 算子性能问题案例 |
| [toolsample6_022.md](toolsample6_022.md) | 下发异常问题 |
| [toolsample6_023.md](toolsample6_023.md) | 集群性能问题 |
| [toolsample6_024.md](toolsample6_024.md) | Atlas 200I/500 A2推理产品场景 |
| [toolsample6_026.md](toolsample6_026.md) | TopN性能问题的解决方案 |
| [toolsample6_028.md](toolsample6_028.md) | MindIE推理场景 |
| [toolsample6_030.md](toolsample6_030.md) | MindIE推理调优 |
| [toolsample6_032.md](toolsample6_032.md) | MindIE服务化调优 |
| [toolsample6_034.md](toolsample6_034.md) | 版本升级 |

### 6. 优化案例
| 文件 | 标题 |
|------|------|
| [toolsample6_035.md](toolsample6_035.md) | 版本升级案例 |
| [toolsample6_036.md](toolsample6_036.md) | 版本升级实践 |
| [toolsample6_039.md](toolsample6_039.md) | 通信优化案例 |
| [toolsample6_042.md](toolsample6_042.md) | 性能优化实践 |
| [toolsample6_044.md](toolsample6_044.md) | 算子优化案例 |
| [toolsample6_046.md](toolsample6_046.md) | 下发优化案例 |
| [toolsample6_047.md](toolsample6_047.md) | 集群优化案例 |
| [toolsample6_048.md](toolsample6_048.md) | 推理优化案例 |
| [toolsample6_050.md](toolsample6_050.md) | 服务化优化案例 |
| [toolsample6_051.md](toolsample6_051.md) | 服务化调优案例 |
| [toolsample6_052.md](toolsample6_052.md) | 性能问题案例 |
| [toolsample6_054.md](toolsample6_054.md) | 性能分析案例 |
| [toolsample6_058.md](toolsample6_058.md) | 调优实践案例 |
| [toolsample6_062.md](toolsample6_062.md) | 性能诊断案例 |
| [toolsample6_075.md](toolsample6_075.md) | 高级调优案例 |
| [toolsample6_111.md](toolsample6_111.md) | 性能优化案例 |
| [toolsample6_116.md](toolsample6_116.md) | 其他案例 |

### 7. 服务化工具
| 文件 | 标题 |
|------|------|
| [toolsample6_025.md](toolsample6_025.md) | 服务化工具 |

## 资源统计

- **文档数量**: 41 个 Markdown 文件
- **图片数量**: 115 张图片
- **总大小**: 约 22MB

## 图片目录

所有图片保存在 `images/` 目录下，文档中的图片链接已转换为本地相对路径。

## 使用说明

1. 每个Markdown文件包含YAML前置信息，记录了标题、来源URL和采集日期
2. 文档保留了原始链接，指向昇腾社区的相关页面
3. 图片已下载到本地，可在离线环境下使用

## 爬虫脚本

爬虫脚本位于项目根目录: `fetch_performance_guide.py`

可重新运行以更新文档内容。
