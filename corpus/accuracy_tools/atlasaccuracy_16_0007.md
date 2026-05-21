---
title: "准备NPU侧dump数据和计算图文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0007.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0007.html"
---

# 准备NPU侧dump数据和计算图文件

#### 使用前须知

- 需要完成训练/在线推理网络的开发、编译和运行，确保拥有可执行的训练/在线推理工程。
- [本节dump数据过程仅为参考示例，介绍基本操作，更多详细介绍请参见《TensorFlow 1.15模型迁移指南](https://www.hiascend.com/document/detail/zh/TensorFlowCommercial/850/migration/tfmigr1/tfmigr1_000001.html)》。
- 每次迭代都会产生dump数据，在训练数据集较大时，每次迭代产生的dump数据量也会增大，建议控制迭代次数，一般仅执行一次迭代。同时对于大模型场景，通常dump数据量太大并且耗时长，可以通过dump_data开启算子统计功能，根据统计数据识别可能异常的算子后，再dump可能异常的算子。
- 多卡环境下，由于训练/在线推理脚本中，每张卡的进程启动时间存在差异，这会导致落盘时产生多个时间戳目录。
- 在容器内执行时，生成的数据保存在容器里。
- 如果训练/在线推理网络包含了随机因子，请在执行生成dump数据前去除。
- 确保代码在网络结构、算子、优化器的选择上，以及参数的初始化策略等方面与GPU上训练/在线推理的代码完全一致，否则比对无意义。
- 不建议在同一个训练脚本中同时进行训练和验证，即不建议将train和evaluate放在同一个脚本中，否则会产生两组dump数据，容易造成混淆。
- 目前仅支持AI CPU、AI Core和HCCL算子进行dump数据。

#### dump参数配置
修改训练/在线推理脚本，开启dump功能。在相应代码中，增加如下的加粗字体信息。
- **Estimator模式：通过NPURunConfig中的dump_config****采集dump数据，在创建NPURunConfig之前，实例化一个DumpConfig**类进行dump的配置（包括配置dump路径、dump哪些迭代的数据、dump算子的输入还是输出数据等）。
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
```

```
from npu_bridge.npu_init import *

# dump_path：dump数据存放路径，该参数指定的目录需要在启动训练/在线推理的环境上（容器或Host侧）提前创建且确保安装时配置的运行用户具有读写权限
# enable_dump：是否开启dump功能
# dump_step：指定采集哪些迭代的dump数据
# dump_mode：dump模式，取值：input/output/all
dump_config = DumpConfig(enable_dump=True, dump_path = "/home/output", dump_step="0|5|10", dump_mode="all")

config = NPURunConfig(
  dump_config=dump_config, 
  session_config=session_config
  )

```
|  |  |
| --- | --- |

- sess.run模式：通过session配置项enable_dump、dump_path、dump_step、dump_mode配置dump参数。
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
```

```
config = tf.ConfigProto()

custom_op =  config.graph_options.rewrite_options.custom_optimizers.add()
custom_op.name =  "NpuOptimizer"
custom_op.parameter_map["use_off_line"].b = True

custom_op.parameter_map["enable_dump"].b = True
custom_op.parameter_map["dump_path"].s = tf.compat.as_bytes("/home/output") 
custom_op.parameter_map["dump_step"].s = tf.compat.as_bytes("0|5|10")
custom_op.parameter_map["dump_mode"].s = tf.compat.as_bytes("all") 
custom_op.parameter_map["dump_layer"].s = tf.compat.as_bytes("nodename1 nodename2 nodename3")
config.graph_options.rewrite_options.remapping = RewriterConfig.OFF

with tf.Session(config=config) as sess:
  print(sess.run(cost))

```
|  |  |
| --- | --- |


[TensorFlow模型训练/在线推理过程中可能存在算子溢出的情况，此时若直接进行精度比对操作则会造成比对结果不准确，请参见溢出算子数据采集与解析](atlasaccuracy_16_0052.html#ZH-CN_TOPIC_0000002504184006)采集溢出数据。

#### 获取dump数据文件和计算图文件

1. 执行训练/在线推理脚本，生成dump数据文件和计算图文件。
开启dump数据采集功能后，脚本执行时会自动在当前执行目录下生成计算图的dump文件（不含有权重等数据的基本版dump，仅dump经过GE优化、编译后的图），后续开发者通过工具进行精度比对时，会依赖此计算图文件查找dump数据文件。您也可以通过环境变量DUMP_GRAPH_PATH指定dump图文件存储路径，示例：
```
export DUMP_GRAPH_PATH=/home/dumpgraph
```

dump数据文件生成在{dump_path}指定的目录下，即{dump_path}/{time}/{device_id}/{model_name}/{model_id}/{data_index}目录下，以{dump_path}配置/home/output为例，例如存放在“/home/output/20200808163566/0/ge_default_20200808163719_121/11/0”。
**表1**dump数据文件路径格式说明
路径key

说明

备注

dump_path

dump数据存放路径（如果设置的是相对路径，则为拼接后的全路径）。

-

time

dump数据文件落盘的时间。

格式为：YYYYMMDDHHMMSS

device_id

设备ID。

-

model_name

子图名称。

model_name层可能存在多个文件夹，dump数据取计算图名称对应目录下的数据。

如果model_name出现了“.”、“/”、“\”以及空格时，转换为下划线表示。

model_id

子图ID号。

--

data_index

迭代数，用于保存对应迭代的dump数据。

如果指定了dump_step，则data_index和dump_step一致；如果不指定dump_step，则data_index序号从0开始计数，每dump一个迭代的数据，序号递增1。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

2. 选取计算图文件。

  - 方法一：
**执行训练脚本完成后会在训练脚本当前目录生成GE图文件，图文件可能会有多个。一般情况下，选取计算图文件方法：将TensorFlow模型保存为pb文件，然后查看该模型，选取其中一个计算类算子的名字作为关键字，找包含该关键字的计算图文件。计算图名称取计算图文件graph****下的name**字段值。

  - 方法二：在所有以“_Build.txt”为结尾的dump图文件中，查找“Iterator”关键词。记录查找出的计算图文件名称，用于后续精度比对。
```
grep Iterator *_Build.txt
```



如上图所示，“ge_proto_00292_Build.txt”即为需要的计算图文件。

3. 选取dump数据文件。

  1. **打开步骤2**中找到的计算图文件，记录第一个graph中的name字段值。如下示例中，记录“ge_default_20240613143502_1”。
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
```

```
graph {
  name: "ge_default_20240613143502_1"
  op {
    name: "atomic_addr_clean0_71"
    type: "AtomicAddrClean"
    attr {
      key: "_fe_imply_type"
      value {
        i: 6
      }
    }
  }
}

```
|  |  |
| --- | --- |

  2. 进入以时间戳命名的dump文件存放路径下，我们会看到该目录下存在几个文件夹：



  3. 找到前面记录的名称为name值的文件夹，例如ge_default_20240613143502_1，这些文件即为需要的dump数据文件。


*dump数据文件命名格式为：{op_type}.{op_name}.{task_id}.{stream_id}.{timestamp}*

对于如下产品，文件名还有可能为其他格式：

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

    - *{op_type}.{op_name_lxsliceN}.({stream_id}.){task_id}.{timestamp}.{task_type}.{context_id}.{thread_id}.{device_id}*
    - *{op_type}.{op_name}.({stream_id}.){task_id}.{timestamp}.{task_type}.{context_id}.{thread_id}.{device_id}*

    - dump数据文件如果op_type、op_name出现了“.”、“/”、“\”、空格时，则会转换为下划线表示。
    - 如果文件名称长度超过了OS文件名称长度限制（一般是255个字符），则会将该dump文件重命名为一串随机数字，映射关系可查看同目录下的mapping.csv。
    - 在图执行过程中，以下算子不会产生dump数据：
      - 在图执行前，已明确不会在Device侧执行的算子，如条件类算子(if/while/for/case等)、数据类算子(Data/RefData/Const等)、数据流算子(StackPush/StackPop/Concat/Split等)。
      - 在图优化阶段，被GE标记为不在Device侧执行的算子，这些算子在dump图中的attr的_no_task属性为true。
      - 图中不会到达最终执行分支的算子。

**父主题：**[GPU vs NPU（TensorFlow 1.15训练/在线推理）](atlasaccuracy_16_0005.html)