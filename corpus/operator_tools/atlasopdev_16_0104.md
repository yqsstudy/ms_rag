---
title: "json配置文件说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0104.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0104.html"
---

# json配置文件说明

编写算子的定义json文件，配置参数的具体说明请参考表1和表2。
例如，json配置文件的命名为add_test.json，开发者可基于该模板修改测试数据及其他配置参数。
```
 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
```

```
{
  "kernel_name": "add_custom",
  "kernel_path": "./add_custom.o",
  "blockdim": 8,
  "mode": "ca",
  "device_id": 0,
  "magic": "RT_DEV_BINARY_MAGIC_ELF_AIVEC",
  "test_cases": [
    {
      "case_name": "Test_AddCustom_001",
      "param_desc": [
        {
          "param_type": "input",
          "type": "float16",
          "shape": [
            8,
            2048
          ],
          "data_path": "./input_x.bin",
          "name": "x"
        },
        {
          "param_type": "input",
          "type": "float16",
          "shape": [
            8,
            2048
          ],
          "data_path": "./input_y.bin",
          "name": "y"
        },
        {
          "param_type": "output",
          "type": "float16",
          "shape": [
            8,
            2048
          ],
          "name": "z"
        },
        {
          "param_type": "workspace",
          "user_workspace_size": 4096
        },
        {
          "param_type": "tiling",
          "tiling_data_size": 8,
          "tiling_data_path": "./tiling.bin"
        }
      ]
    }
  ]
}

```
|  |  |
| --- | --- |
**表1**json文件配置参数说明
参数名称

参数描述

类型

是否必选

kernel_name

核函数名称。

string

是

kernel_path

**核函数二进制.o**文件所在路径，可配置为绝对路径或者相对路径。

string

是

blockdim

核函数运行所需的核数，默认值：1。

int

否

mode

测试模式。

- 上板：onboard
- 性能仿真：ca

string

是

device_id

运行时使用昇腾AI处理器的ID，默认值：0。

int

否

tiling_key

当前动态算子的tiling key。
说明：
该参数仅适用于动态算子。

uint64

否

magic
算子类型。
- Cube算子：RT_DEV_BINARY_MAGIC_ELF_AICUBE
- Vector算子：RT_DEV_BINARY_MAGIC_ELF_AIVEC
- Mix融合算子：RT_DEV_BINARY_MAGIC_ELF（仅Atlas A3 训练系列产品/Atlas A3 推理系列产品和Atlas A2 训练系列产品/Atlas A2 推理系列产品支持配置）
说明：
Atlas 推理系列产品需配置为RT_DEV_BINARY_MAGIC_ELF。

string

是

test_cases

测试数据，支持列表，每个元素包含一个用例。详细说明可参考表2。
说明：
算子上板或仿真调优时仅支持配置单个用例。

map

是
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
**表2**test_case参数字段说明
参数

说明

类型

是否必选

case_name

-

-

测试用例的名称，需唯一。

string

是

param_desc

-

-

用例描述，支持列表，每个元素代表一个核函数参数。

list

是

-

param_type

input/output/workspace/tiling/fftsAddr

参数类型。

string

是

-

type

-

输入输出数据支持的数据类型，例如：uint8、int16、int32、float16、float32、float等。
说明：
当“param_type”为input、output时必选。

string

否

-

shape

-

输入输出Tensor支持的形状，所有输入输出Tensor需支持相同数量的形状。

例如：[8, 3, 256, 256]。

若输入非法的形状会报错，例如：[0]。
说明：
当“param_type”为input、output时必选。

list

否

-

data_path

-

输入数据bin文件的路径。
说明：
- 当“param_type”为input时必须输入data_path或value_range，且data_path优先级更高。
- [若json文件的"data_path"字段为空，需将json文件中设置为"data_path":"null"。json文件具体内容请参见json配置文件说明](atlasopdev_16_0104.html#ZH-CN_TOPIC_0000002536920583)。

string

否

-

name

-

参数名称，需唯一。
说明：
当“param_type”为input、output时必选。

string

否

-

user_workspace_size

-

用户设置的workspace_size大小。
说明：
当“param_type”为workspace时必选。

int

否

-

tiling_data_size

-

tiling数据大小。
说明：
当“param_type”为tiling时必选。

int

否

-

tiling_data_path

-

tiling数据bin文件所在路径。
说明：
当“param_type”为tiling时必选。

string

否

-

data_size

-

fftsAddr的data_size大小。
说明：
当“param_type”为fftsAddr时必选。

int

否
|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

- “output”中参数取值的个数都要与“input”一致，否则测试用例生成会失败。
例如：“input”的type支持的类型个数为2，则“output”的type支持的类型个数也需要为2。

同理，所有input和output中的type、shape和value_range的取值个数也需要保持一致。

- 一个算子所有“input”中参数取值的个数都要一致，否则测试用例生成会失败。
所有“input”中的type、shape和value_range的取值个数也需要保持一致。

**父主题：**[算子调优（msProf）](atlasopdev_16_0081.html)