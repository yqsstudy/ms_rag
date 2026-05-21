---
title: "准备离线模型dump数据文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0028.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0028.html"
---

# 准备离线模型dump数据文件

#### 使用前须知

- 请在dump数据前，完成模型对应的应用工程的编译、运行，确保工程正常。
- 每次推理都会产生dump数据，在循环次数较多时，每次推理产生的dump数据量会相应增加，建议dump数据时仅执行一次推理。对于大模型场景，通常dump数据量庞大且耗时较长，可以通过dump_data开启算子统计功能，根据统计数据识别可能异常的算子，然后仅针对这些可能异常的算子进行dump。
- Docker场景下，不支持将容器作为运行环境使用dump功能。
- **提供aclInit()****接口和aclmdlSetDump()**接口两种接口方式dump数据。
  - **aclInit()**[接口的详细使用方法请参见“aclInit](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/appdevgapi/aclcppdevg_03_0022.html)”。
  - **aclmdlSetDump()**[接口的详细使用方法请参见“aclmdlSetDump](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/appdevgapi/aclcppdevg_03_0315.html)”。

#### dump数据

参考以下步骤进行离线模型dump操作：

1. **打开aclInit()****函数所在的推理应用工程代码文件，查看调用的aclInit()****或aclmdlSetDump()**函数，获取acl.json文件路径。

如果aclInit()或aclmdlSetDump()初始化为空，则需要修改该函数，补充步骤2创建的acl.json路径。这里的acl.json路径是相对工程编译生成的二进制文件的路径。

2. 在查到的目录下修改acl.json文件（如不存在，则需要新建，建议放在工程编译后的out目录下），添加dump配置，格式如下所示。
模型推理场景下，开启dump数据采集：
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
```

```
{                                                                                            
	"dump":{
		"dump_list":[                                                                        
			{	"model_name":"ResNet-101"
			},
			{                                                                                
				"model_name":"ResNet-50",
				"layer":[
				      "conv1conv1_relu",
				      "res2a_branch2ares2a_branch2a_relu",
				      "res2a_branch1",
				      "pool1"
				] 
			}  
		],  
		"dump_path":"/home/output",
                "dump_mode":"output",
		"dump_op_switch":"off",
                "dump_data":"tensor"
	}                                                                                        
}

```
|  |  |
| --- | --- |

单算子调用场景下，开启dump数据采集：

```
1
2
3
4
5
6
7
8
```

```
{
    "dump":{
        "dump_path":"/home/output",
        "dump_list":[{}], 
	"dump_op_switch":"on",
        "dump_data":"tensor"
    }
}

