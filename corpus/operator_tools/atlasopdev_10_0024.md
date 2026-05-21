---
title: "基于msOpGen工具创建算子工程"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_10_0024.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_10_0024.html"
---

# 基于msOpGen工具创建算子工程

#### 功能描述

CANN开发套件包中提供了自定义算子工程生成工具msOpGen，可基于算子原型定义输出算子开发相关交付件，包括算子代码实现文件、算子适配插件、算子原型定义、算子信息库定义以及工程编译配置文件。

若开发者需要自定义多个AI CPU算子，需要在同一算子工程中进行实现，并将所有自定义算子在同一工程中同时进行编译，将所有AI CPU自定义算子的实现文件编译成一个动态库文件。

#### 使用前提

- 
CANN组合包提供进程级环境变量设置脚本，供用户在进程中引用，以自动完成环境变量设置。执行命令参考如下，以下示例均为root或非root用户默认安装路径，请以实际安装路径为准。

```
# 以root用户安装toolkit包后配置环境变量
source /usr/local/Ascend/cann/set_env.sh 
# 以非root用户安装toolkit包后配置环境变量
source ${HOME}/Ascend/cann/set_env.sh 
```

- 安装依赖：**如下命令如果使用非root用户安装，需要在安装命令后加上--user。**
```
pip3 install xlrd==1.2.0
```

#### 使用方法

1. 确认需要的输入文件。
自定义算子工程生成工具支持输入三种类型的原型定义文件创建算子工程，分别为：
  - 适配昇腾AI处理器算子IR定义文件（.json）
  - TensorFlow的原型定义文件（.txt）
TensorFlow的原型定义文件可用于生成TensorFlow、Caffe、PyTorch框架的算子工程。

  - 适配昇腾AI处理器算子IR定义文件（.xlsx）

2. 请用户选择一种文件完成输入文件的准备工作。

  - 适配昇腾AI处理器算子IR定义的json文件的准备工作用户可从CANN软件安装后文件存储路径下的“python/site-packages/op_gen/json_template”中获取模板文件IR_json.json，并进行修改，其文件参数配置说明请参见表1。**表1**json文件配置参数说明
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

    - required
    - optional
    - dynamic

未配置默认为required。

format

列表

[针对类型为Tensor的参数，配置为Tensor支持的数据排布格式，具体请参考《Ascend C算子开发指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_map_10_0002.html)[》中的数据排布格式](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_10_0099.html)章节。

包含如下取值：

ND,NHWC,NCHW,HWCN,NC1HWC0,FRACTAL_Z等。

format与type的数量需保持一致。

type

列表

算子参数的类型。

取值范围：float16（fp16）, float32（fp32）, int8, int16, int32, uint8, uint16, bfloat16（bf16）, bool等。
说明：
[不同计算操作支持的数据类型不同，详细请参见《TBE&AI CPU算子开发接口](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/aicpuopapi/opdevapi_07_0000.html)》。

format与type的数量需保持一致。

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

[针对类型为Tensor的参数，配置为Tensor支持的数据排布格式，具体请参考《Ascend C算子开发指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_map_10_0002.html)[》中的数据排布格式](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_10_0099.html)章节。包含如下取值：

ND,NHWC,NCHW,HWCN,NC1HWC0,FRACTAL_Z等。

format与type的数量需保持一致。

type

列表

算子参数的类型。

取值范围：float16（fp16）, float32（fp32）, int8, int16, int32, uint8, uint16, bfloat16（bf16）, bool等。
说明：
[不同计算操作支持的数据类型不同，详细请参见《TBE&AI CPU算子开发接口](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/aicpuopapi/opdevapi_07_0000.html)》。format与type的数量需保持一致。

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

int、bool、float、string、list_int、list_float等。

default_value

-

默认值
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
    - 若input_desc或output_desc中的name参数相同，则后一个会覆盖前一参数。
    - input_desc，output_desc中的type需按顺序一一对应匹配，format也需按顺序一一对应匹配。
例如，第一个输入x的type配置为[“int8”,“int32”]，第二个输入y的type配置为[“fp16”,“fp32”]，输出z的type配置为[“int32”,“int64”]，最终这个算子支持输入(“int8”,“fp16”)生成int32，或者(“int32”,“fp32”)生成int64，即输入和输出的type是垂直对应的，类型不能交叉。

    - input_desc，output_desc中的type与format需一一对应匹配，数量保持一致。type的数据类型为以下取值（"numbertype"、"realnumbertype"、"quantizedtype"、"BasicType"、"IndexNumberType"、"all"）时，需识别实际的type数量是否与format数量保持一致，若数量不一致，创建工程会收到报错提示，同时format按照type的个数进行补齐，继续生成算子工程。若type的取值为基本数据类型（如：“int32”），且与format无法一一对应时，创建工程会收到报错提示，并停止运行。

  - TensorFlow的原型定义文件（.txt）的准备工作
