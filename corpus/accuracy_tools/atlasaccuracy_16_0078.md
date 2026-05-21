---
title: "如何查看dump数据文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0078.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0078.html"
---

# 如何查看dump数据文件

[本功能将在后续版本下线，当前版本推荐使用上文中的查看dump数据文件](atlasaccuracy_16_0055.html#ZH-CN_TOPIC_0000002536143821)。

dump文件无法通过文本工具直接查看其内容，为了查看dump文件内容，本文提供以下脚本将dump文件转换为numpy格式文件后，再通过numpy官方提供的能力转为txt文档进行查看：

1. 使用安装用户登录开发环境。
2. 进入${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
3. 执行dump_data_conversion.py脚本，转换dump文件为numpy文件。举例：
**********
```
python3 dump_data_conversion.py -target numpy -type offline -i $HOME/dump -o $HOME/dumptonumpy
```

[dump_data_conversion.py脚本的各个输入参数使用方法，请参见如何进行npy文件转dump文件](atlasaccuracy_16_0076.html#ZH-CN_TOPIC_0000002504184018)。

4. 调用Python，转换numpy文件为txt文件。举例：

```
1
2
3
4
5
6
```

```
$ python3
Python 3 (default, Mar  5 2020, 16:07:54)[GCC 5.4.0 20160609] on linuxType "help", "copyright", "credits" or "license" for more information.
>>> import numpy as np
>>> a = np.load("$HOME/dumptonumpy/Pooling.pool1.1.1147.1589195081588018.output.0.npy")
>>> b = a.flatten()
>>> np.savetxt("$HOME/dumptonumpy/Pooling.pool1.1.1147.1589195081588018.output.0.txt", b)

```
|  |  |
| --- | --- |

转换为.txt格式文件后，维度信息、dtype均不存在。详细的使用方法请参考NumPy官网介绍。

**父主题：**[原compare_vector.py精度比对方式](atlasaccuracy_16_0065.html)