```
|  |  |
| --- | --- |
**表1**acl.json文件格式说明
配置项

参数说明

dump_list

（必选）待dump数据的整网模型列表。

  - 模型推理场景下，当需要Dump全部算子时，配置为：
```
"dump_list":[{}]
```

当需要Dump多个模型或特定算子时，需要结合model_name和layer使用。

  - 在单算子调用场景（包括单算子模型执行和单算子API执行）下，dump_list建议配置为：
```
"dump_list":[{}]
```

model_name

模型名称，各个模型的model_name值须唯一。

  - 模型加载方式为文件加载时，填入模型文件的名称，不需要带后缀名；也可以配置为ATC模型文件转换后的json文件里的最外层"name"字段对应值。
  - 模型加载方式为内存加载时，配置为ATC模型文件转换后的json文件里的最外层"name"字段对应值。

layer

IO性能较差时，可能会因为数据量过大而导致执行超时，因此不建议进行全量dump，请指定算子进行dump。通过该字段可以指定需要dump的算子名，支持指定为ATC模型转换后的算子名，也支持指定为转换前的原始算子名，配置时需注意：

  - 需按格式配置，每行配置模型中的一个算子名，且每个算子之间用英文逗号隔开。
  - 用户可以无需设置model_name，此时会默认dump所有model下的相应算子。如果配置了model_name，则dump对应model下的相应算子。
  - 若指定的算子其输入涉及data算子，会同时将data算子信息dump出来；若需dump data算子，需要一并填写data节点算子的后继节点，才能dump出data节点算子数据。
  - 当需要dump模型中所有算子时，不需要包含layer字段。

optype_blacklist

配置dump数据黑名单，黑名单中的指定类型的算子的输入或输出数据不会进行数据dump，用户可通过该配置控制dump的数据量。

该功能仅在执行模型数据dump操作，且dump_level为op时生效，同时支持和opname_blacklist配合使用。

配置示例：

```
{
	"dump":{
		"dump_list":[     
			{                                                                                
				"model_name":"ResNet-50",
				"optype_blacklist":[
				    {
					  "name":"conv"
					  "pos":["input0", "input1"]
					} 
				] 
			}
		],  
		"dump_path":"/home/output",
                "dump_mode":"input",
	}  
}
```

以上示例表示：不对conv算子的input0数据和input1数据执行dump操作，conv为算子类型。

optype_blacklist中包括name和pos字段，配置时需注意：

  - name表示算子类型，支持指定为ATC模型转换后的算子类型，配置为空时该过滤项不生效。
  - pos表示算子的输入或输出，仅支持配置为inputn或outputn格式，其中n表示输入输出索引号。配置为空时该过滤项不生效。
  - optype_blacklist内最多支持配置100个过滤项。
  - 如果配置了model_name，则仅对该model下的算子生效。如果不配置model_name，则对所有model下的算子生效。

opname_blacklist

配置dump数据黑名单，黑名单中的指定名称的算子的输入或输出数据不会进行数据dump，用户可通过该配置控制dump的数据量。

该功能仅在执行模型数据dump操作，且dump_level为op时生效，同时支持和optype_blacklist配合使用。

配置示例：

```
{
	"dump":{
		"dump_list":[     
			{                                                                                
				"model_name":"ResNet-50",
				"opname_blacklist":[
				    {
					  "name":"conv"
					  "pos":["input0", "input1"]
					} 
				] 
			}
		],  
		"dump_path":"/home/output",
                "dump_mode":"input",
	}  
}
```

以上示例表示：不对conv算子的input0数据和input1数据执行dump操作，conv为算子名称。

opname_blacklist中包括name和pos字段，配置时需注意：

  - name表示算子名称，支持指定为ATC模型转换后的算子名称，配置为空时该过滤项不生效。
  - pos表示算子的输入或输出，仅支持配置为inputn或outputn格式，其中n表示输入输出索引号。配置为空时该过滤项不生效。
  - opname_blacklist内最多支持配置100个过滤项。
  - 如果配置了model_name，则仅对该model下的算子生效。如果不配置model_name，则对所有model下的算子生效。

opname_range

配置dump数据范围，对begin到end闭区间内的数据执行dump操作。

该功能仅在执行模型数据dump操作，且dump_level为op时生效。

配置示例：

```
{
	"dump":{
		"dump_list":[
			{
				"model_name":"ResNet-50",
				"opname_range":[{"begin":"conv1", "end":"relu1" }, {"begin":"conv2", "end":"pool1"}]
			}
		],
		"dump_mode":"output",
        "dump_level": "op",
        "dump_path":"/home/output"
	}
}
```

以上示例表示对conv1到relu1、conv2到pool1闭区间内的数据执行dump操作，conv1、relu1、conv2、pool1表示算子名称。

配置时需注意：

  - model_name不允许为空。
  - begin和end中的参数表示算子名称，支持指定为ATC模型转换后的算子名称。
  - begin和end不允许为空，且只能配置为非data算子；若begin和end范围内算子的输入涉及data算子，会同时对data算子信息执行dump操作。

dump_path

（必选）dump数据文件存储到运行环境的目录，该目录需要提前创建且确保安装时配置的运行用户具有读写权限。
支持配置绝对路径或相对路径：
  - 绝对路径配置以“/”开头，例如：/home/output。
  - 相对路径配置直接以目录名开始，例如：output。

dump_mode

dump数据模式。

  - input：dump算子的输入数据。
  - output：dump算子的输出数据，默认取值output。
  - all：dump算子的输入、输出数据。
注意，配置为all时，由于部分算子在执行过程中会修改输入数据，例如集合通信类算子HcomAllGather、HcomAllReduce等，因此系统在进行dump时，会在算子执行前dump算子输入，在算子执行后dump算子输出，这样，针对同一个算子，算子输入、输出的dump数据是分开落盘，会出现多个dump文件，在解析dump文件后，用户可通过文件内容判断是输入还是输出。

dump_level

dump数据级别，取值：

  - op：按算子级别dump数据。
  - kernel：按kernel级别dump数据。
  - all：默认值，op和kernel级别的数据都dump。

默认配置下，dump数据文件会比较多，例如有一些aclnn开头的dump文件，若用户对dump性能有要求或内存资源有限时，则可以将该参数设置为op级别，以便提升dump性能、精简dump数据文件数量。

**说明**：算子是一个运算逻辑的表示（如加减乘除运算），kernel是运算逻辑真正进行计算处理的实现，需要分配具体的计算设备完成计算。

dump_op_switch

单算子调用场景（包括单算子模型执行和单算子API执行）下，是否开启dump数据采集。

  - on：开启。
  - off：关闭，默认取值off。

dump_step

指定采集哪些迭代的dump数据。推理场景无需配置。

不配置该参数，默认所有迭代都会产生dump数据，数据量比较大，建议按需指定迭代。

多个迭代用“|”分割，例如：0|5|10；也可以用“-”指定迭代范围，例如：0|3-5|10。

配置示例：

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
```