[TensorFlow的原型定义文件（.txt）中内容可从TensorFlow开源社区](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/core/ops)[获取，例如，Add算子](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/core/ops/math_ops.cc)的原型定义在TensorFlow开源社区中/tensorflow/core/ops/math_ops.cc文件中，在文件中搜索“Add”找到Add对应的原型定义，内容如下所示：

```
REGISTER_OP("Add")
    .Input("x: T")
    .Input("y: T")
    .Output("z: T")
    .Attr(
        "T: {half, float, int32}")
    .SetShapeFn(shape_inference::BroadcastBinaryOpShapeFn);
```

将以上内容另存为**.txt文件。

每个**.txt文件仅能包含一个算子的原型定义。

自定义算子工程生成工具只解析算子类型、Input、Output、Attr中内容，其他内容可以不保存在**.txt中。

  - 适配昇腾AI处理器算子IR定义的Excel文件准备工作
用户可从CANN软件安装后文件存储路径下的“toolkit/tools/msopgen/template”目录下获取模板文件Ascend_IR_Template.xlsx进行修改。请基于“Op”页签进行修改，“Op”页签可以定义多个算子，每个算子都包含如下参数：
**表2**IR原型定义参数说明
列名称

含义

是否必选

Op

算子的Operator Type。

是

Classify
算子相关参数的类别，包含：
    - 输入：Input
    - 动态输入：DYNAMIC_INPUT
    - 输出：Output
    - 动态输出：DYNAMIC_OUTPUT
    - 属性：Attr

是

Name

算子参数的名称。

是

Type

算子参数的类型。

包含如下取值：

tensor、int、bool、float、ListInt、ListFloat等。

是

TypeRange

针对类型为Tensor的参数，需要配置Tensor支持的类型。

包含如下取值：

fp16,fp32,double,int8,int16,int32,int64,uint8,uint16,uint32,uint64,bf16,bool等。

框架为MindSpore时，需要将Tensor的类型值转换为MindSpore所支持的值：

I8_Default,I16_Default,I32_Default,I64_Default,U8_Default,U16_Default,U32_Default,U64_Default,BOOL_Default等。

否

Required

是否必须输入，有如下取值：

    - TRUE
    - FALSE

是

Doc

对应参数的描述。

否

Attr_Default_value

属性的默认值。

否

Format

针对类型为Tensor的参数，配置为Tensor支持的数据排布格式。

包含如下取值：

ND,NHWC,NCHW,HWCN,NC1HWC0,FRACTAL_Z等。

否

Group

算子分类。

否
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

配置示例如下所示：
**表3**IR原型定义表示例
*预留行*

**Op**

**Classify**

**Name**

**Type**

**TypeRange**

**Required**

**Doc**

**Attr_Default_value**

**Format**

Reshape

INPUT

x

tensor

fp16,fp32,double,int8,int16,int32,int64,uint8,uint16,uint32,uint64,bf16,bool

TRUE

-

-

ND

INPUT

shape

tensor

int32,int64

FALSE

-

-

-

DYNAMIC_OUTPUT

y

tensor

fp16,fp32,double,int8,int16,int32,int64,uint8,uint16,uint32,uint64,bf16,bool

FALSE

-

-

ND

ATTR

axis

int

-

FALSE

-

0

-

ATTR

num_axes

int

-

FALSE

-

-1

-

ReshapeD

INPUT

x

tensor

fp16,fp32,double,int8,int16,int32,int64,uint8,uint16,uint32,uint64,bf16,bool

TRUE

-

-

ND

OUTPUT

y

tensor

fp16,fp32,double,int8,int16,int32,int64,uint8,uint16,uint32,uint64,bf16,bool

TRUE

-

-

ND

ATTR

shape

list_int

-

FALSE

-

{}

-

ATTR

axis

int

-

FALSE

-

0

-

ATTR

num_axes

int

-

FALSE

-

-1

-
|  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |

    - 请直接基于模板文件的第一个页签“Op”进行修改，实现算子的原型定义输入文件。
    - 请不要删除“Op”页签的前三行以及列。

3. 创建算子工程。

执行如下命令，参数说明请参见表4。

