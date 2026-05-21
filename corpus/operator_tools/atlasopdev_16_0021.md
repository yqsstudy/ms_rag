---
title: "创建算子工程"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0021.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0021.html"
---

# 创建算子工程

1. 编写算子的原型定义json文件，用于生成算子开发工程。json文件的配置参数详细说明请参考表1。
例如，AddCustom算子的json文件命名为add_custom.json，文件内容如下：
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
```

```
[
    {
        "op": "AddCustom",
        "input_desc": [
            {
                "name": "x",
                "param_type": "required",
                "format": [
                    "ND",
                    "ND",
                    "ND"
                ],
                "type": [
                    "fp16",
                    "float",
                    "int32"
                ]
            },
            {
                "name": "y",
                "param_type": "required",
                "format": [
                    "ND",
                    "ND",
                    "ND"
                ],
                "type": [
                    "fp16",
                    "float",
                    "int32"
                ]
            }
        ],
        "output_desc": [
            {
                "name": "z",
                "param_type": "required",
                "format": [
                    "ND",
                    "ND",
                    "ND"
                ],
                "type": [
                    "fp16",
                    "float",
                    "int32"
                ]
            }
        ]
    }
]

```
|  |  |
| --- | --- |
例如，ReduceMaxCustom算子（包含属性）的json文件命名为reduce_max_custom.json，文件内容如下：
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
```

```
[
    {
        "op": "ReduceMaxCustom",
        "input_desc": [
            {
                "name": "x",
                "param_type": "required",
                "format": ["ND"],
                "type": ["float16"]
            }
        ],
        "output_desc": [
            {
                "name": "y",
                "param_type": "required",
                "format": ["ND"],
                "type": ["float16"]
            },
            {
                "name": "idx",
                "param_type": "required",
                "format": ["ND"],
                "type": ["int32"]
            }
        ],
        "attr": [                                                                   
            {
                "name": "reduceDim",
                "param_type": "required",
                "type": "int"
            },
            {
                "name": "isKeepDim",
                "param_type": "optional",
                "type": "int",
                "default_value": 1
            }
        ]
    }
]

```
|  |  |
| --- | --- |
**表1**json文件配置参数说明
配置字段

类型

含义

是否必选

op

-

字符串

算子的Operator Type。

是

input_desc

-

列表

输入参数描述。

否

name

字符串

算子输入参数的名称。

param_type

字符串

参数类型：

  - required（必选）
  - optional （可选）
  - dynamic（动态输入）

未配置默认为required（必选）。

format

列表

针对类型为Tensor的参数，配置为Tensor支持的数据排布格式。

包含如下取值：

ND、NHWC、NCHW、HWCN、NC1HWC0、FRACTAL_Z等。
说明：
format与type需一一对应。若仅填充其中一项的唯一值，msOpGen工具将会以未填充项的唯一输入值为准自动补充至已填充项的长度。例如用户配置为format:["ND"] /type:["fp16","float","int32"]，msOpGen工具将会以format的唯一输入值（"ND"）为准自动补充至type参数的长度，自动补充后的配置为format:["ND","ND","ND"]/type:["fp16","float","int32"]。

type

列表

