---
title: "算子工程编译"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_10_0089.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_10_0089.html"
---

# 算子工程编译

#### 简介

算子交付件开发完成后，需要对算子工程进行编译，生成自定义算子安装包*.run，详细的编译操作包括：

- 将AI CPU算子代码实现文件*.h与*.cc编译成libcust_aicpu_kernels.so。
- 将算子信息库定义文件*.ini编译成*.json。
- 将原型定义文件*.h与*.cc编译成libcust_op_proto.so。
- *将TensorFlow/Caffe/ONNX算子的适配插件实现文件*.h与*.cc编译成libcust_{tf|caffe|onnx**}*_parsers.so。

#### 命令行环境

- 不建议对样例工程或自动生成的编译配置文件进行修改，否则可能会造成自定义算子运行失败。
- 编译生成算子包的操作系统版本与架构需要与执行算子包部署操作的操作系统版本与架构相同。

1. 在自定义算子工程的“custom.proto”文件中增加原始框架为Caffe的自定义算子的定义。

若开发其他框架的算子，此步骤无需操作，custom.proto文件如下所示：
**********************************
```
syntax = "proto2";
package domi.caffe;
message NetParameter {
  optional string name = 1; 
  // LayerParameter定义，保持默认，用户无需修改
  repeated LayerParameter layer = 100;  // ID 100 so layers are printed last.

}
message LayerParameter {
  optional string name = 1;  // 模型解析所需要定义，保持默认，用户无需修改。
  optional string type = 2;  // 模型解析所需要定义，保持默认，用户无需修改。

  // 在LayerParameter中添加自定义算子层的定义，ID需要保持唯一，取值原则为：不与内置caffe.proto中编号重复，且小于5000。
  // 内置的caffe.proto存储路径为CANN软件安装后文件存储路径的“include/proto/caffe.proto”。
  optional CustomTest1Parameter custom_test1_param = 1000;  
  optional CustomTest2Parameter custom_test2_param = 1001;  
}

// 增加自定义算子层的定义
message CustomTest1Parameter {
    optional bool adj_x1 = 1 [default = false];
    optional bool adj_x2 = 2 [default = false];
}
//若自定义算子中无属性进行解析映射，则message xxParameter定义保持空，如下所示：
message CustomTest2Parameter {
}
```

Parameter的类型（粗斜体部分）建议保持唯一，不与内置caffe.proto（CANN软件安装后文件存储路径下的“include/proto/caffe.proto”）定义重复。

2. 修改build.sh脚本，配置算子编译所需环境变量。

  - ASCEND_TENSOR_COMPILER_INCLUDE：CANN软件头文件所在路径。
 
 请取消此环境变量的注释，并修改为CANN软件头文件所在路径，例如：
```
export ASCEND_TENSOR_COMPILER_INCLUDE=${INSTALL_DIR}/include
```

${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。

  - TOOLCHAIN_DIR：AI CPU算子使用的编译器路径，请取消此环境变量的注释，并按照下述描述修改。
    - 针对Ascend EP场景，请配置为HCC编译器所在路径，例如：
```
export TOOLCHAIN_DIR=${INSTALL_DIR}/toolkit/toolchain/hcc
```

${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。

  - AICPU_KERNEL_TARGET：AI CPU算子实现文件编译生成的动态库文件名称。
    - 建议用户取消此环境变量的注释，并在动态库文件的名称中添加自定义唯一后缀作为标识，例如使用软件版本号作为后缀，避免后续由于AI CPU软件升级造成自定义AI CPU动态库文件的冲突。注意，配置的动态库文件的名称长度不能超过84个字节。例如：**
```
export AICPU_KERNEL_TARGET=cust_aicpu_kernels_3.3.0
```

    - 若不配置此环境变量，使用默认值：cust_aicpu_kernels。

  - AICPU_SOC_VERSION：请选择实际硬件平台对应的昇腾AI处理器的类型。
  - vendor_name：标识自定义算子所属厂商的名称，默认值为"customize"。建议开发者自行指定所属厂商名称，避免和其他厂商提供的算子包冲突。当前TBE自定义算子工程中算子实现代码文件所在的目录名为impl，算子包部署后，为避免多厂商的算子实现Python包名冲突，所在的目录名会修改为${vendor_name}_impl的格式。

3. 执行算子工程编译。

  - [若您是基于《TBE&AI CPU算子开发指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/tbeaicpudevg/atlasopdev_10_0001.html)[》的基于算子样例](nottoctopics/zh-cn_topic_0000002502730932.html)创建的工程，编译方法如下：
    - 若您只需要编译TBE算子，请在算子工程目录下执行如下命令。
**chmod +x build.sh**

**./build.sh -t**

    - 若您只需要编译AI CPU算子，请在算子工程目录下执行如下命令。
**chmod +x build.sh**

**./build.sh -c**

    - 若您既需要编译TBE算子，又需要编译AI CPU算子，请在算子工程目录下执行如下命令。
**chmod +x build.sh**

**./build.sh**

  - [若您是算子工程创建（msOpGen）](atlasopdev_16_0017.html#ZH-CN_TOPIC_0000002536800491)创建的工程，编译方法如下：
在算子工程目录下执行如下命令：

**chmod +x build.sh**

**./build.sh**

***编译成功后，会在当前目录下创建build_out目录，并在build_out目录下生成自定义算子安装包custom_opp_<target_os>_<target_architecture>*.run**。

**若重新进行工程编译，请先执行./build.sh clean**命令进行编译文件的清理。

**父主题：**[算子编译部署](atlasopdev_10_0087.html)