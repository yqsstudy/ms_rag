---
title: "性能数据文件分片"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0305.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0305.html"
---

# 性能数据文件分片

性能数据文件分片是对于解析完成的timeline数据文件（.json），系统会识别.json文件在Chrome浏览器（“chrome://tracing”）上打开时间的长短，适当将.json文件切分成合适的数量，以方便用户快速打开。分片操作是在执行性能数据导出时自动启动。

数据文件分片通过msprof_slice.json配置文件配置分片属性，msprof_slice.json配置文件内容及字段说明如下。

```
1
2
3
4
5
```

```
{
  "slice_switch": "off",
  "slice_file_size(MB)": 0,
  "strategy": 0
}

```
|  |  |
| --- | --- |

msprof_slice.json配置文件保存目录为：

${INSTALL_DIR}/tools/profiler/profiler_tool/analysis/msconfig，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。若安装的Ascend-cann-toolkit软件包，以root安装举例，则安装后文件存储路径为：/usr/local/Ascend/ascend-toolkit/latest。
**表1**参数说明
参数

说明

slice_switch

分片开关。取值为：

- on：开启分片。
- off：关闭分片，默认值。

当前分片限制文件最大为20G，如果开启分片功能且文件大小超过20G时文件导出失败，此外，如果开启了分片开关，但是实际文件大小小于200M时，也不会触发分片。

默认情况下关闭数据分片，开启数据分片须编辑msprof_slice.json文件并配置该参数为on，配置为其他值均表示取默认值。

默认情况下，数据分片根据timeline数据文件在Chrome浏览器上打开时间的长短判断分片，打开时间超出上限时，执行分片操作，分片文件大小由slice_file_size参数控制，分片文件数量由strategy参数控制。

[分片后的文件名格式为：模块名_{slice_n}_{timestamp}.json，其中slice_n表示分片的序号，其他字段含义请参见总体说明](atlasprofiling_16_0141.html#ZH-CN_TOPIC_0000002504198580)。

slice_file_size(MB)

分片文件的容量上限。单位为MB，取值范围为大于等于200的正整数，默认情况下，不限制分片文件的大小。

参数配置大于等于200的正整数时，每个分片文件大小不能超过该值；参数配置其他值时，不限制分片文件的大小，仅根据strategy参数限制分片文件数量。

strategy

分片策略。取值为：

- 0：默认值，按照切分次数最少且每个文件打开时间在可接受范围内的标准，对文件进行拆分。
- 1：按照每个文件打开时间缩短为快速打开的标准（切分次数更多），对文件进行拆分。

由于文件打开的时间长短与计算机性能有关，故无法给出准确的打开时间，一般情况下文件打开时间参考值如下：

- 文件打开时间超出上限的参考时间为≥30s。
- 文件打开时间在可接受范围内的参考时间为[10,30)，单位为s。
- 文件打开时间为快速打开的参考时间为(0,10)，单位为s。

具体打开时间请以设备实际情况为准。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
**父主题：**[附录](atlasprofiling_16_0209.html)