算子参数的类型。

  - Ascend C或TBE算子取值范围：float、half、float16 (fp16)、float32 (fp32)、int8、int16、int32、int64、uint8、uint16、uint32、uint64、qint8、qint16、qint32、quint8、quint16、quint32、bool、double、string、resource、complex64、complex128、bf16、numbertype、realnumbertype、quantizedtype、all、BasicType、IndexNumberType、bfloat16。
  - MindSpore数据类型取值范围：None_None、BOOL_None、BOOL_Default、BOOL_5HD、BOOL_FracZ、BOOL_FracNZ、BOOL_C1HWNCoC0、BOOL_NCHW、BOOL_NHWC、BOOL_NDHWC、I8_None、I8_Default、I8_5HD、I8_FracZ、I8_FracNZ、I8_C1HWNCoC0、I8_NCHW、I8_NHWC、I8_HWCN、I8_NDHWC、U8_None、U8_Default、U8_5HD、U8_FracZ、U8_FracNZ、U8_C1HWNCoC0、U8_NCHW、U8_NHWC、U8_HWCN、U8_NDHWC、I16_None、I16_Default、I16_5HD、I16_FracZ、I16_FracNZ、I16_C1HWNCoC0、I16_NCHW、I16_NHWC、I16_HWCN、I16_NDHWC、U16_None、U16_Default、U16_5HD、U16_FracZ、U16_FracNZ、U16_C1HWNCoC0、U16_NCHW、U16_NHWC、U16_HWCN、U16_NDHWC、I32_None、I32_Default、I32_5HD、I32_FracZ、I32_FracNZ、I32_C1HWNCoC0、I32_NCHW、I32_NHWC、I32_HWCN、I32_NDHWC、U32_None、U32_Default、U32_5HD、U32_FracZ、U32_FracNZ、U32_C1HWNCoC0、U32_NCHW、U32_NHWC、U32_HWCN、U32_NDHWC、I64_None、I64_Default、I64_5HD、I64_FracZ、I64_FracNZ、I64_C1HWNCoC0、I64_NCHW、I64_NHWC、I64_HWCN、I64_NDHWC、U64_None、U64_Default、U64_5HD、U64_FracZ、U64_FracNZ、U64_C1HWNCoC0、U64_NCHW、U64_NHWC、U64_HWCN、U64_NDHWC、F16_None、F16_Default、F16_5HD、F16_FracZ、F16_FracNZ、F16_C1HWNCoC0、F16_NCHW、F16_NHWC、F16_HWCN、F16_NDHWCi、F16_FracZNLSTM、F32_None、F32_Default、F32_5HD、F32_FracZ、F32_FracNZ、F32_C1HWNCoC0、F32_NCHW、F32_NHWC、F32_HWCN、F32_NDHWC、F32_FracZNLSTM、F64_None、F64_Default、F64_5HD、F64_FracZ、F64_FracNZ、F64_C1HWNCoC0、F64_NCHW、F64_NHWC、F64_HWCN、F64_NDHWC。
说明：
  - [不同计算操作支持的数据类型不同，详细请参见《Ascend C算子开发接口](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendcopapi/atlasascendc_api_07_0003.html)》。
  - format与type需一一对应。若仅填充其中一项的唯一值，msOpGen工具将会以未填充项的唯一输入值为准自动补充至已填充项的长度。例如用户配置为format:["ND"] /type:["fp16","float","int32"]，msOpGen工具将会以format的唯一输入值（"ND"）为准自动补充至type参数的长度，自动补充后的配置为format:["ND","ND","ND"]/type:["fp16","float","int32"]。

output_desc

-

列表

输出参数描述。

是

name

字符串

算子输出参数的名称。

param_type

字符串

参数类型：

  - required
  - optional
  - dynamic

未配置默认为required。

format

列表

针对类型为Tensor的参数，配置为Tensor支持的数据排布格式。

包含如下取值：

ND、NHWC、NCHW、HWCN、NC1HWC0、FRACTAL_Z等。
说明：
format与type需一一对应。若仅填充其中一项的唯一值，msOpGen工具将会以未填充项的唯一输入值为准自动补充至已填充项的长度。例如用户配置为format:["ND"] /type:["fp16","float","int32"]，msOpGen工具将会以format的唯一输入值（"ND"）为准自动补充至type参数的长度，自动补充后的配置为format:["ND","ND","ND"]/type:["fp16","float","int32"]。

type

列表

