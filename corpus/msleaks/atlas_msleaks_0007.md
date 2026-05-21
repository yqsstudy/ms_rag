---
title: "命令行采集"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0007.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0007.html"
---

# 命令行采集

可以通过执行以下命令，启动msLeaks工具，采集内存数据。

- 用户不需要使用命令行指定参数
```
msleaks [options] <prog_name> 
```

- 用户需要使用命令行指定参数
  - *方式一（推荐使用此方式）：user*.sh为用户脚本**
```
msleaks [options] bash user.sh
```

  - 方式二
```
msleaks [options] -- <prog_name> [prog_options]
```


  - [环境变量TASK_QUEUE_ENABLE可自行配置，具体配置可参见《Ascend Extension for PyTorch 环境变量参考](https://www.hiascend.com/document/detail/zh/Pytorch/730/comref/Envvariables/docs/zh/environment_variable_reference/env_variable_list.md)[》的“TASK_QUEUE_ENABLE](https://www.hiascend.com/document/detail/zh/Pytorch/730/comref/Envvariables/docs/zh/environment_variable_reference/TASK_QUEUE_ENABLE.md)”章节。
当TASK_QUEUE_ENABLE配置为2时，开启task_queue算子下发队列Level 2优化，此时会采集workspace内存。

  - [msLeaks工具支持在开放态部署场景下采集内存数据，主要采集HAL类型的内存申请和释放事件，安装开放态部署场景，请参见《CANN 软件安装指南 (开放态)](https://www.hiascend.com/document/detail/zh/canncommercial/82RC1/openform/instguide310/instgopen_0002.html)》。
  - 使用root用户运行msLeaks工具时，系统会通过打印提示，跳过文件权限校验，存在安全风险，建议使用普通用户权限安装执行。

**表1**命令行参数说明
参数

说明

options

命令行参数，详细参数参见表2。

prog_name

用户脚本名称，请保证自定义脚本的安全性。

当开启内存对比功能时不需要输入此参数。

prog_options

用户脚本参数，请保证自定义脚本参数的安全性。

当开启内存对比功能时不需要输入此参数。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
**表2**参数说明
参数类别

参数

说明

是否必选

通用参数

--help, -h

输出msLeaks帮助信息。

否

--version, -v

输出msLeaks版本信息。

否

--steps

选择要采集内存信息的Step ID，须配置为实际Step范围内的整数，可配置1个或多个，当前最多支持配置5个。输入的Step ID以逗号（全角半角逗号均可）分割。如果不配置该参数，则默认采集所有Step的内存信息。

示例：--steps=1,2,3。

否

--device

*采集的设备信息。可选项有npu和npu:{id*}，默认值为npu，取值不可为空，可同时选择多个，取值间以逗号（全角半角逗号均可）分隔，示例：--device=npu。

*如果取值中同时包含npu和npu:{id**}，那么默认还是采集所有npu的内存信息，npu:{id*}不生效。

- npu：采集所有的npu内存信息。
- *npu:{id*}：采集指定卡号的npu内存信息，其中id为指定的卡号，需输入有效id，取值范围为[0，31]，可采集多个卡的内存信息，取值间以逗号（全角半角逗号均可）分隔，示例：--device=npu:2,npu:7。

否

--level

采集的算子信息。可选项有0和1，默认值为0，示例：--level=0。

- 0：取值也可写为op，采集op算子的信息。
- 1：取值也可写为kernel，采集kernel算子的信息。

否

--events

采集事件。可选项有alloc、free、launch和access，默认值为alloc，free，launch，取值间以逗号（全角半角逗号均可）分隔。示例：--events=alloc,free,launch。

- alloc：采集内存申请事件。
- free：采集内存释放事件。
- launch：采集算子/kernel下发事件。
- access：采集内存访问事件。当前仅支持采集ATB和Ascend Extension for PyTorch算子场景的内存访问事件。

需要注意的是，当设置--events=alloc时，默认会增加free，实际采集的为alloc和free；当设置--events=free时，默认会增加alloc，实际采集的为alloc和free；当设置--events=access时，默认会增加alloc和free，实际采集的为access、alloc和free。

否

--call-stack

采集调用栈。可选项有python和c，可同时选择，以逗号（全角半角逗号均可）分隔。可设置调用栈的采集深度，在选项后输入数字，选项与数字以英文冒号间隔，表示采集深度，取值范围为[0，1000]，默认值为50，示例：--call-stack=python，--call-stack=c:20,python:10。

- python：采集python调用栈。
- c：采集c调用栈。

否

--collect-mode

内存采集方式。可选项有immediate和deferred，默认值为immediate，取值仅支持选择其一，示例：--collect-mode=immediate。

- immediate：立即采集，即用户脚本开始运行时，就开始采集内存信息，直到用户脚本运行结束；也可配合Python自定义采集接口控制采集范围。
- deferred：自定义采集，需配合Python自定义采集接口使用，等待msleaks.start()脚本执行后，开始采集。
如果仅设置--collect-mode=deferred，不使用Python自定义采集接口时，默认不采集任何数据（除少量系统数据）。

否

--analysis

启用相关内存分析功能。默认值为leaks，如果--analysis参数的取值为空，则不启用任何分析功能；可多选，取值间以逗号（全角半角逗号均可）分隔，示例：--analysis=leaks,decompose。

- leaks：识别内存泄漏事件。
- inefficient：识别低效内存，仅当--events=access,alloc,free,launch时，支持识别ATB LLM和Ascend Extension for PyTorch单算子场景的低效内存。
[低效内存还支持通过离线方式进行识别，可通过API接口进行自定义设置，具体操作可参见API参考](atlas_msleaks_0017.html#ZH-CN_TOPIC_0000002538348383)。

- decompose：开启内存拆解功能。

需要注意的是，当设置--analysis=leaks或--analysis=decompose时，默认会打开--events的alloc和free，即--events=alloc,free。

否

--data-format

输出的文件格式。可选项有db和csv，根据需求选择一种格式，取值不可为空，默认值为csv，示例：--data-format=db。

[当输出文件为db格式时，可使用MindStudio Insight工具展示，请参见《MindStudio Insight工具用户指南》中的“内存调优](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0120.html)”章节。

- db：db格式文件，请确保已安装sqlite依赖。
**执行sqlite3 --version****检查是否安装sqlite依赖，如果未安装，可执行sudo apt-get install sqlite3 libsqlite3-dev**命令安装。

- csv：csv格式文件。

否

--watch

*内存块监测。可选项有start，out{id**}，end和full-content，其中end为必选，可多选，取值间以逗号（全角半角逗号均可）分隔。参数设置格式为：--watch=start:out{id*},end,full-content，示例：--watch=op0,op1,full-content。

- *start：可选，字符串形式，表示一个算子，不同框架下格式不同。当需要设置out{id*}时，start为必选。
- *out{id*}：可选，表示算子的output编号。当Tensor为一个列表时，可以指定需要落盘的Tensor，取值为Tensor在列表中的下标编号。
- end：必选，字符串形式，表示一个算子，不同框架下格式不同。
- full-content：可选，如果选择该值，表示落盘完整的Tensor数据，如果不选，则落盘Tensor对应的哈希值。

否

--output

指定输出件落盘路径，路径最大输入长度为4096。默认的落盘目录为“leaksDumpResults”。

示例：--output=/home/projects/output。

否

--log-level

指定输出日志的级别，可选值有info、warn、error。默认值为warn。

否

内存对比参数

--compare

开启Step间内存数据对比功能。

否

--input

对比文件所在的绝对目录，需输入基线文件和对比文件的目录，以逗号（全角半角逗号均可）分隔，仅在compare功能开启时有效，路径最大输入长度为4096。

示例：--input=/home/projects/input1,/home/projects/input2。

否
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

- 当--events=launch，需要采集Aten算子下发与访问事件时，此时需要满足Ascend Extension for PyTorch框架中的PyTorch版本大于或等于2.3.1，才可使用该功能。
- *当--analysis参数取值包含decompose时，leaks_dump_{timestamp*}.csv文件中Attr参数中会包含显存类别和组件名称。
- 当--analysis参数取值包含decompose时，会开启内存分解功能，当前支持对Ascend Extension for PyTorch框架、MindSpore框架和ATB算子框架的内存池进行分类，但是暂不支持对MindSpore框架和ATB算子框架的内存池进行细分类。在Ascend Extension for PyTorch框架下，可支持对aten、weight、gradient、optimizer_state进行细分类，其中weight、gradient、optimizer_state仅限于PyTorch的训练场景（即调用optimizer.step()接口的场景），aten是aten算子中申请的内存，需要同时满足PyTorch版本大于或等于2.3.1，--level参数取值中包含0，--events参数取值中包含alloc，free，access。
- 当参数--level=1，且使用Hugging Face的tokenizers库时，可能会遇到“当前发生进程fork，并行被禁用”的告警提示。这个告警信息本身不会影响功能，可以选择忽略。如果希望避免这类告警，可执行export TOKENIZERS_PARALLELISM=false来关闭并行的行为。
- 当--collect-mode=deferred，且使用Python自定义采集接口进行采集数据时，Step内内存分析功能不可用，内存块监测、拆解和低效内存识别功能只对采集范围内的数据可用。
**父主题：**[内存采集](atlas_msleaks_0003.html)