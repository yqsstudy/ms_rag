---
title: "如何进行dump数据文件Format转换"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0077.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0077.html"
---

# 如何进行dump数据文件Format转换

[本功能将在后续版本下线，当前版本推荐使用上文中的dump数据文件Format转换](atlasaccuracy_16_0054.html#ZH-CN_TOPIC_0000002536023787)。

#### 执行dump数据文件Format转换

本版本提供dump数据文件Format转换能力，用于用户根据自身需求将昇腾AI处理器生成的dump数据文件转换成numpy数据文件，方便查看。

该功能通过shape_conversion.py脚本实现，该脚本存放在${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。命令格式如下：

```
python3 shape_conversion.py -i <dump_file_path> -format <format> -o <output_path> [-shape <shape>] [-tensor <tensor>] [-index <index>] [-custom <custom_path>]
```

命令格式参数项说明：

- -i：昇腾AI处理器生成的dump文件（含路径）。
- [-format ：转换后的数据Format。支持的Format转换类型参见支持的Format转换类型](atlasaccuracy_16_0054.html#ZH-CN_TOPIC_0000002536023787__zh-cn_topic_0000002534483563_section816410197413)。
- -o：转换后的数据存放目录。
不建议配置与当前用户不一致的其它用户目录，避免提权风险。

- **-shape：Format转换需要的Shape，当前仅FRACTAL_NZ转换需要该Shape，格式为([0-9]+,)+[0-9]+**，每个数字必须大于0。可选。
- -tensor ：表示转换的dump文件是input数据还是output数据，默认为output。可选。
- -index：表示tensor的索引，默认为0。可选。
- -custom：用户自定义Format转换.py文件存放路径，需指定到“format_convert”目录的上一层目录。可选。.py文件相关要求参见准备自定义Format转换.py文件。
不建议调用与当前用户不一致的其它用户目录下的自定义脚本文件，避免提权风险。

#### 支持的Format转换类型

结果保存为“原始文件名.output.{index}.{shape}.npy”或“原始文件名.input.{index}.{shape}.npy”，Shape的格式如：1x3x224x224。

如果自定义的Format和内置的Format一样，以自定义Format为准。

当前内置的Format转换支持如下类型：

- FRACTAL_NZ转换NCHW
- FRACTAL_NZ转换ND
- HWCN转换FRACTAL_Z
- HWCN转换成NCHW
- HWCN转换成NHWC
- NC1HWC0转换成HWCN
- NC1HWC0转换成NCHW
- NC1HWC0转换成NHWC
- NCHW转换成FRACTAL_Z
- NCHW转换成NHWC
- NHWC转换成FRACTAL_Z
- NHWC转换成HWCN
- NHWC转换成NCHW
- NDC1HWC0转换成NCDHW

[一般情况下，非四维的Format是由四维Format转换而来，那么对于同一个非四维Format支持转换成多种Format类型的情况，该非四维Format只有重新转回原始的四维Format才有效。例如NC1HWC0支持转换成HWCN、NCHW、NHWC，但是被转换的NC1HWC0数据只有一种四维的原始数据，假设为HWCN，那么该NC1HWC0数据只能转换成HWCN。识别原始数据的Format类型需要了解《ATC离线模型编译工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/atctool/atlasatc_16_0031.html)[》中的“高级功能 > 单算子模型转换](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/atctool/atlasatc_16_0031.html)”。

#### 准备自定义Format转换.py文件

用户自定义的Format转换.py文件只能用来进行Format转换，文件安全性由用户自行保证。

为满足用户自定义Format转换，需要按以下要求准备：

- .py文件命名需满足规则：“convert_{format_from}_to_{format_to}.py”，其中，format_from和format_to支持的类型如下：
  - NCHW
  - NHWC
  - ND
  - NC1HWC0
  - FRACTAL_Z
  - NC1C0HWPAD
  - NHWC1C0
  - FSR_NCHW
  - FRACTAL_DECONV
  - C1HWNC0
  - FRACTAL_DECONV_TRANSPOSE
  - FRACTAL_DECONV_SP_STRIDE_TRANS
  - NC1HWC0_C04
  - FRACTAL_Z_C04
  - CHWN
  - DECONV_SP_STRIDE8_TRANS
  - NC1KHKWHWC0
  - BN_WEIGHT
  - FILTER_HWCK
  - HWCN
  - LOOKUP_LOOKUPS
  - LOOKUP_KEYS
  - LOOKUP_VALUE
  - LOOKUP_OUTPUT
  - LOOKUP_HITS
  - MD
  - NDHWC
  - C1HWNCoC0
  - FRACTAL_NZ

- .py文件内容需满足以下规则：
```
1
2
3
```

```
def convert(shape_from, shape_to, array):
    
    return numpy_array

```
|  |  |
| --- | --- |

参数说明：

  - shape_from：array数据的转换前的Shape，一维数组。
  - shape_to：array数据的转换后的Shape，一维数组。（可选）。
  - array：一维原始数据。
  - 返回值：转换后的numpy数组。

- .py文件存放目录需满足：
.py文件必须存放在“format_convert”目录下，如果该目录不存在，需要新建。

**父主题：**[原compare_vector.py精度比对方式](atlasaccuracy_16_0065.html)