算子参数的类型。

  - Ascend C或TBE算子取值范围：float、half、float16 (fp16)、float32 (fp32)、int8、int16、int32、int64、uint8、uint16、uint32、uint64、qint8、qint16、qint32、quint8、quint16、quint32、bool、double、string、resource、complex64、complex128、bf16、numbertype、realnumbertype、quantizedtype、all、BasicType、IndexNumberType、bfloat16。
  - MindSpore数据类型取值范围：None_None、BOOL_None、BOOL_Default、BOOL_5HD、BOOL_FracZ、BOOL_FracNZ、BOOL_C1HWNCoC0、BOOL_NCHW、BOOL_NHWC、BOOL_NDHWC、I8_None、I8_Default、I8_5HD、I8_FracZ、I8_FracNZ、I8_C1HWNCoC0、I8_NCHW、I8_NHWC、I8_HWCN、I8_NDHWC、U8_None、U8_Default、U8_5HD、U8_FracZ、U8_FracNZ、U8_C1HWNCoC0、U8_NCHW、U8_NHWC、U8_HWCN、U8_NDHWC、I16_None、I16_Default、I16_5HD、I16_FracZ、I16_FracNZ、I16_C1HWNCoC0、I16_NCHW、I16_NHWC、I16_HWCN、I16_NDHWC、U16_None、U16_Default、U16_5HD、U16_FracZ、U16_FracNZ、U16_C1HWNCoC0、U16_NCHW、U16_NHWC、U16_HWCN、U16_NDHWC、I32_None、I32_Default、I32_5HD、I32_FracZ、I32_FracNZ、I32_C1HWNCoC0、I32_NCHW、I32_NHWC、I32_HWCN、I32_NDHWC、U32_None、U32_Default、U32_5HD、U32_FracZ、U32_FracNZ、U32_C1HWNCoC0、U32_NCHW、U32_NHWC、U32_HWCN、U32_NDHWC、I64_None、I64_Default、I64_5HD、I64_FracZ、I64_FracNZ、I64_C1HWNCoC0、I64_NCHW、I64_NHWC、I64_HWCN、I64_NDHWC、U64_None、U64_Default、U64_5HD、U64_FracZ、U64_FracNZ、U64_C1HWNCoC0、U64_NCHW、U64_NHWC、U64_HWCN、U64_NDHWC、F16_None、F16_Default、F16_5HD、F16_FracZ、F16_FracNZ、F16_C1HWNCoC0、F16_NCHW、F16_NHWC、F16_HWCN、F16_NDHWCi、F16_FracZNLSTM、F32_None、F32_Default、F32_5HD、F32_FracZ、F32_FracNZ、F32_C1HWNCoC0、F32_NCHW、F32_NHWC、F32_HWCN、F32_NDHWC、F32_FracZNLSTM、F64_None、F64_Default、F64_5HD、F64_FracZ、F64_FracNZ、F64_C1HWNCoC0、F64_NCHW、F64_NHWC、F64_HWCN、F64_NDHWC。
说明：
  - [不同计算操作支持的数据类型不同，详细请参见《Ascend C算子开发接口](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendcopapi/atlasascendc_api_07_0003.html)》。
  - format与type需一一对应。若仅填充其中一项的唯一值，msOpGen工具将会以未填充项的唯一输入值为准自动补充至已填充项的长度。例如用户配置为format:["ND"] /type:["fp16","float","int32"]，msOpGen工具将会以format的唯一输入值（"ND"）为准自动补充至type参数的长度，自动补充后的配置为format:["ND","ND","ND"]/type:["fp16","float","int32"]。

attr

-

列表

属性描述。

否

name

字符串

算子属性参数的名称。

param_type

字符串

参数类型：

  - required
  - optional

未配置默认为required。

type

字符串

算子参数的类型。

包含如下取值：

[int、bool、float、string、list_int、list_float、list_bool、list_list_int，其他请自行参考OpAttrDef《Ascend C算子开发接口](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendcopapi/atlasascendc_api_07_0003.html)》中的“ Host API > 原型注册与管理 > OpAttrDef > OpAttrDef”章节进行修改。

default_value

-

