---
title: "内存对比"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0006.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0006.html"
---

# 内存对比

如果训练推理参数一致，但是CANN和Ascend Extension for PyTorch或MindSpore框架的版本不配套，训练推理任务的两个不同Step的内存使用可能存在差异，会造成内存使用过多，甚至OOM的问题。而msLeaks工具则提供了用户对比分析、定位问题的能力。

#### 工具使用

使用本对比功能之前，需要先采集两个不同Step的数据。

1. 使用环境变量关闭task_queue算子下发队列优化。

```
export TASK_QUEUE_ENABLE=0
```

2. [在训练推理代码中添加mstx打点代码，可参考内存泄漏分析](atlas_msleaks_0005.html#ZH-CN_TOPIC_0000002506468684)。
3. 执行以下命令，使用msLeaks工具采集指定Step的内存数据。需要采集两个不同Step的数据。建议每次只采集一个Step的数据，两个不同Step的数据采集完成后，用来进行Step间内存对比分析。
****
```
msleaks [options] ${Application} --steps=<Required Step> --level=kernel
```

  - [options：命令行参数，具体信息可参见表1](atlas_msleaks_0007.html#ZH-CN_TOPIC_0000002506468682__zh-cn_topic_0000002534400213_table958214912512)。
  - Application：用户程序。
  - --steps：需要采集的Step编号。

4. 执行以下命令，对比采集到的两个Step的内存使用差异。
****
```
msleaks --compare --input=path1,path2 --level=kernel
```

其中--compare和--input参数需同时使用，单独使用无效，同时--input输入的两个文件路径需要逗号（全角半角逗号均可）隔开，--level也可选op。

5. Step间对比生成的结果目录如下。
**
```
|- leaksDumpResults
       |- compare
               |- memory_compare_{timestamp}.csv
```

#### 结果说明

[Step间内存问题可通过输出文件查询定位，输出文件详解可参见输出说明](atlas_msleaks_0016.html#ZH-CN_TOPIC_0000002506628524)。
**父主题：**[内存分析](atlas_msleaks_0004.html)