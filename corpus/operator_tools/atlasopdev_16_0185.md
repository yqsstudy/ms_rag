---
title: "mskpp.tiling_func"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0185.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0185.html"
---

# mskpp.tiling_func

#### 功能说明

调用用户的tiling函数。

[mskpp.tiling_func不支持调用《基础数据结构和接口参考](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/basicdataapi/atlasopapi_07_00001.html)》中的GetCompileInfo接口。

#### 函数原型

```
def tiling_func(op_type: str, inputs: list, outputs: list, lib_path: str,
                inputs_info: list = None, outputs_info: list = None, attr=None, soc_version: str = None) -> TilingOutput
```

#### 参数说明

参数名

输入/输出

说明

op_type

输入

需根据tiling函数的实现填写，例如AddCustom、 MatmulLeakyreluCustom等。msKPP工具查找tiling函数的唯一依据，查找逻辑请参见lib_path参数。

数据类型：str。

必选参数。
说明：
若CANN中曾经部署过相同类型的算子（op_type），用户修改了tiling函数并重新编译，则需要在CANN环境中重新部署该算子。

inputs

输入

按Kernel函数入参顺序填入tensor信息，不使用某个参数的情况，对应位置请传入None占位。

数据类型为list，每个元素必须是tensor或者list[tensor]，不在inputs_info中显式指定format或者ori_format时，所有tensor默认为ND格式。

可选参数。

outputs

输入

按Kernel函数入参顺序填入tensor信息，不使用某个参数的情况，对应位置请传入None占位。

数据类型：list，每个元素必须是tensor或者list[tensor]，不在inputs_info中显式指定format或者ori_format时，所有tensor默认为ND格式。

可选参数。

inputs_info

输入

按Kernel函数入参顺序填写info信息，不使用某个参数的情况，对应位置请传入空dict或者None占位。

数据类型为list，inputs_info参数中元素的数据类型为dict或list[dict]，每个dict的元素说明如下：

- ori_shape：输入tensor的原始维度信息。
- shape：输入tensor运行时的维度信息。
- [dtype：输入tensor的数据类型，具体请参见《TBE&AI CPU算子开发接口](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/aicpuopapi/opdevapi_07_0000.html)》的DataType接口。
- [ori_format：输入tensor的原始数据排布格式，默认为ND，具体请参见《TBE&AI CPU算子开发接口](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/aicpuopapi/opdevapi_07_0000.html)》的Format接口。
- [format：输入tensor的数据排布格式，默认为ND，具体请参见《TBE&AI CPU算子开发接口](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/aicpuopapi/opdevapi_07_0000.html)》的Format接口。
- data_path：值依赖场景下，输入tensor的bin文件路径。

举例如下：

```
[{"ori_shape": [8, 2048], "shape": [8, 2048], "dtype": "float16", "ori_format": "ND", "format": "ND"},
 {"ori_shape": [8, 2048], "shape": [8, 2048], "dtype": "float16", "ori_format": "ND", "format": "ND"}]
```

可选参数。
说明：
该输入参数和inputs存在约束关系：

- inputs为tensor时，inputs_info必须是dict。
- inputs为list[tensor]时，inputs_info必须是list[dict]。
- inputs为None时，inputs_info每个元素至少包含[shape, dtype]。

outputs_info

输入

存放输出的信息，不使用某个参数的情况，对应位置请传入空dict占位。

数据类型为list，outputs_info参数中元素的数据类型为dict或list[dict]，每个dict的元素说明如下：

- ori_shape：输出tensor的原始维度信息。

- shape：输出tensor的维度信息。
- [dtype：输出tensor的数据类型，具体请参见《TBE&AI CPU算子开发接口](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/aicpuopapi/opdevapi_07_0000.html)》的DataType接口。
- [ori_format：输出tensor的原始数据排布格式，默认为ND，具体请参见《TBE&AI CPU算子开发接口](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/aicpuopapi/opdevapi_07_0000.html)》的Format接口。
- [format：输出tensor的数据排布格式，默认为ND，具体请参见《TBE&AI CPU算子开发接口](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/aicpuopapi/opdevapi_07_0000.html)》的Format接口。
- data_path：保留参数，不生效。

举例如下：

```
[{"shape": [8, 2048], "dtype": "float16", "format": "ND"},
 {"shape": [8, 2048], "dtype": "float16", "format": "ND"}]
```

可选参数。
说明：
该输入参数和inputs存在约束关系：

- outputs为tensor时，outputs_info必须是dict。
- outputs为list[tensor]时，outputs_info必须是list[dict]。
- outputs为None时，outputs_info每个元素至少包含[shape, dtype]。

attr

输入

