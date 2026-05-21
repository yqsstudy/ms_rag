---
title: "生成测试用例定义文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_10_0097.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_10_0097.html"
---

# 生成测试用例定义文件

指导用户使用msOpST工具生成算子测试用例定义文件（*.json），作为算子ST测试用例的输入。

#### 使用方法

1. 获取待测试算子的信息定义文件（.ini）路径。

msOpST工具根据待测算子信息库定义文件（.ini）生成算子ST测试用例定义文件，在算子工程文件中算子信息库定义文件路径如下所示。
********************************
```
├── cpukernel                             //AI CPU算子文件目录
│   ├── CMakeLists.txt
│   ├── impl        //算子代码实现文件目录
│   │   ├── xx_kernels.cc
│   │   └── xx_kernels.h
│   ├── op_info_cfg
│   │   ├── xx_kernel
│   │       ├── xx.ini                //算子信息库定义文件
│   └── toolchain.cmake
├── tbe                                    //TBE算子文件目录
│   ├── CMakeLists.txt   
│   ├── impl       //算子代码实现文件目录
│       └── xx.py       //算子代码实现文件
│   ├── op_info_cfg     //算子信息库文件目录
│       └── ai_core
│                 ├── {Soc Version}       //昇腾AI处理器类型
│                     ├── xx.ini         //算子信息库定义文件
```

*ini文件在TBE算子工程下的路径为：“tbe/op_info_cfg/ai_core/{Soc Version}/xx.ini”，{Soc Version}为*昇腾AI处理器的类型。

ini文件在AI CPU算子工程下的路径为：“cpukernel/op_info_cfg/aicpu_kernel/xx.ini”。

若进行AI CPU自定义算子ST测试，请不要改变算子工程的目录结构。因为该工具会根据算子信息库定义文件所在算子工程的目录找到算子原型定义文件，并根据算子原型定义文件生成算子测试用例定义文件。

2. 执行如下命令生成算子测试用例定义文件，参数说明请参见表1。
******************************
```
msopst create -i {operator define file} -out {output path} -m {pb file} -q
```
**表1**参数说明
参数名称

参数描述

是否必选

create

用于生成算子测试用例定义文件（*.json）。

是

-i，--input

算子信息库定义文件路径（*.ini文件），可配置为绝对路径或者相对路径。

**说明：输入的算子信息库定义文件（*.ini）仅能包含一个算子的定义。**

是

-out，--output

生成文件所在路径，可配置为绝对路径或者相对路径，并且工具执行用户具有可读写权限。

若不配置，则默认生成在执行命令的当前路径。

否

-m，--model

配置为TensorFlow模型文件的路径，可配置为绝对路径或者相对路径。

若配置此参数，工具会从TensorFlow模型文件中获取首层算子的shape信息，并自动dump出算子信息库定义文件中算子的shape、dtype以及属性的value值，如果dump出的值在算子信息库定义文件所配置的范围内，则会自动填充到生成的算子测试用例定义文件中；否则会报错。
说明：
若配置此参数，系统中需要安装1.15或2.6.5版本的TensorFlow。

否

-q，--quiet

当前版本仅针对-m参数生效，代表是否进行人机交互。

若不配置-q参数，则会提示用户修改获取到的模型中的首层shape信息。

若配置了-q参数，则不会提示用户更改首层shape信息。

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

示例：

以add算子为例，执行如下命令:
****
```
msopst create -i OpInfoDefine/add.ini -out ./output
```

*请将OpInfoDefine*更换为算子信息库定义文件所在路径，请参见步骤1。

*命令执行成功后，会在当前路径的output目录下生成算子测试用例定义文件：Add_case_timestamp*.json。