***msopgen gen -i {operator define file}**-f {framework type}**-c {Compute Resource}**-out {Output Path}***
**表4**参数说明
参数名称

参数描述

是否必选

gen

用于生成算子开发交付件。

是

-i，

--input

算子定义文件路径，可配置为绝对路径或者相对路径。工具执行用户需要有此路径的可读权限。

算子定义文件支持如下三种类型：

  - 适配昇腾AI处理器算子IR定义文件（.json）
  - TensorFlow的原型定义文件（.txt）
  - 适配昇腾AI处理器算子IR定义文件（.xlsx）

是

-f，

--framework

框架类型。

  - TensorFlow框架，参数值：tf或者tensorflow
  - Caffe框架，参数值：caffe
  - PyTorch框架，参数值：pytorch
  - MindSpore框架，参数值：ms或者mindspore
  - ONNX框架，参数值：onnx
说明：
所有参数值大小写不敏感。

否

-c，

--compute_unit

算子使用的计算资源。

  - *针对TBE算子，配置格式为：ai_core-{Soc Version}**，ai_core与{Soc Version}*之间用中划线“-”连接。
*{Soc Version}*的取值请根据实际昇腾AI处理器版本进行选择。
说明：
*{Soc Version}*请通过如下方式获取：

    - **针对如下产品：在安装昇腾AI处理器的服务器执行npu-smi info****命令进行查询，获取Name****信息。实际配置值为AscendName，例如Name***取值为xxxyy**，实际配置值为Ascendxxxyy*。
Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

    - **针对如下产品，在安装昇腾AI处理器的服务器执行npu-smi info -t board -i***id***-c***chip_id***命令进行查询，获取Chip Name****和NPU Name****信息，实际配置值为Chip Name_NPU Name。例如Chip Name***取值为Ascendxxx***，NPU Name***取值为1234，实际配置值为Ascendxxx**_*1234。其中：
      - **id：设备id，通过npu-smi info -l**命令查出的NPU ID即为设备id。
      - **chip_id：芯片id，通过npu-smi info -m**命令查出的Chip ID即为芯片id。

Atlas A3 训练系列产品/Atlas A3 推理系列产品

基于同系列的AI处理器型号创建的算子工程，其基础功能（基于该工程进行算子开发、编译和部署）通用。

  - 针对AI CPU算子，请配置为：aicpu。 说明：
针对Atlas A3 训练系列产品/Atlas A3 推理系列产品，不支持增加如下编译选项：

    - -march=armv8-a+lse
    - -march=armv8.1-a
    - -march=armv8.2-a
    - -march=armv8.3-a

是

-out，

--output

生成文件所在路径，可配置为绝对路径或者相对路径，并且工具执行用户具有可读写权限。

若不配置，则默认生成在执行命令的当前路径。

否

-m，

--mode

生成交付件模式。

  - 0：创建新的算子工程，若指定的路径下已存在算子工程，则会报错退出。
  - 1：在已有的算子工程中追加算子。

默认值：0。

否

-op，

--operator

此参数针对-i为算子IR定义文件的场景。

配置算子的类型，如：Conv2DTik。

若不配置此参数，当IR定义文件中存在多个算子时，工具会提示用户选择算子。

否

-lan，

--language

算子编码语言。

  - py：基于DSL和TIK算子编程框架，使用Python编程语言进行开发。

默认值：py。

否

-h，--help

输出帮助信息。

否
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

示例：

使用IR_json.json模板作为输入创建原始框架为TensorFlow的算子工程。

  1. 创建算子工程。TBE算子执行如下命令：******
```
msopgen gen -i json_path/IR_json.json -f tf -c ai_core-{Soc Version} -out ./output_data
```
AI CPU算子执行如下命令：****
```
msopgen gen -i json_path/IR_json.json -f tf -c aicpu -out ./output_data
```

    - -i参数请修改为IR_json.json文件的实际路径。例如："${INSTALL_DIR}/python/site-packages/op_gen/json_template/IR_json.json"。
    - TBE算子工程的-c参数中{Soc Version}为昇腾AI处理器的型号。

  2. 选择算子（可选）：
    - 若输入IR_json.json文件只有一个算子原型定义或使用-op参数指定算子类型请跳过此步骤。
    - 若输入IR_json.json文件中包含多个原型定义，且没有使用-op参数指定算子类型工具会提示输入选择的算子序号，选择算子。
工具会提示输入选择的算子序号，输入：1。
****
```
There is more than one operator in the .json file:  
1 Op_1
2 Op_2
Input the number of the op: 1
```