tiling函数使用到的算子属性。

数据类型：dict或者list。
说明：
- dict格式键值只能包含大小写英文字母、数字、下划线。
```
{
  "a1": 1,
  "a2": False,
  "a3": "ssss",
  "a4": 1.2,
  "a5": [111, 222, 333],
  "a6": [111.111, 111.222, 111.333],
  "a7": [True, False],
  "a8": ["asdf", "zxcv"],
  "a9": [[1, 2, 3, 4], [5, 6, 7, 8], [5646, 2345]],
}
```

- list格式，推荐使用。若某个attr需要传空列表时，必须用这种格式（例如下面的"a10"）。
  - "name"和"value"的值只能包含大小写英文字母、数字、下划线。
  - "dtype"：输入tensor的数据类型。

```
[
  {"name": "a1", "dtype": "int", "value": 1},
  {"name": "a2", "dtype": "bool", "value": False},
  {"name": "a3", "dtype": "str", "value": "ssss"},
  {"name": "a4", "dtype": "float", "value": 1.2},
  {"name": "a5", "dtype": "list_float", "value": [111.111, 111.222, 111.333]},
  {"name": "a6", "dtype": "list_bool", "value": [True, False]},
  {"name": "a7", "dtype": "list_str", "value": ["asdf", "zxcv"]},
  {"name": "a8", "dtype": "list_list_int", "value": [[1, 2, 3, 4], [5, 6, 7, 8], [5646, 2345]]},
  {"name": "a9", "dtype": "list_int", "value": [111, 222, 333]},
  {"name": "a10", "dtype": "list_int", "value": []},
  {"name": "a11", "dtype": "int64", "value": 2},
  {"name": "a12", "dtype": "float32", "value": 1.3},
  {"name": "a13", "dtype": "string", "value": "ssss"},
  {"name": "a14", "dtype": "list_string", "value": ["asdf", "zxcv"]},
]
```

可选参数。

lib_path

输入

**msOpGen工程编译生成的liboptiling.so文件的路径，可在工程目录下通过f****ind . -name 'liboptiling.so'****进行查找。msKPP工具会按已部署算子、.so**文件的查找顺序获取用户tiling函数。

数据类型：str。

可选参数。

soc_version

输入

配置为昇腾AI处理器的类型。

可选参数。
说明：
- **非Atlas A3 训练系列产品/Atlas A3 推理系列产品：在安装昇腾AI处理器的服务器执行npu-smi info****命令进行查询，获取Chip Name****信息。实际配置值为AscendChip Name，例如Chip Name***取值为xxxyy**，实际配置值为Ascendxxxyy**。当Ascendxxxyy为代码样例的路径时，需要配置为ascendxxxyy*。
- **Atlas A3 训练系列产品/Atlas A3 推理系列产品：在安装昇腾AI处理器的服务器执行npu-smi info -t board -i***id***-c***chip_id***命令进行查询，获取Chip Name****和NPU Name****信息，实际配置值为Chip Name_NPU Name。例如Chip Name***取值为Ascendxxx***，NPU Name***取值为1234，实际配置值为Ascendxxx**_**1234。当Ascendxxx**_**1234为代码样例的路径时，需要配置为ascendxxx**_*1234。
其中：

  - **id：设备id，通过npu-smi info -l**命令查出的NPU ID即为设备id。
  - **chip_id：芯片id，通过npu-smi info -m**命令查出的Chip ID即为芯片id。

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

#### 返回值说明

参数名

说明

blockdim

用户tiling函数配置的核数。

数据类型：int。

workspace_size

该值为用户自行申请的workspace大小加上 msKPP工具预留的78,643,200Byte。

数据类型：int。

workspace

msKPP工具为用户申请的workspace空间，大小为workspace_size。

数据类型：numpy.array。

tiling_data

存放tiling_data，用于调用Kernel函数。

数据类型：numpy.array。

tiling_key

用户tiling函数配置的tiling_key，若用户未设置，msKPP工具会默认设置为0。

数据类型：int。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### 调用示例

```
M = 1024
N = 640
K = 256
input_a = np.random.randint(1, 10, [M, K]).astype(np.float16)
input_b = np.random.randint(1, 10, [K, N]).astype(np.float16)
input_bias = np.random.randint(1, 10, [N]).astype(np.float32)
output = np.zeros([M, N]).astype(np.float32)
# tiling data
tiling_output = mskpp.tiling_func(
    op_type="MatmulLeakyreluCustom",
    inputs=[input_a, input_b, input_bias], outputs=[output],
    lib_path="liboptiling.so",  # tiling代码编译产物 
)
```
**父主题：**[接口列表](atlasopdev_16_0175.html)