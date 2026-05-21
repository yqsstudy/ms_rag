---
title: "compile_executable"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0170.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0170.html"
---

# compile_executable

#### 功能说明

编译代码，返回一个可执行的executable对象。

#### 函数原型

```
executable = compile_executable(build_script, src_file)
```

#### 参数说明

参数名

输入/输出

说明

build_script

输入

用于编译被调优应用的脚本文件路径。

数据类型：str。

必选参数。

src_file

输入

代码文件路径。

数据类型：str。

必选参数。

output_bin_path

输入

指定编译生成的可执行文件路径。

数据类型：str。

可选参数，默认值：_gen_executable。

use_cache

输入

开启后不执行编译，加载output_bin_path所指定的文件。

数据类型：bool。

可选参数，默认值：False。
说明：
当使用msDebug工具拉起compile接口时，需配置use_cache=True。

profiling_cmd

输入

预留参数。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 返回值说明

可执行程序对象executable，类型：CompiledExecutable，支持如下方式调用：executable(arg1, arg2, ...)，其中arg1、arg2、...是程序自定义入参。

#### 调用示例

```
executable = compile_executable(build_script, src_file)
executable(a, b, c)
```
**父主题：**[接口列表](atlasopdev_16_0156.html)