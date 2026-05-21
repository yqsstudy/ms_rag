---
title: "compile"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0162.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0162.html"
---

# compile

#### 功能说明

编译Kernel下发代码，返回一个可执行的Kernel对象。

#### 函数原型

```
kernel = compile(build_script, gen_file)
```

#### 参数说明

参数名

输入/输出

说明

build_script

输入

用于模板库Kernel编译的脚本。

数据类型：str。

必选参数。

gen_file

输入

由code_gen接口生成的Kernel下发代码文件路径，一般直接使用code_gen接口返回值。

数据类型：str。

必选参数。

output_bin_path

输入

指定编译生成的可执行文件路径。

数据类型：str。

可选参数，默认值：_gen_module.so。

use_cache

输入

开启后不执行编译，加载output_bin_path所指定的文件。

数据类型：bool。

可选参数，默认值：False。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 返回值说明

可运行的Kernel对象，类型：CompiledKernel，支持如下方式调用kernel：kernel[blockdim](arg1, arg2, ..., timeout=-1, device_id=0, repeat=1)，其中arg1、arg2、...是Kernel的入参。

调用示例

```
kernel = compile(build_script, gen_file)
kernel[blockdim](arg1, arg2, ..., device_id=0)
```
**表1**CompiledKernel可选入参介绍
参数名

输入/输出

说明

device_id

输入

NPU设备ID，设置运行ST测试用例的昇腾AI处理器的ID。

数据类型：int。

若未设置此参数，默认为0。

timeout

输入

camodel仿真场景需要默认设置较长超时时间，设置为-1时表示不限制。

数据类型：int。

单位: ms，默认值为300000。

repeat

输入

重复运行次数，默认值为1。

数据类型：int。

stream

输入

预留参数。

kernel_name

输入

预留参数。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
**父主题：**[接口列表](atlasopdev_16_0156.html)