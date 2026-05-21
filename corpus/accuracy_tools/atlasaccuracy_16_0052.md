---
title: "溢出算子数据采集与解析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0052.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0052.html"
---

# 溢出算子数据采集与解析

AI业务运行过程中出现浮点异常情况时，可通过溢出算子数据采集和解析进行问题定界定位。

#### 采集溢出算子数据

- [离线推理场景，请参见《应用开发指南 (C&C++)](https://www.hiascend.com/document/detail/zh/canncommercial/850/appdevg/acldevg/aclcppdevg_000000.html)[》中的“溢出算子数据采集及分析](https://www.hiascend.com/document/detail/zh/canncommercial/850/appdevg/acldevg/aclcppdevg_000090.html)”章节采集溢出数据。
- [TensorFlow 1.15训练/在线推理：请参见《TensorFlow 1.15模型迁移指南](https://www.hiascend.com/document/detail/zh/TensorFlowCommercial/850/migration/tfmigr1/tfmigr1_000001.html)[》中的“更多特性 > 溢出数据采集](https://www.hiascend.com/document/detail/zh/TensorFlowCommercial/850/migration/tfmigr1/tfmigr1_000076.html)”章节采集溢出数据。

#### 查看溢出算子数据

生成的溢出算子数据文件默认存储在{dump_path}/{time}/{device_id}/{model_name}/{model_id}/{data_index}目录下，例如：“/home/HwHiAiUser/output/20200808163566/0/npu_cluster_0/11/0”。如果没有采集到溢出数据，即不存在溢出情况，则不会生成上述目录。

存放路径及文件命名规则：

- dump_path：用户配置的溢出数据存放路径，例如/home/HwHiAiUser/output。
- time：时间戳，例如20200808163566。
- device_id：设备ID。
- model_name：子图名称。model_name层可能存在多个文件夹，如果model_name出现了“.”、“/”、“\”、空格时，转换为下划线表示。
- model_id：子图ID。
- data_index：迭代数，用于保存对应迭代的溢出数据。

上述目录下会生成两类溢出数据文件：

- 溢出算子的dump文件：通用命名规则如{op_type}.{op_name}.{task_id}.{stream_id}.{timestamp}，如果op_type、op_name出现了“.”、“/”、“\”、空格时，会转换为下划线表示。
用户可通过{op_name}字段确定溢出算子名，特殊场景下（如单算子API执行场景），{op_name}字段可能不完全对应算子名称，但可以大致判断出算子名称，并通过解析溢出算子dump文件确定该算子的输入和输出。

- 算子溢出数据文件：命名规则如Opdebug.Node_OpDebug.{task_id}.{stream_id}.{timestamp}。用户可通过解析算子溢出数据文件得知溢出相关信息。
  - 文件名中的task_id不是溢出算子的task_id，用户不需要关注task_id的实际含义。
  - 在docker内执行时，生成的数据存在docker里。

#### 解析溢出算子dump文件

1. 将采集到的数据文件上传到安装有Toolkit软件包的环境。
2. 进入${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
3. 执行msaccucmp.py脚本，转换dump文件为numpy文件。举例：
******
```
python3 msaccucmp.py convert -d /home/HwHiAiUser/dump -out /home/HwHiAiUser/dumptonumpy -v 2
```

-d参数支持传入单个文件，对单个dump文件进行转换，也支持传入目录，对整个path下所有的dump文件进行转换。

4. 调用Python，转换numpy文件为txt文件。举例：

```
1
2
3
4
5
```

```
$ python3
>>> import numpy as np
>>> a = np.load("/home/HwHiAiUser/dumptonumpy/Pooling.pool1.1.5.1732082705016774.output.0.npy")
>>> b = a.flatten()
>>> np.savetxt("/home/HwHiAiUser/dumptonumpy/Pooling.pool1.1.5.1732082705016774.output.0.txt", b)

```
|  |  |
| --- | --- |

转换为.txt格式文件后，维度信息、dtype均不存在。详细的使用方法请参考NumPy官网介绍。

#### 解析算子溢出数据文件

由于生成的溢出数据是二进制格式，可读性较低，需要通过工具将bin文件解析为用户可读性好的json文件。

1. **请根据实际情况，将算子溢出数据文件**上传到安装有Toolkit软件包的环境。

建议用户将data_index最小的目录下时间戳最小的dump文件作为待解析文件。

2. 进入${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
3. 执行解析命令，例如：
****
```
python3 msaccucmp.py convert -d /home/HwHiAiUser/opdebug/Opdebug.Node_OpDebug.1.5.1732082705016774 -out /home/HwHiAiUser/result
```

关键参数：

  - -d：溢出数据文件所在目录，包括文件名。
  - -out：解析结果待存储目录，如果不指定，默认生成在当前目录下。

4. 解析结果文件内容如下示例。

  - 如果同时开启AI Core算子溢出检测和Atomic Add溢出检测，则仅显示最先出现的溢出信息。
  - 如下示例中，先出现AI Core算子溢出信息，因此Atomic Add即便是有溢出信息也不会显示出来。

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
```

```
{
    "DHA Atomic Add": {
        "model_id": 0,
        "stream_id": 0,
        "task_id": 0,
        "task_type": 0,
        "pc_start": "0x0",
        "para_base": "0x0",
        "status": 0
    },
    "L2 Atomic Add": {
        "model_id": 0,
        "stream_id": 0,
        "task_id": 0,
        "task_type": 0,
        "pc_start": "0x0",
        "para_base": "0x0",
        "status": 0
    },
    "AI Core": {
        "model_id": 514,
        "stream_id": 563,
        "task_id": 57,
        "task_type": 0,
        "pc_start": "0x1008005b0000",
        "para_base": "0x100800297000",
        "kernel_code": "0x1008005ae000",
        "block_id": 1,
        "status": 32
    }
}

```
|  |  |
| --- | --- |

完整字段说明：

下列字段包含当前可解析的所有字段，各产品所包含字段请以实际产品解析结果为准。

  - model_id：标识溢出算子所在的模型ID。
  - stream_id：标识溢出算子所在的Stream ID。
  - task_id：标识溢出算子的Task ID。
  - task_type：标识溢出算子的Task类型。
  - context_id：Context ID，内部预留。
  - thread_id：线程ID，内部预留。
  - pc_start：标识溢出算子的代码程序的起始位置。
  - para_base：标识溢出算子的参数起始地址。
  - src_addr：SDMA传输场景的通信源地址。
  - dst_addr：SDMA传输场景的通信目的地址。
  - channel_id：通道ID。
  - core_id：AI Core ID。
  - kernel_code：标识溢出算子的代码程序起始位置，和pc_start相同。
  - block_id：标识溢出算子的Block ID参数。
  - **status：AICore的status寄存器状态，包含了溢出的信息。用户可以从status值分析得到具体溢出错误，具体请参见下文“通过status分析错误原因**”。

#### 通过status分析错误原因

- AI Core算子溢出检测状态字段status为十进制表示，需要转换成十六进制，然后定位到具体错误。
例如：status为272，转换成十六进制为0x00000110，则可以判定出可能原因为0x00000010+0x00000100。

  - 0x00000008：带符号的整数最小负数NEG符号位取反溢出。
  - 0x00000010：整数加法、减法、乘法或乘加操作计算有溢出。
  - 0x00000020：浮点计算有溢出。
  - 0x00000080：浮点数转无符号数的输入是负数。
  - 0x00000100：Float32转Float16或32位带符号的整数转Float16中出现溢出。
  - 0x00000400：CUBE累加出现溢出。

注：上述浮点异常信息为对应十六进制bit位的异常表示，可能会出现多种浮点异常组合的情况。

- DHA Atomic Add溢出检测状态字段status的值为十进制，大于0即表示出现DHA Atomic Add溢出。

- L2 Atomic Add溢出检测状态字段status的值为十进制，大于0即表示出现L2 Atomic Add溢出。
**父主题：**[扩展功能](atlasaccuracy_16_0051.html)