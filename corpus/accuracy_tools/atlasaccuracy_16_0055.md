---
title: "查看dump数据文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0055.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0055.html"
---

# 查看dump数据文件

dump文件无法通过文本工具直接查看其内容，为了查看dump文件内容，本文提供以下脚本将dump文件转换为numpy格式文件后，再通过numpy官方提供的能力转为txt文档进行查看。

该功能通过msaccucmp.py脚本实现，脚本存放在${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。

```
python3 msaccucmp.py convert -d <dump_file> [-out <output>] [-v <version>] [-t <type>]
```

命令格式参数项说明如表1所示。
**表1**参数说明
**参数名**

**描述**

是否必选

-d

--dump_file

昇腾AI处理器生成的dump文件。

支持指定单个文件；单个路径（不支持递归嵌套，只支持文件的父目录）；同时指定多个文件，文件名用逗号隔开，例如-d /{PATH}/dump_file1,/{PATH}/dump_file2。

是

-out

--output

转换后的数据存放目录，默认为当前路径。

不建议配置与当前用户不一致的其它用户目录，避免提权风险。

否

-v

--version

dump文件类型，1代表protobuf序列化后的数据文件，2代表自定义格式的数据文件。默认取值为2。

否

-t

--type

输出文件的类型。取值为：

- npy：输出文件保存为numpy格式。npy文件不支持bfloat16格式，若工具输入源文件为bfloat16格式，则会将其解析为float32格式的npy文件。
- msnpy：输出文件保存为numpy格式，一般用于MindSpore场景。
- bin：输出文件保存为binary格式。

默认值为npy。

否
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 操作步骤

1. 使用安装用户登录开发环境。
2. 进入${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
3. 执行msaccucmp.py脚本，转换dump数据文件为numpy格式文件。
******
```
python3 msaccucmp.py convert -d $HOME/dump -out $HOME/dumptonumpy -v 2
```

  - [msaccucmp.py脚本的各个输入参数使用方法，请参见dump数据文件Format转换](atlasaccuracy_16_0054.html#ZH-CN_TOPIC_0000002536023787)。
  - -d参数支持传入单个文件，对单个dump文件进行转换，也支持传入目录（不支持递归嵌套，只支持文件的父目录），对整个path下所有的dump文件进行转换。

4. 调用Python，转换numpy文件为txt文件。举例：

```
$ python3
Python 3 (default, Mar  5 2020, 16:07:54)[GCC 5.4.0 20160609] on linuxType "help", "copyright", "credits" or "license" for more information.
>>> import numpy as np
>>> a = np.load("$HOME/dumptonumpy/Pooling.pool1.1.1147.1589195081588018.output.0.npy")
>>> b = a.flatten()
>>> np.savetxt("$HOME/dumptonumpy/Pooling.pool1.1.1147.1589195081588018.output.0.txt", b)
```

转换为.txt格式文件后，维度信息、dtype均不存在。详细的使用方法请参见NumPy官网介绍。

**父主题：**[扩展功能](atlasaccuracy_16_0051.html)