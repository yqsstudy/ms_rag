---
title: "如何进行npy文件转dump文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0076.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0076.html"
---

# 如何进行npy文件转dump文件

[本功能将在后续版本下线，当前版本推荐使用上文中的dump数据文件Format转换](atlasaccuracy_16_0054.html#ZH-CN_TOPIC_0000002536023787)。

#### 转换Caffe模型npy文件为dump数据文件

获取到Caffe原始数据后，通过dump_data_conversion.py脚本进行数据转换，输出二进制格式的dump文件。命令行格式如下：
********
```
python3 dump_data_conversion.py -type type -target target -i input_path -o output_path
```

- -type：数据类型，必选参数。参数值选项：
  - quant：量化Caffe模型数据。
  - tf：非量化TensorFlow模型数据。
  - caffe：非量化Caffe模型数据。
  - offline：离线模型数据。

- -target：数据转换目标格式，参考值选项：numpy和dump。必选参数。
  - numpy：dump文件转换为numpy文件。
  - dump：numpy文件转换为dump文件。

- -i：数据文件路径（可以是文件夹或者文件），必选参数。
  - numpy文件转换为dump文件：
*如果“-i”参数输入是文件夹，则格式要求如下：文件夹下的文件必须是{op_name}.{output_index}.{timestamp}*.npy格式文件。

*如果“-i”参数输入是文件名，则输入的文件名需满足{op_name}.{output_index}.{timestamp}*.npy格式要求。每次仅支持输入1个文件。

其中op_name对应的名称需满足“A-Za-z0-9_-”正则表达式规则，output_index由0~9数字组成，timestamp为16位时间戳。

  - dump文件转numpy文件：
[“-i”参数输入的文件夹或文件名格式必须满足数据格式要求](atlasaccuracy_16_0067.html#ZH-CN_TOPIC_0000002536143827)章节要求。

- -o：转换后输出文件路径。必选参数。
不建议配置与当前用户不一致的其它用户目录，避免提权风险。

Caffe原始数据（numpy文件）转dump数据文件命令举例：
********
```
python3 dump_data_conversion.py -type caffe -target dump -i $HOME/caffenpyfile -o $HOME/caffedump
```

- dump_data_conversion.py脚本存放在${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
- 使用该脚本进行数据转换，确保主机内存大小不低于15GB；如果待转换的dump数据单个文件大小超过441MB，则建议使用更大内存主机。

#### TensorFlow模型npy文件转换dump数据文件

获取到TensorFlow原始数据后，通过dump_data_conversion.py脚本进行数据转换，输出二进制格式的dump文件。命令行格式如下：
********
```
python3 dump_data_conversion.py -type type -target target -i input_path -o output_path
```

TensorFlow原始数据（npy文件）转dump数据文件的命令举例：

- -type：数据类型，必选参数。参数值选项：
  - quant：量化Caffe模型数据。
  - tf：非量化TensorFlow模型数据。
  - caffe：非量化Caffe模型数据。
  - offline：离线模型数据。

- -target：数据转换目标格式，参考值选项：numpy和dump。必选参数。
  - numpy：dump文件转换为numpy文件。
  - dump：numpy文件转换为dump文件。

- -i：数据文件路径（可以是文件夹或者文件），必选参数。
  - numpy文件转换为dump文件：
*如果“-i”参数输入是文件夹，则格式要求如下：文件夹下的文件必须是{op_name}.{output_index}.{timestamp}*.npy格式文件。

*如果“-i”参数输入是文件名，则输入的文件名需满足{op_name}.{output_index}.{timestamp}*.npy格式要求。每次仅支持输入1个文件。

其中op_name对应的名称需满足“A-Za-z0-9_-”正则表达式规则，output_index由0~9数字组成，timestamp为16位时间戳。

  - dump文件转numpy文件：
[“-i”参数输入的文件夹或文件名格式必须满足数据格式要求](atlasaccuracy_16_0067.html#ZH-CN_TOPIC_0000002536143827)章节要求。

- -o：转换后输出文件路径。必选参数。
不建议配置与当前用户不一致的其它用户目录，避免提权风险。

TensorFlow原始数据（numpy文件）转dump数据文件命令举例：
********
```
python3 dump_data_conversion.py -type tf -target dump -i $HOME/tfnpyfile -o $HOME/tfdump
```

- dump_data_conversion.py脚本存放在/home/xxx/Ascend/cann/tools/operator_cmp/compare路径下。
- 使用该脚本进行数据转换，确保主机内存大小不低于15GB；如果待转换的dump数据单个文件大小超过441MB，则建议使用更大内存主机。
**父主题：**[原compare_vector.py精度比对方式](atlasaccuracy_16_0065.html)