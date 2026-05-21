---
title: "信息收集"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_085.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_085.html"
---

# 信息收集

本文以Atlas 200I A2 加速模块为例，分析使用Atlas 200I A2推理场景通常需要收集如下信息。

#### Profiling信息收集

[Profiling数据采集操作详情可参见《性能调优工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0001.html)[》的“msprof采集通用命令](https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0008.html)章节。

1. 登录运行环境，进入msprof工具所在目录“/var”。
2. 执行如下命令，采集性能数据。其中application为用户程序。
****
```
msprof --output={path} {application}
```

命令示例：

```
msprof --output=$[HOME]/profiling_output $[HOME]/HIAI_PROJECTS/MyAppname/out/main
```

3. 命令执行完成后，在--output指定的目录下生成PROF_XXX目录，目录结构如下。

```
├── device_{id}
│├──data
│└──...
└──host
│├──data
│└──...
```

4. 将PROF_XXX目录上传到安装toolkit包的开发环境，执行以下命令进行数据解析。

```
msprof --export=on --output=<dir>
```

PROF_XXX目录下会新增数据文件，目录结构如下：

```
├── device_{id}
│├──data
├──host
│├──data
│└──...
└──mindstudio_profiler_output
│├──xx_*.csv
│├──xx_*.json
│└──...
...
```

#### ONNX通过ATC转换OM的日志收集

设置转换ONNX文件时的日志级别，并将日志的输出定向到文件，分析该问题，步骤如下：

1. 配置ATC运行环境变量。

```
export ASCEND_SLOG_PRINT_TO_STDOUT=1
export ASCEND_GLOBAL_LOG_LEVEL=0
```

2. ATC命令加上--log=debug，收集转换日志。

命令示例：
****
```
atc --model=$modelPath/$onnxfile \
--log=debug \
--framework=5  \
--input_shape="x:$batchsize,3,$height,$width" \
--input_fp16_nodes="x" \
--output_type=FP16 \
--op_select_implmode=high_precision \
--output=$outputPath/$outname  \
--soc_version=Ascendxxxyy \  # xxxyy为用户实际使用的具体芯片类型
```

3. 重新执行ATC，将输出的信息重定向到一个日志文本文件连同ATC执行产生的fusion_result.jsonl一并获取，用于后续的性能分析。

#### 收集推理日志

执行OM文件进行推理，收集推理输出的日志，采集步骤如下：

1. 配置OM模型运行环境变量。

```
export ASCEND_SLOG_PRINT_TO_STDOUT=1
export ASCEND_GLOBAL_LOG_LEVEL=1
```

2. 然后执行OM文件，将输出的信息重定向到一个日志文本文件。

#### 返回ATC转换前后的ONNX文件和OM文件

ONNX是业内目前比较主流的模型格式，广泛用于模型交流及部署，离线推理需要将ONNX文件转换为OM文件来进行推理。

需要将训练环境模型运行导出的ONNX文件和转换产生的OM文件一并采集，用于后续分析。
**父主题：**[ONNX离线推理场景解决方案](toolsample6_084.html)