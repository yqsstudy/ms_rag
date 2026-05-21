---
title: "工具概述"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0039.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0039.html"
---

# 工具概述

[异常检测工具（msSanitizer，MindStudio Sanitizer）是一种基于昇腾AI处理器的工具，包含了单算子开发场景下的内存检测、竞争检测、未初始化检测和同步检测四个子功能。用户使用msOpST工具](atlasopdev_16_0028.html#ZH-CN_TOPIC_0000002504880724)在真实的硬件环境中对算子的功能进行测试后，可根据实际测试情况选择是否使用msSanitizer工具进行异常检测。

- 内存检测：工具可以在用户开发算子的过程中，协助定位非法读写、多核踩踏、非对齐访问、内存泄漏以及非法释放等内存问题。同时工具也支持对CANN软件栈的内存检测，帮助用户定界软件栈内存异常发生的模块。
- 竞争检测：工具可以协助用户定位由于竞争风险可能导致的数据竞争问题，包含核内竞争和核间竞争问题。其中，核内竞争包含流水间竞争和流水内竞争。
- 未初始化检测：工具可以协助用户定位由于内存未初始化可能导致的脏数据读取问题。
- 同步检测：工具可以协助用户定位由于前序算子中的未配对同步指令导致的后续算子同步失败的问题。

msSanitizer工具不支持对多线程算子及使用了掩码的向量类计算指令进行检测。

#### 工具特性

msSanitizer通过不同子功能提供了不同类型的异常检测功能，目前已支持的功能如下：
**表1**msSanitizer工具功能
使用场景

使用说明

使用示例

算子内存检测

[内存检测](atlasopdev_16_0042.html#ZH-CN_TOPIC_0000002536920491)

[msSanitizer支持内核调用符调用的Ascend C算子（包括Vector、Cube算子和Mix融合算子）内存和竞争的检测，可参考内存检测](atlasopdev_16_0042.html#ZH-CN_TOPIC_0000002536920491)。

算子竞争检测

[竞争检测](atlasopdev_16_0043.html#ZH-CN_TOPIC_0000002504880738)

[msSanitizer支持对单算子API调用的Ascend C算子（包括Vector、Cube算子和Mix融合算子）内存和竞争的检测，可参考竞争检测](atlasopdev_16_0043.html#ZH-CN_TOPIC_0000002504880738)。

算子未初始化检测

[未初始化检测](atlasopdev_16_0128.html#ZH-CN_TOPIC_0000002505040566)

[msSanitizer支持Ascend CL调用的Ascend C算子（包括Vector、Cube算子和Mix融合算子）未初始化的检测，可参考未初始化检测](atlasopdev_16_0128.html#ZH-CN_TOPIC_0000002505040566)。

同步检测

[同步检测](atlasopdev_16_0181.html#ZH-CN_TOPIC_0000002536800527)

[msSanitizer支持内核调用符或单算子API调用的Ascend C算子（包括Vector、Cube算子和Mix融合算子）同步指令配对情况的检测，可参考同步检测](atlasopdev_16_0181.html#ZH-CN_TOPIC_0000002536800527)。

CANN软件栈的内存检测

[内存检测](atlasopdev_16_0042.html#ZH-CN_TOPIC_0000002536920491)

[支持CANN软件栈内存检测，详细可参考检测CANN软件栈的内存](atlasopdev_16_0047.html#ZH-CN_TOPIC_0000002505040574)。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 命令汇总

可以通过运行以下命令来调用msSanitizer工具。
********************
```
mssanitizer <options> -- <user_program> <user_options>   
```

- options为检测工具的命令行选项，详细的参数选项及其默认值，请参考表2和表3*，user_program为用户算子程序，user_options为用户程序的命令行选项。*
- *如要加载的可执行文件或用户自定义程序本身带有命令行参数时，在可执行文件或用户程序（application*）之前使用“--”分隔检测工具和用户命令。****
```
mssanitizer -- application parameter1 parameter2 ...
```

- 用户需保证可执行文件及用户自定义程序的安全性。
- *用户需自行保证可执行文件或用户程序（application*）执行的安全性。
  - *建议限制对可执行文件或用户程序（application*）的操作权限，避免提权风险。
  - 不建议进行高危操作（删除文件、删除目录、修改密码及提权命令等），避免安全风险。

**表2**通用参数说明
参数名称

参数描述

参数取值

是否必选

-v，--version

查询msSanitizer工具版本。

-

否

-t，--tool

指定异常检测的子工具。

- memcheck：内存检测（默认）
- racecheck：竞争检测
- initcheck：未初始化检测
- synccheck：同步检测

否

--log-file

指定检测报告输出到文件。

*{file_name}*，如配置为test_log。
说明：
- 仅支持数字、大小写字母和- . / _四种符号。
- 为避免日志泄漏风险，建议限制该文件权限，确保只有授权人员才能访问该文件。
- 工具会以覆盖的方式将报告输出到test_log文件。若test_log文件中已有内容，这些内容将会被清空。因此，建议指定一个空文件用于输出报告。

否

--log-level

指定检测报告输出等级。

- info：输出info/warn/error级别的运行信息。
- warn：输出warn/error级别的运行信息（默认）。
- error：输出error级别的运行信息。

否

--max-debuglog-size

指定检测工具调试输出日志中单个文件大小的上限。

可设定范围为1~10240之间的整数，单位为MB。

默认值为1024。
说明：
--max-debuglog-size=100就表示单个调试日志的大小上限为100MB。

否

--block-id

是否启用单block检测功能。

可设定范围为0~200之间的整数。

启用前

- 内存检测、未初始化检测和同步检测：默认检测所有block。
- 竞争检测：核间默认检测所有block，核内默认检测block 0的流水内及流水间的竞争。

启用后

- 内存检测、未初始化检测和同步检测：检测指定block。
- 竞争检测：核间不进行检测，检测指定block的流水内及流水间的竞争。

否

--cache-size

表示单block的GM内存大小。

单block可设定范围为1~8192之间的整数，单位为MB。

单block默认值为100MB，表示单block可申请100MB的内存大小。
说明：
- 启用单block检测时，--cache-size的最大值为8192MB。不启用单block检测时，--cache-size可设置的最大值为(24*1024 / block数量) 。
- [当--cache-size值不满足需求时，异常检测工具将会打印信息提示用户重新设置--cache-size值，具体请参见msSanitizer工具提示--cache-size异常](atlasopdev_16_0138.html#ZH-CN_TOPIC_0000002505040578)。

否

--kernel-name

指定要检测的算子名称。

支持使用算子名中的部分字符串来进行模糊匹配。如果不指定，则系统默认会对整个程序执行期间所调度的所有算子进行检测。

例如，需要同时检测名为"abcd"和"bcd"的算子时，可以通过配置--kernel-name="bc"来实现这一需求，系统会自动识别并检测所有包含"bc"字符串的算子。

否

-h，--help

输出帮助信息。

-

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
**表3**内存检测参数说明
参数名称

参数描述

参数取值

是否必选

--check-unused-memory

使能分配内存未使用检测。

- yes
- no（默认）

否

--leak-check

使能内存泄漏检测。

- yes
- no（默认）

否

--check-device-heap

使能Device侧内存检测。

- yes
- no（默认）

否

--check-cann-heap

使能CANN软件栈内存检测。

- yes
- no（默认）

否
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

- --check-device-heap或--check-cann-heap使能后，将不会对Kernel内进行检测。
- Device侧内存检测和CANN软件栈内存检测不能同时使能，若同时使能会提示“CANNOT enable both --check-cann-heap and --check-device-heap”。
- 使用msSanitizer工具提供的API头文件重新编译的待检测程序只能用于Ascend CL系列接口的泄漏检测，无法用于Device接口的检测。

#### 异常检测功能启用原则

异常检测工具提供内存检测（memcheck）、竞争检测（racecheck）、未初始化检测（initcheck）和同步检测（synccheck）四种检测功能，多种检测功能可以组合开启，组合启用检测功能需满足以下原则：

- 多个检测功能可通过多次指定--tool参数同时开启。如执行以下命令可同时开启内存检测和竞争检测：
```
mssanitizer -t memcheck -t racecheck ./application
```

- 若开启了检测功能对应的子选项，则对应的检测功能也会被默认开启。如开启了内存检测对应的泄漏检测子选项，则内存检测功能会被自动开启：
```
mssanitizer -t racecheck --leak-check=yes ./application
```
以上命令等价于：
```
mssanitizer -t racecheck -t memcheck --leak-check=yes ./application
```

- 若不指定任何检测功能，则默认启用内存检测：
```
mssanitizer ./application
```

以上命令等价于：

```
mssanitizer -t memcheck ./application
```

#### 调用场景

支持如下调用算子的场景：

- Kernel直调算子开发：Kernel直调。
  - [Kernel直调场景，详细信息可参考Kernel直调。具体操作请参见检测内核调用符方式的Ascend C算子](atlasopdev_16_0045.html#ZH-CN_TOPIC_0000002505040570)。
  - 在<<<>>>自定义算子接入torch场景时，默认使用内存池的方式管理GM内存，可能会导致越界检测结果不准确。因此，在检测前需要额外设置如下环境变量关闭内存池，从而获得更精确的检测结果。****
```
export PYTORCH_NO_NPU_MEMORY_CACHING=1
```

- 工程化算子开发：单算子API调用。
  - [单算子API调用场景，详细信息可参考单算子API调用](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_10_0070.html)[。具体操作请参见检测API调用的单算子](atlasopdev_16_0046.html#ZH-CN_TOPIC_0000002536800533)。
  - 在调用含有aclnn前缀的API时，需执行以下命令，通过aclInit接口传入acl.json文件以保证内存检测的准确性。
```
auto ret = aclInit("./acl.json"); // acl.json文件内容为{"dump":{"dump_scene":"lite_exception"}}
```

- AI框架算子适配：PyTorch框架。
  - [PyTorch图模式（TorchAir）下，仅支持在msSanitizer工具不添加编译选项的情况下进行检测，具体请参见配置编译选项（可选）](atlasopdev_16_0040.html#ZH-CN_TOPIC_0000002536800523__zh-cn_topic_0000002534506457_section1819973616410)。
  - [PyTorch图模式（TorchAir）下，支持Ascend IR图执行模式和aclgraph图执行模式，具体请参见《Ascend Extension for PyTorch 套件与三方库支持清单](https://www.hiascend.com/document/detail/zh/Pytorch/730/modthirdparty/modparts/thirdpart_0003.html)[》中的“reduce-overhead模式功能 > reduce-overhead模式配置](https://www.hiascend.com/document/detail/zh/Pytorch/730/modthirdparty/torchairuseguide/torchair_00021.html)”章节。
  - [PyTorch框架调用场景，详细信息可参考《Ascend Extension for PyTorch 框架特性指南](https://www.hiascend.com/document/detail/zh/Pytorch/730/ptmoddevg/Frameworkfeatures/docs/zh/framework_feature_guide_pytorch/overview.md)[》中的“基于OpPlugin算子适配开发](https://www.hiascend.com/document/detail/zh/Pytorch/730/ptmoddevg/Frameworkfeatures/docs/zh/framework_feature_guide_pytorch/adaptation_description_opplugin.md)[”章节。具体操作请参见检测PyTorch接口调用的算子](atlasopdev_16_0136.html#ZH-CN_TOPIC_0000002536920503)。

- Triton算子开发：Triton算子调用。
  - [Triton算子调用场景，详细信息可参考检测Triton算子](atlasopdev_16_0176.html#ZH-CN_TOPIC_0000002504880746)。
  - [已完成Triton及Triton-Ascend插件的安装和配置，具体操作请参见Link](https://gitcode.com/Ascend/triton-ascend)。
  - Triton算子调用场景不适用于Atlas 推理系列产品。
  - 为了防止未重新编译的算子造成影响，建议您启用以下环境变量：
```
export TRITON_ALWAYS_COMPILE=1
```

  - Triton场景会使用PyTorch创建Tensor，PyTorch框架内默认使用内存池的方式管理GM内存，会对内存检测产生干扰。因此，在检测前需要额外设置如下环境变量关闭内存池，以保证检测结果准确。
```
1
```

```
export PYTORCH_NO_NPU_MEMORY_CACHING=1

```
|  |  |
| --- | --- |

#### 结果件说明

结果件名称

说明

*mssanitizer_{TIMESTAMP}**_{PID*}.log

*msSanitizer工具运行过程中，在mindstudio_sanitizer_log目录下生成的工具日志，TIMESTAMP**为当前时间戳，PID**为当前检测工具的PID*。

*kernel.{PID*}.o

*msSanitizer工具运行过程中，会在当前路径下生成的算子缓存文件。其中，PID**为当前使用的检测工具的PID*，该算子缓存文件用于解析异常调用栈。

- 正常情况下，msSanitizer工具退出时会自动清理该算子缓存文件。
- 当msSanitizer工具异常退出（如被用户“CTRL+C”中止）时，该算子缓存文件会保留在文件系统中。因为该算子缓存文件包含算子的调试信息，建议限制其他用户对此文件的访问权限，并在检测工具运行完成后及时删除。

*tmp_{PID**}_{TIMESTAMP*}

msSanitizer工具运行过程中，会在当前路径下生成的临时文件夹。其中，PID为当前使用的检测工具的PID，TIMESTAMP为当前时间戳，该文件夹用于生成算子Kernel二进制。

- 正常情况下，msSanitizer工具退出时会自动清理该文件夹。
- 当通过环境变量export INJ_LOG_LEVEL=0开启DEBUG等级日志，或工具异常退出（如被用户“CTRL+C”中止）时，该文件夹会保留在文件系统中，方便用户调测使用。因为该文件夹包含算子的调试信息，建议限制其他用户对此文件的访问权限，并在调测完成后及时删除。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
**父主题：**[异常检测（msSanitizer）](atlasopdev_16_0038.html)