3. *修改测试用例定义模板文件“OpType**_case_timestamp*.json”。
步骤2生成的json文件为模板文件，不满足直接作为ST测试用例生成输入的要求，所以用户需要参考此步骤，修改算子测试用例定义文件（*.json），构造测试用例，以满足ST测试覆盖的范围。****************************
```
[
      {
        "case_name":"Test_Add_001",
        "error_threshold":[0.1,0.1],
        "st_mode":"pt_python_train", 
        "run_torch_api":"torch.square",
        "op": "Add",
        "input_desc": [ 
            { 
                "name": "x1",
                "format": [
                    "ND"
                ],
                "type": [ 
                    "int32",
                    "float",
                    "float16"
                ],
                "shape": [32,16], 
                "data_distribute": [
                    "uniform"                 
                ],
                "value_range": [
                    [
                        0.1,
                        1.0
                    ]
                ]
            },
            { 
                "name": "x2",
                "format": [
                    "ND"
                ],
                 "type": [
                    "int32",
                    "float",
                    "float16"
                ],
                "shape": [32,16], 
                "data_distribute": [
                    "uniform"
                ],
                "value_range": [
                    [
                        0.1,
                        1.0
                    ]
                ]
            }
        ],  
        "output_desc": [
            {
                "name": "y",
                "format": [
                    "ND"
                ],
                "type": [
                    "int32",
                    "float",
                    "float16"
                ],
                "shape": [32,16] 
          }
        ]
    }
]
```

测试用例定义文件其他配置项及说明。

  - *当TBE算子信息库定义文件（*.ini）中inputx**.paramType=optional时，生成的算子测试用例中inputx*的"format"为"UNDEFINED"或"RESERVED"，"type"为"UNDEFINED"。
  - *当TBE算子信息库定义文件（*.ini）中inputx**.paramType=dynamic时，生成的算子测试用例中inputx*的"name"为“算子名称+编号”，编号根据dynamic_input的个数确定，从0开始依次递增。
  - 当TBE算子信息库定义文件（*.ini）中Tensor的实现format与原始format不同时，用户需手动添加"ori_format"和"ori_shape"字段，将origin_format与origin_shape转成离线模型需要的format与shape。
    - "ori_format"输入为原始算子支持的数据格式，个数必须与format个数保持一致。
    - "ori_shape"输入为shape根据format和ori_format转换的结果。