```
{
	"dump":{
		"dump_list":[     
			...... 
		],  
		"dump_path":"/home/output",
                "dump_mode":"output",
		"dump_op_switch":"off",
                "dump_step": "0|3-5|10"
	}  
}

```
|  |  |
| --- | --- |

[训练场景下，若通过acl.json中的dump_step参数指定采集哪些迭代的dump数据，又同时在GEInitialize接口中配置了ge.exec.dumpStep参数（该参数也用于指定采集哪些迭代的dump数据），则以最后配置的参数为准。GEInitialize接口的详细介绍请参见《图模式开发指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/graph/graphdevg/atlasag_25_0081.html)[》的“GEInitialize](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendgraphapi/atlasgeapi_07_0086.html)”。

dump_data

算子dump内容类型，取值：

  - tensor: dump算子数据，默认为tensor。
  - stats: dump算子统计数据，结果文件为csv格式，文件中包含算子名称、输入/输出的数据类型、最大值、最小值等。

通常dump数据量太大并且耗时长，可以先对算子统计数据进行dump，根据统计数据识别可能异常的算子，然后再dump算子数据。

dump_stats

仅Atlas A2 训练系列产品/Atlas A2 推理系列产品支持该参数，当dump_data=stats时，可通过本参数设置收集统计数据中的哪一类数据，本参数取值如下（若不指定取值，默认采集Max、Min、Avg、Nan、Negative Inf、Positive Inf数据）：

  - Max：dump算子统计数据中的最大值。
  - Min：dump算子统计数据中的最小值。
  - Avg：dump算子统计数据中的平均值。
  - Nan：dump算子统计数据中未定义或不可表示的数值，仅针对浮点类型half、bfloat、float。
  - Negative Inf：dump算子统计数据中的负无穷值，仅针对浮点类型half、bfloat、float。
  - Positive Inf：dump算子统计数据中的正无穷值，仅针对浮点类型half、bfloat、float。
  - L2norm：dump算子统计数据的L2Norm值。

配置示例：

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
```

```
{
    "dump":{
	"dump_list":[     
		...... 
	],  
        "dump_path":"/home/output",
        "dump_mode":"output",
        "dump_data":"stats",
        "dump_stats":["Max", "Min"]
    }
}

```
|  |  |
| --- | --- |

3. 运行应用程序，生成dump数据文件，生成的路径及格式说明如下。

*模型推理场景下，dump数据落盘路径为：{dump_path}**/{time}**/{device_id}**/{model_name}**/{model_id}**/{data_index}**/{dump文件}*

*单算子调用场景（包括单算子模型执行和单算子API执行）下，dump数据落盘路径为：{dump_path}**/{time}**/{device_id}**/{dump文件}*
**表2**dump数据文件路径说明
路径key

说明

备注

dump_path

acl.json中配置的dump数据文件存储目录。

*dump数据文件命名格式为：{op_type}.{op_name}.{task_id}.{stream_id}.{timestamp}*

time

dump数据文件落盘的时间。

格式为：YYYYMMDDHHMMSS

device_id

设备ID。

-

model_name

模型名称。

如果model_name出现了“.”、“/”、“\”、空格时，转换为下划线表示。

model_id

模型ID号。

-

data_index

针对每个Task ID执行的次数维护一个序号，从0开始计数，该Task每dump一次数据，序号递增1。

-
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

  - dump数据文件如果op_type、op_name出现了“.”、“/”、“\”、空格时，则会转换为下划线表示。
  - 如果文件名称长度超过了OS文件名称长度限制（一般是255个字符），则会将该dump文件重命名为一串随机数字，映射关系可查看同目录下的mapping.csv。
  - 在图执行过程中，以下算子不会产生dump数据：
    - 在图执行前，已明确不会在Device侧执行的算子，如条件类算子(if/while/for/case等)、数据类算子(Data/RefData/Const等)、数据流算子(StackPush/StackPop/Concat/Split等)。
    - 在图优化阶段，被GE标记为不在Device侧执行的算子，这些算子在dump图中的attr的_no_task属性为true。
    - 图中不会到达最终执行分支的算子。

**父主题：**[NPU vs NPU（离线推理）](atlasaccuracy_16_0032.html)