*当命令行提示：Generation completed，则完成Op_1**算子工程的创建。Op_1*为文件中"op"的值。

  3. 查看算子工程目录：
    - *TBE算子工程目录生成在-out所指定的目录下：./output_data，*目录结构如下所示：************
```
├── build.sh     // 编译配置入口脚本
├── cmake 
│   ├── config.cmake
│   ├── util        // 算子工程编译所需脚本及公共编译文件存放目录
├── CMakeLists.txt // 算子工程的CMakeLists.txt
├── framework      // 算子插件实现文件目录，框架为“PyTorch”的算子无需关注
│   ├── CMakeLists.txt
│   ├── tf_plugin    // 原始框架类型为TensorFlow时生成的算子适配插件代码所在目录
│       └── tensorflow_conv2_d_plugin.cc       // 算子适配插件实现文件
│       └── CMakeLists.txt
│   └── onnx_plugin   // 原始框架类型为ONNX时生成的算子适配插件代码所在目录
│       ├── CMakeLists.txt
│       └── conv2_d_plugin.cc   // 算子适配插件实现文件
├── op_proto     // 算子原型定义文件及CMakeLists文件所在目录   
│   ├── conv2_d.h
│   ├── conv2_d.cc
│   ├── CMakeLists.txt
├── tbe 
│   ├── CMakeLists.txt   
│   ├── impl    // 算子代码实现文件目录
│       └── conv2_d.py      // 算子代码实现文件
│   ├── op_info_cfg   // 算子信息库文件目录
│       └── ai_core
│                 ├── {Soc Version}         // 昇腾AI处理器类型
│                     ├── conv2_d.ini         // 算子信息库定义文件、
├── op_tiling  // 算子tiling实现文件目录，不涉及tiling实现的算子无需关注
│   ├── CMakeLists.txt   
├── scripts     // 自定义算子工程打包相关脚本所在目录
```

    - *AI CPU算子工程目录生成在 -out 所指定的目录下：./output_data，*目录结构如下所示：********
```
├── build.sh     // 编译配置入口脚本
├── cmake 
│   ├── config.cmake
│   ├── util        // 算子工程编译所需脚本及公共编译文件存放目录
├── CMakeLists.txt   // 算子工程的CMakeLists.txt
├── cpukernel
│   ├── CMakeLists.txt
│   ├── impl        // 算子代码实现文件目录
│   │   ├── conv2_d_kernels.cc
│   │   └── conv2_d_kernels.h
│   ├── op_info_cfg
│   │   └── aicpu_kernel
│   │       └── conv2_d.ini      // 算子信息库定义文件
│   └── toolchain.cmake
├── framework      // 算子插件实现文件目录，框架为“PyTorch”的算子无需关注
│   ├── CMakeLists.txt
│   ├── tf_plugin    // 原始框架类型为TensorFlow时生成的算子适配插件代码所在目录
│       └── tensorflow_conv2_d_plugin.cc       // 算子适配插件实现文件
│       └── CMakeLists.txt
│   └── onnx_plugin   // 原始框架类型为ONNX时生成的算子适配插件代码所在目录
│       ├── CMakeLists.txt
│       └── conv2_d_plugin.cc   // 算子适配插件实现文件
├── op_proto     // 算子原型定义文件及CMakeLists文件所在目录   
│   ├── conv2_d.h
│   ├── conv2_d.cc
│   ├── CMakeLists.txt
├── op_tiling  // 算子tiling实现文件目录，不涉及tiling实现的算子无需关注
│   ├── CMakeLists.txt
├── scripts     // 自定义算子工程打包相关脚本所在目录
```

4. **可选：**在算子工程中追加算子。

若需要在已存在的算子工程目录下追加其他自定义算子，命令行需配置“-m 1”参数。

执行如下命令。

TBE算子命令示例：
********
```
msopgen gen -i json_path/*.json -f tf -c ai_core-{Soc Version}  -out ./output_data -m 1
```

AI CPU算子命令示例：
********
```
msopgen gen -i json_path/*.json -f tf -c aicpu -out ./output_data -m 1
```

  - -i参数请修改为IR_json.json文件的实际路径。例如："${INSTALL_DIR}/python/site-packages/op_gen/json_template/IR_json.json"。
  - TBE算子工程的-c参数中{Soc Version}为昇腾AI处理器的型号。

在算子工程目录下追加*.json中的算子。MindSpore AICPU算子工程不能够添加非MindSpore框架的算子，也不能添加MindSpore TBE的算子。

**父主题：**[TBE&AI CPU算子开发场景](atlasopdev_10_0023.html)