默认值。
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

  - json文件可以配置多个算子，json文件为列表，列表中每一个元素为一个算子。
  - 若input_desc或output_desc中存在相同name参数，则后一个会覆盖前一参数。
  - input_desc，output_desc中的type需按顺序一一对应匹配，format也需按顺序一一对应匹配。
例如，第一个输入x的type配置为[“int8”,“int32”]，第二个输入y的type配置为[“fp16”,“fp32”]，输出z的type配置为[“int32”,“int64”]，最终这个算子支持输入(“int8”,“fp16”)生成int32，或者(“int32”,“fp32”)生成int64，即输入和输出的type是垂直对应的，类型不能交叉。

  - input_desc，output_desc中的type与format需一一对应匹配，数量保持一致。type的数据类型为以下取值（"numbertype"、"realnumbertype"、"quantizedtype"、"BasicType"、"IndexNumberType"、"all"）时，需识别实际的type数量是否与format数量保持一致，若数量不一致，创建工程会收到报错提示，同时format按照type的个数进行补齐，继续生成算子工程。若type的取值为基本数据类型（如：“int32”），且与format无法一一对应时，创建工程会收到报错提示，并停止运行。
  - json文件可对“attr”算子属性进行配置，具体请参考编写原型定义文件。
  - **算子的Operator Type需要采用大驼峰**[的命名方式，即采用大写字符区分不同的语义，具体请参见算子工程编译](atlasopdev_16_0024.html#ZH-CN_TOPIC_0000002504880720__zh-cn_topic_0000002502586626_zh-cn_topic_0000001691887130_li143721718182018)的须知内容。

2. [以生成AddCustom的算子工程为例，执行如下命令，参数说明请参见表2](atlasopdev_16_0018.html#ZH-CN_TOPIC_0000002536920461__zh-cn_topic_0000002534506475_zh-cn_topic_0000001740005677_table20825174505717)。
********
```
msopgen gen -i {*.json} -f {framework type} -c {Compute Resource} -lan cpp -out {Output Path}
```

3. 命令执行完后，会在指定目录下生成算子工程目录，工程中包含算子实现的模板文件，编译脚本等。
*算子工程目录生成在-out所指定的目录下：./output_data，*目录结构如下所示：
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
```

```
output_data
├── build.sh         // 编译入口脚本
├── cmake 
│   ├── config.cmake
│   ├── util        // 算子工程编译所需脚本及公共编译文件存放目录
├── CMakeLists.txt   // 算子工程的CMakeLists.txt
├── CMakePresets.json // 编译配置项
├── framework        // 算子插件实现文件目录，单算子模型文件的生成不依赖算子适配插件，无需关注
├── op_host                      // Host侧实现文件
│   ├── add_custom_tiling.h    // 算子tiling定义文件
│   ├── add_custom.cpp         // 算子原型注册、shape推导、信息库、tiling实现等内容文件
│   ├── CMakeLists.txt
├── op_kernel                   // Kernel侧实现文件
│   ├── CMakeLists.txt   
│   ├── add_custom.cpp        // 算子代码实现文件 
├── scripts                     // 自定义算子工程打包相关脚本所在目录

```
|  |  |
| --- | --- |

4. **可选：**在算子工程中追加算子。若需要在已存在的算子工程目录下追加其他自定义算子，命令行需配置“-m 1”参数。
**********
```
msopgen gen -i json_path/*.json -f tf -c ai_core-{Soc Version} -out ./output_data -m 1
```

  - *-i：指定算子原型定义文件add_custom*.json所在路径。
  - -c：参数中{Soc Version}为昇腾AI处理器的型号。

**在算子工程目录下追加*.json**中的算子。MindSpore算子工程不能够添加非MindSpore框架的算子。

5. [完成算子工程创建，进行算子开发](atlasopdev_16_0023.html#ZH-CN_TOPIC_0000002536920467)。
**父主题：**[算子工程创建（msOpGen）](atlasopdev_16_0017.html)