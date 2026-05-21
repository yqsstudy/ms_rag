---
title: "准备离线模型dump数据文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0068.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0068.html"
---

# 准备离线模型dump数据文件

#### 前提条件

[在准备dump数据前，请参见《ATC离线模型编译工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/atctool/atlasatc_16_0031.html)[》模型转换，准备好模型文件；如果涉及模型量化，请参见《AMCT模型压缩工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/amct/atlasamct_16_0001.html)》完成量化操作后再进行模型转换，生成量化的模型文件。并请配套生成的模型文件完成应用工程的编译、运行，确保工程正常。

- 执行AMCT时，同步会生成量化融合规则文件，该文件在精度比对时会使用。
- Docker场景下，不支持将容器作为运行环境使用dump功能。
- **提供aclInit()****接口和aclmdlSetDump()**接口两种接口方式dump数据。
  - **aclInit()**[接口的详细使用方法请参见《应用开发指南 (C&C++)](https://www.hiascend.com/document/detail/zh/canncommercial/850/appdevg/acldevg/aclcppdevg_000000.html)[》中的“aclInit](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/appdevgapi/aclcppdevg_03_0022.html)”。
  - **aclmdlSetDump()**[接口的详细使用方法请参见“aclmdlSetDump](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/appdevgapi/aclcppdevg_03_0315.html)”。

#### dump数据

参考以下步骤进行离线模型dump操作：

1. **打开工程文件，查看调用的aclInit()****或aclmdlSetDump()**函数，获取acl.json文件路径。

如果aclInit()或aclmdlSetDump()初始化为空，则需要修改该函数，补充步骤2创建的acl.json路径。这里的acl.json路径是相对工程编译生成的二进制文件的路径。

2. 在查到的目录下修改acl.json文件（如不存在，则需要新建，建议放在工程编译后的out目录下），添加dump配置，格式如下所示。

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
		"dump_op_switch":"off"
	}                                                                                        
}

```
|  |  |
| --- | --- |
acl.json文件配置dump规则说明：
  - 样例中的dump、dump_list、dump_path为必选字段；model_name、layer、dump_mode、dump_op_switch为可选字段。
  - 当需要dump模型的所有算子时，不需要包含layer字段。
  - 当需要dump指定的部分算子时，按格式配置layer字段，每行配置模型中的一个算子名，且每个算子之间用英文逗号隔开。
  - 如果存在多个模型需要dump，则需要为每个模型创建dump配置，且每个模型之间用英文逗号隔开。
  - 如果仅dump单算子模型时，则dump_list为空，dump_op_switch配置为on。
acl.json文件配置项说明：
  - dump_list：需要dump数据的整网模型列表。
    - model_name：模型名称。
[模型加载方式为文件加载时，填入模型文件的名称，不需要带后缀名，也可以配置为ATC模型文件转换后的json文件里的最外层"name"字段对应值；模型加载方式为内存加载时，配置为模型文件转换后的json文件里的“"name"”字段对应值。模型加载方式说明请参见“acl API（C）](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/appdevgapi/aclcppdevg_03_0020.html)”章节的内容。

    - layer：算子名。

  - dump_path：dump数据文件存储到运行环境{dump_path}目录下的路径。
支持配置绝对路径或相对路径（相对执行命令行时的当前路径）：

    - 绝对路径配置以“/”开头，例如：/home/output。
    - 相对路径配置直接以目录名开始，例如：output。

例如：dump_path配置为/home/output，则dump数据文件存储到运行环境的/home/output目录下。

该参数指定的目录需要提前创建且确保安装时配置的运行用户具有读写权限。

  - dump_mode：dump数据模式，取值范围：input、output和all，默认取output。可选。
    - input：dump算子的输入数据。
    - output：dump算子的输出数据。
    - all：同时dump算子的输入、输出数据。

  - dump_op_switch：单算子模型dump数据开关。取值范围：on和off。默认取值off。可选。
    - on：开启单算子模型dump。
    - off：关闭单算子模型dump。


  - 不具有输出的TBE算子、AI CPU算子，如StreamActive、Send、Recv、const等不会生成dump数据；编译后的模型中部分算子并不会在AI CPU或AI Core执行，如concatD类型算子，则无法生成dump数据。
  - 采用dump部分算子场景下，因data算子不会在AI CPU或AI Core上执行，如果用户填写dump data节点算子时需要一并填写data节点算子的后继节点，才能dump出data节点算子数据。
  - 按格式填写acl.json文件时，请确保各个模型的model_name值唯一。
  - 模型加载方式为文件加载时，model_name除了可以配置为模型文件名外，也可以配置为模型文件转换后的json文件里的“"name"”字段对应值。模型名称获取方式（同时可以获取到各个算子名）：
如果acl.json文件里model_name配置项值同时包括模型文件名、此处获取的name值，以模型文件名的配置项生效。

1. 运行应用工程，生成dump数据文件。

工程运行完毕后，可以在运行环境{dump_path}路径下查看到生成的dump数据文件。生成的路径及格式说明：

```
{dump_path}/{time}/{device_id}/{model_name}/{model_id}/{data_index}/{dump文件}
```

单算子模型dump时，路径为：

```
{dump_path}/{device_id}/{op_name}/{dump文件}
```

  - time：dump数据文件落盘的时间。格式为：YYYYMMDDHHMMSS。
  - device_id：设备ID。
  - model_name：模型名称。
  - model_id：模型ID号。
  - data_index：针对每个Task ID执行的次数维护一个序号，从0开始计数，该Task每dump一次数据，序号递增1。
  - dump文件：命名规则如{op_type}.{op_name}.{task_id}.{timestamp}

如果model_name、op_type、op_name出现了“.”、“/”、“\”、空格时，转换为下划线表示。

**父主题：**[比对数据准备](atlasaccuracy_16_0066.html)