[用户可基于如上模板进行修改，“*.json”文件支持的全量字段说明如下表所示。不同场景下的测试用例定义文件的样例可参见测试用例定义文件配置样例](atlasopdev_10_0099.html#ZH-CN_TOPIC_0000002536920611)。
**表2**算子测试用例定义json文件
参数

说明

case_name

-

必选。

String类型。

测试用例的名称。

op

-

必选。

String类型。

算子的类型。不允许为空。

error_threshold

-

可选。

配置自定义精度标准，取值为含两个元素的列表："[threshold1，threshold2]"

  - threshold1：算子输出结果与标杆数据误差阈值，若误差大于该值则记为误差数据。
  - threshold2：误差数据在全部数据占比阈值。若误差数据在全部数据占比小于该值，则精度达标，否则精度不达标。

取值范围为："[0.0,1.0]"。
说明：
若测试用例json文件和执行msopst命令时均配置该参数，以执行msopst命令时配置的精度标准进行比对。若均未配置，则以执行msopst命令时默认精度标准[0.01,0.05]进行比对。

st_mode

-

可选。

String类型。

ST测试模式，其值为："ms_python_train"，表示Mindspore的算子工程（仅Atlas 训练系列产品支持）；"pt_python_train"，表示PyTorch框架下的算子工程。

run_torch_api

-

可选。

*配置torch_api调用算子的接口，其值为："torch.square*"，“square”为接口名称，请根据实际情况配置。

expect

-

可选。

用户期望的测试结果状态。属性支持以下两种类型，默认值为“success”。

  - success：表示期望测试用例运行成功。若模型转换失败，流程将提前终止，用户可查看ATC工具相关日志定位问题。
  - failed：表示期望测试用例运行失败。若用户需要运行异常用例，可修改expect字段为failed。若模型转换失败，流程将继续执行。

在统计结果中，依据STCaseReport中的status和expect是否一致统计，一致则统计至“success count”，不一致则统计至“failed count”。

fuzz_impl

-

可选，String类型。

若用户需要生成大量测试用例，可利用fuzz测试参数生成脚本辅助生成。此种场景下，用户需要手工添加此字段，配置fuzz测试参数生成脚本的绝对路径或者相对路径：函数名，fuzz测试参数生成脚本的实现方法请参见4。
说明：
不建议用户调用其它用户目录下的fuzz测试参数生成脚本，以避免提权风险。

fuzz_case_num

-

可选。

int类型。

在添加了“fuzz_impl”参数的情况下，需要手工添加此字段，配置利用fuzz测试参数生成脚本生成测试用例数量，范围为1~2000。

input_desc

-

必选。

算子输入描述。
说明：
所有input_desc中参数取值的个数都要一致，否则测试用例生成会失败。

例如：input1的format支持的类型个数2，则input2的format支持的类型个数也需要为2。

*同理，所有inputx*中的type、shape、data_distribute和value_range的取值个数也需要保持一致。

-

name

可选。

*算子为动态多输入场景时，“name”为必选配置，请配置为算子信息库中“inputx*.name”参数的名称+编号，编号从“0”开始，根据输入的个数按照0，1，2......，依次递增。

例如，算子信息文件中指定的输入个数为4个，则input_desc中需要配置4个输入描述，name分别为“xxx0”、"xxx1"、“xxx2”、“xxx3”，其中xxx为输入参数的名称。

[动态多输入场景的配置示例可参见•若算子的输入个数不确定（动态多输入场景）](atlasopdev_10_0099.html#ZH-CN_TOPIC_0000002536920611__zh-cn_topic_0000002502586554_li847855219617)。

-

format

必选。

String或者String的一维数组。

输入Tensor数据的排布格式，不允许为空。
常见的数据排布格式如下：
  - NCHW
  - NHWC
  - ND：表示支持任意格式。
  - NC1HWC0：5维数据格式。其中，C0与微架构强相关，该值等于Cube单元的size，例如16；C1是将C维度按照C0切分：C1=C/C0，若结果不整除，最后一份数据需要padding到C0。
  - FRACTAL_Z：卷积的权重的格式。
  - FRACTAL_NZ：分形格式，在Cube单元计算时，输出矩阵的数据格式为NW1H1H0W0。整个矩阵被分为（H1*W1）个分形，按照column major排布，形状如N字形；每个分形内部有（H0*W0）个元素，按照row major排布，形状如z字形。考虑到数据排布格式，将NW1H1H0W0数据格式称为Nz格式。其中，H0,W0表示一个分形的大小，示意图如下所示：


  - RESERVED：预留，当format配置为该值，则type必须配置为“UNDEFINED”，代表算子的此输入可选。

  - fuzz：使用fuzz测试参数生成脚本自动批量生成值。

-

ori_format

可选。

String或者String的一维数组，支持以下两种取值：

  - 配置为输入数据的原始format。
当算子实现的format与原始format不同时，需要配置此字段；若不配置此字段，默认算子实现的format与原始format相同。

  - 配置为“fuzz”，表示使用fuzz测试参数生成脚本自动批量生成值。

-

type

必选。

String或者String的一维数组。

输入数据支持的数据类型。

  - bool
  - int8
  - uint8
  - int16
  - uint16
  - int32
  - int64
  - uint32
  - uint64
  - float16
  - float32
  - float
  - bfloat16（仅Atlas A2 训练系列产品/Atlas A2 推理系列产品支持该数据类型）
  - double（仅AI CPU算子支持该数据类型）
  - complex64（仅AI CPU算子支持该数据类型）
  - complex128（仅AI CPU算子支持该数据类型）
  - UNDEFINED：表示算子的输入类型为可选。
  - fuzz：使用fuzz测试参数生成脚本自动批量生成值。

[输入数据类型为复数场景的配置示例可参见•若算子的输入输出类型为复数，测试用例定义文件如...](atlasopdev_10_0099.html#ZH-CN_TOPIC_0000002536920611__zh-cn_topic_0000002502586554_li115917150720)。

-

shape

必选。

  - int类型。一维或者二维数组。
输入Tensor支持的形状。

    - 支持静态shape输入的场景：
shape维度以及取值都为固定值，该场景下不需要配置shape_range参数。

    - 支持动态shape输入的场景：
shape中包含-1，例如：(200, -1)表示第二个轴长度未知。该场景下需要与shape_range参数配合使用，用于给出“-1”维度的取值范围。

  - String类型，“fuzz”。
支持fuzz，使用fuzz测试参数生成脚本自动批量生成值。

  - 空
如果format和type为UNDEFINED时shape允许为空。

需要注意，配置的shape需要与format相匹配。

-

ori_shape

可选。

  - int类型。一维或者二维数组。
输入数据的原始shape。当算子实现的shape与原始shape不同时，需要配置此字段。

  - String类型，“fuzz”。
支持fuzz，使用fuzz测试参数生成脚本自动批量生成值。

若不配置此字段，默认算子实现的shape与原始shape一致。

-

typical_shape

可选。

  - int类型。一维或者二维数组。
实际用于测试的shape。

若配置的“shape”字段中含有-1时，用户需要在算子测试用例定义文件中新增“typical_shape”字段，给定出固定shape值，用于实际测试。

  - String类型，“fuzz”。
支持fuzz，使用fuzz测试参数生成脚本自动批量生成值。

-

shape_range

可选。

  - int类型。一维或者二维数组。
当算子支持动态shape时，此字段表示支持的shape范围。

默认值为：[[1,-1]]。表示shape可以取1到无穷。

例如：shape配置为(200, -1)，shape_range配置为[[1,-1]]时，则代表shape第二个维度的取值为1到无穷。

  - String类型，“fuzz”。
支持fuzz，使用fuzz测试参数生成脚本自动批量生成值。

-

is_const

可选。

bool类型。

  - true：若用户需要配置常量输入的用例，则配置该字段，其值为true。
  - false：若该字段值为false，则需要配置张量输入用例。

[输入为常量的配置示例可参见•若算子的某个输入为常量，测试用例定义文件如下所...](atlasopdev_10_0099.html#ZH-CN_TOPIC_0000002536920611__zh-cn_topic_0000002502586554_li1664717410582)。

-

data_distribute

必选。

String或者String的一维数组。
使用哪种数据分布方式生成测试数据，支持的分布方式有：
  - uniform：返回均匀分布随机值
  - normal：返回正态分布（高斯分布）随机值
  - beta：返回Beta分布随机值
  - laplace：返回拉普拉斯分布随机值
  - triangular：返回三角形分布随机值
  - relu：返回均匀分布+Relu激活后的随机值
  - sigmoid：返回均匀分布 + sigmoid激活后的随机值
  - softmax：返回均匀分布 + softmax激活后的随机值
  - tanh：返回均匀分布 + tanh激活后的随机值
  - fuzz：使用fuzz测试参数生成脚本自动批量生成值

-

value_range

必选。

  - int类型或者float类型。一维或者二维数组。
取值范围，不能为空。

为[min_value, max_value]且min_value <=max_value。

  - String类型，“fuzz”。
支持fuzz，使用fuzz测试参数生成脚本自动批量生成值

-

value

可选。

String或者Tensor数组。
若用户需要指定输入数据时，可通过增加“value”字段进行配置。有如下两种配置方式：
  - 直接输入Tensor数据，如Tensor的值为[1,2,3,4]。
"value": [1,2,3,4]

  - 输入二进制数据文件的路径，如数据文件为test.bin时。
"value": "../test.bin"

二进制数据bin文件需用户自行准备。可以输入绝对路径，也可以输入测试用例定义文件的相对路径。

  - 配置为“fuzz”，使用fuzz测试参数生成脚本自动批量生成值。 说明：
[若用户添加了“value”字段，“data_distribute”和“value_range”字段将会被忽略。同时需要保证“format”,"type"，"shape"字段的值与“value”数据对应，且每个用例只能测试一种数据类型。配置示例可参见•若指定固定输入，例如ReduceSum的axe...](atlasopdev_10_0099.html#ZH-CN_TOPIC_0000002536920611__zh-cn_topic_0000002502586554_li10983136112016)。

output_desc

-

必选。

算子输出描述。
说明：
output_desc中参数取值的个数都要与input_desc一致，否则测试用例生成会失败。

*例如：inputx*的format支持的类型个数2，则output的format支持的类型个数也需要为2。

-

name

可选。String类型。

输出参数名称。

算子为动态多输出场景时，“name”为必选配置，请配置为算子信息库中“outputx.name”参数的名称+编号，编号从“0”开始，根据输出的个数按照0，1，2......，依次递增。

例如，算子信息文件中指定的输出个数为4个，则output_desc中需要配置4个输出描述，name分别为“xxx0”、"xxx1"、“xxx2”、“xxx3”，其中xxx为输出参数的名称。

-

format

必选。

String或者String的一维数组。

输出Tensor数据的排布格式，不允许为空。

支持如下数据排布格式：

  - NCHW
  - NHWC
  - ND：表示支持任意格式。
  - NC1HWC0：5维数据格式。其中，C0与微架构强相关，该值等于Cube单元的size，例如16；C1是将C维度按照C0切分：C1=C/C0，若结果不整除，最后一份数据需要padding到C0。
  - FRACTAL_Z：卷积的权重的格式。
  - FRACTAL_NZ：分形格式，在Cube单元计算时，输出矩阵的数据格式为NW1H1H0W0。整个矩阵被分为（H1*W1）个分形，按照column major排布，形状如N字形；每个分形内部有（H0*W0）个元素，按照row major排布，形状如z字形。考虑到数据排布格式，将NW1H1H0W0数据格式称为Nz格式。其中，H0,W0表示一个分形的大小，示意图如下所示：


  - fuzz：使用fuzz测试参数生成脚本自动批量生成值。

-

ori_format

可选。

String或者String的一维数组。

  - 当算子实现的format与原始format不同时，需要配置此字段，配置为数据的原始format。
  - 配置为“fuzz”，表示使用fuzz测试参数生成脚本自动批量生成值。

若不配置此字段，默认算子实现的format与原始format相同。

-

type

必选。

String或者String的一维数组或“fuzz”。

输出数据支持的数据类型。

  - bool
  - int8
  - uint8
  - int16
  - uint16
  - int32
  - int64
  - uint32
  - uint64
  - float16
  - float32
  - float
  - bfloat16（仅Atlas A2 训练系列产品/Atlas A2 推理系列产品支持该数据类型）
  - double（仅AI CPU算子支持该数据类型）
  - complex64（仅AI CPU算子支持该数据类型）
  - complex128（仅AI CPU算子支持该数据类型）
  - fuzz：使用fuzz测试参数生成脚本自动批量生成值。

-

shape

必选。

  - int类型。一维或者二维数组。
输入Tensor支持的形状。

  - String类型，“fuzz”。
支持fuzz，使用fuzz测试参数生成脚本自动批量生成值。

-

ori_shape

可选。

  - int类型。一维或者二维数组。
输入数据的原始shape。当算子实现的shape与原始shape不同时，需要配置此字段。

  - String类型，“fuzz”。
支持fuzz，使用fuzz测试参数生成脚本自动批量生成值。

若不配置此字段，默认算子实现的shape与原始shape一致。

attr

-

可选。

-

name

若配置attr，则为必选。

String类型。

属性的名称，不为空。

-

type

若配置attr，则为必选。

String类型。

属性支持的类型。

  - bool
  - int
  - float
  - string
  - list_bool
  - list_int
  - list_float
  - list_string
  - list_list_int
  - data_type：如果attr中的value值为数据类型时，type值必须为data_type

-

value

若配置attr，则为必选。

属性值，根据type的不同，属性值不同。

  - 如果“type”配置为“bool”，“value”取值为true或者false。
  - 如果“type”配置为“int”，“value”取值为整形数据。
  - 如果“type”配置为“float”，“value”取值为浮点型数据。
  - 如果“type”配置为“string”，“value”取值为字符串，例如“NCHW”。
  - 如果“type”配置为“list_bool”，“value”取值示例：[false, true]。
  - 如果“type”配置为“list_int”，“value”取值示例：[1, 224, 224, 3]。
  - 如果“type”配置为“list_float”，“value”取值示例：[1.0, 0.0]。
  - 如果“type”配置为“list_string”，“value”取值示例：["str1", "str2"]
  - 如果“type”配置为“list_list_int”，“value”取值示例：[[1, 3, 5, 7], [2, 4, 6, 8]]
  - 如果“type”配置为“data_type”，“value”支持如下取值：int8、int32、int16、int64、uint8、uint16、uint32、uint64、float、float16、float32、bool、double、complex64、complex128、bfloat16
  - “value”值配置为“fuzz”时，表示使用fuzz测试参数生成脚本自动批量生成值。

calc_expect_func_file

-

可选。

String类型。

算子期望数据生成函数对应的文件路径及算子函数名称，如："/home/test/test_*.py:function"

其中，/home/test/test_*.py为算子期望数据生成函数的实现文件，function为对应的函数名称。
须知：
不建议用户调用其它用户目录下的期望数据生成脚本，以避免提权风险。
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
|  |  |  |
|  |  |  |
|  |  |  |

4. 若用户需要自动生成大量测试用例，请参考此步骤用实现fuzz测试参数生成脚本（.py）并配置测试用例定义文件（.json）。

  1. 实现fuzz测试参数生成脚本。该脚本可以自动生成测试用例定义文件中input_desc、output_desc、attr内除了name的任何参数。下面以随机生成shape和value参数为例，创建一个fuzz_shape.py供用户参考。该示例会随机生成一个1-4维，每个维度取值范围在1-64的shape参数，用于ST测试。
    1. 导入脚本所需依赖。
```
import numpy as np
```

    2. **实现fuzz_branch()方法，若用户自定义随机生成待测试参数的方法名，需要在算子测试用例定义文件中配置fuzz_impl**字段。
```
def fuzz_branch():
    # 生成测试参数shape值
    dim = random.randint(1, 4)
    x_shape_0 = random.randint(1, 64)
    x_shape_1 = random.randint(1, 64)
    x_shape_2 = random.randint(1, 64)
    x_shape_3 = random.randint(1, 64)
    if dim == 1:
        shape = [x_shape_0]
    if dim == 2:
        shape = [x_shape_0, x_shape_1]
    if dim == 3:
        shape = [x_shape_0, x_shape_1, x_shape_2]
    if dim == 4:
        shape = [x_shape_0, x_shape_1, x_shape_2, x_shape_3]
    # 根据shape随机生成x1、x2的value
    fuzz_value_x1 = np.random.randint(1, 10, size=shape)
    fuzz_value_x2 = np.random.randint(1, 10, size=shape)

    # 用字典数据结构返回shape值，将生成的shape值返回给input_desc的x1、x2和output_desc的y的shape参数。其中x1、x2、y测试用例定义文件输入、输出的name。
    return {"input_desc": {"x1": {"shape": shape,"value": fuzz_value_x1}, 
                           "x2": {"shape": shape,"value": fuzz_value_x2}},
            "output_desc": {"y": {"shape": shape}}}
```

      - 该方法生成测试用例定义文件input_desc、output_desc、attr内除了name的任何参数，用户可自定义实现参数的生成方法，以满足算子测试的需求。
      - 该方法的返回值为字典格式，将该方法生成的参数值以字典的方式赋值给算子进行st测试。返回的字典结构与测试用例定义文件中参数结构相同。

  2. 配置测试用例定义文件。
    1. 添加“fuzz_impl”字段，值为“fuzz生成测试参数的脚本的相对路径或绝对路径：函数名”，如：“conv2d_fuzz.py:fuzz_branch”若自定义的随机生成待测试参数的方法，请将fuzz_branch配置为自定义方法名，若不配置默认使用fuzz_branch方法。
    2. 添加“fuzz_case_num”字段，值为利用fuzz脚本生成多少条测试用例，如：2000。
    3. 将需要自动生成的参数的值设为"fuzz"。
详细的参数说明可参见表2。

算子测试用例定义文件的示例如下所示：
************************************************************************
```
[
    {
        "case_name":"Test_Add_001",         
        "op": "Add",                             
        "fuzz_impl": "./fuzz_shape.py:fuzz_branch",   //配置fuzz测试参数生成脚本路径:函数名
        "fuzz_case_num": 2000,   //配置生成测试用例数量
         "input_desc": [            // 算子的输入描述
              {                     //算子的第一个输入
                "name": "x1",
                "format": [
                    "ND"       //删除多余值，保留一个与自动生成shape参数相匹配的值
                ],
                "type": [
                    "float16"  //删除多余值，保留一个与自动生成shape参数相匹配的值
                ],
                "shape":"fuzz",     // 修改自动生成参数的值为“fuzz”
                "data_distribute": [
                    "uniform"
                ],
                "value_range": [
                    [
                        0.1,
                        1.0
                    ]
                ],	
                "value": "fuzz"	
             {                     //算子的第二个输入
                "name": "x2",
                 "format": [
                    "ND"          //删除多余值，保留一个与自动生成shape参数相匹配的值
                ],
                "type": [
                    "float16"     //删除多余值，保留一个与自动生成shape参数相匹配的值 
                ],
                "shape":"fuzz",  //  修改自动生成参数的值为“fuzz”
                "data_distribute": [
                    "uniform"
                ],
                "value_range": [
                    [
                        0.1,
                        1.0
                    ]
                ],       
                "value": "fuzz" 
            }
        ],  
        "output_desc": [                       //算子的输出描述，必选，含义同输入Tensor描述
            {
                "name": "y",
                "format": [
                    "ND"                     //删除多余值，保留一个与自动生成shape参数相匹配的值
                ],
                "type": [
                    "float16"         //删除多余值，保留一个与自动生成shape参数相匹配的值
                ],
                "shape":"fuzz"       //  修改自动生成参数的值为“fuzz”
    }
]
```

    - 测试用例定义文件中参数为“fuzz”的输入、输出或属性需要有“name”参数，若没有请手动添加“name”参数，如： "name": "y"。
    - 若测试用例定义文件中存在参数值为“fuzz”的情况下，其他各参数取值需唯一，并且与fuzz测试参数生成脚本生成的参数不矛盾，如：shape参数为“fuzz”，且生成的shape为[1, 3, 16, 16]，对应的format也应该是支持4维的。

5. 若用户需要得到实际算子输出与期望输出的比对结果，需要参考此步骤自定义期望数据生成函数。

  1. 自定义实现add算子期望数据生成函数。
在Python文件中实现算子期望数据生成函数，文件目录和文件名称可自定义，如“/home/test/test_add_st.py”。

例如Add算子的期望数据生成函数实现如下：

```
def calc_expect_func(x1, x2, y):    
    res = x1["value"] + x2["value"]
    return [res, ]
```

用户需根据开发的自定义算子完成算子期望数据生成函数。测试用例定义文件中的全部Input、Output、Attr的name作为算子期望数据生成函数的输入参数，若Input是可选输入，请将该输入指定默认值传参。

例如，某算子输入中的x3为可选输入时，定义该算子的期望数据生成函数如下。

```
def calc_expect_func(x1, x2, x3=None, y=None)
```

  2. *在ST测试用例定义文件“OpType*_xx.json”中增加比对函数。配置算子测试用例定义文件。在1*中的算子测试用例定义文件Add_case_timestamp*.json增加"calc_expect_func_file"参数，参数值为"/home/test/test_add_st.py:calc_expect_func"。********
```
[
    {
        "case_name":"Test_Add_001",         
        "op": "Add",                             
        "calc_expect_func_file": "/home/test/test_add_st.py:calc_expect_func",   //配置生成算子期望输出数据的实现文件
        "input_desc": [...]
        ...
        ...
    }
]
```

**父主题：**[基于msOpST工具进行算子ST测试](atlasopdev_10_0095.html)