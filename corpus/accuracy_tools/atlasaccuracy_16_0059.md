---
title: "生成npy文件名异常情况批量处理"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0059.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0059.html"
---

# 生成npy文件名异常情况批量处理

TensorFlow模型生成dump数据时，因tfdbg自身原因或运行环境原因，会出现tfdbg截断算子名，导致生成的npy文件名与预期不符，造成转换dump数据文件异常。

需要参考以下方法重新生成npy文件，使得npy文件名符合精度比对要求。

- 本文中脚本名称、路径等均为举例，请根据实际替换。
- 批量处理后，如果遇到某算子的dump文件存在，但是比对结果为NaN，需要检查该算子的dump文件名中的{op_name}是否与TensorFlow算子名称一致，如果不一致需要手动修改dump文件名中的算子字段与TensorFlow算子名称一致。其中如果出现"/"请修改为"_"。

1. 执行TensorFlow工程。

进入调试命令行交互模式后，输入run命令。

2. **执行lt > tensor_name**命令将所有tensor的名称暂存到文件里。
3. **创建可执行脚本，如pt_cmd.sh，获取tensor_name**文件中tensor_name对应的tensor_index。

脚本内容如下：

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
#!/bin/bash
timestamp=$[$(date +%s%N)/1000]
index=1
while read -r line
do
  tensor_index=`echo $line | awk '{print $4}'`
  echo "pt "$tensor_index" -n 0 -w "$((index++))"."$timestamp".npy" >> $2
done < $1

```
|  |  |
| --- | --- |

赋予pt_cmd.sh可执行权限并执行脚本。

**bash***pt**_cmd.sh tensor_name tensor_name.txt*

4. ***回到tfdbg命令行，输入run命令后，将上一步生成的tensor_name.txt***文件内容粘贴执行，生成npy文件。
5. 将生成的npy文件，移动到新的文件夹，如npy_dir。
6. 创建可执行脚本，如index_to_tensorname.sh，并执行脚本批量修改npy文件名。

脚本内容如下：

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
```

```
#!/bin/bash
timestamp=$[$(date +%s%N)/1000]
while read -r line
do
  tensor_index=`echo $line | awk '{print $2}'`
  real_file=`echo $line | awk '{print $6}'`
  changed1_tensor_index=${tensor_index//\//_}
  changed2_tensor_index=${changed1_tensor_index//:/.}
  echo $2/$real_file $2/$changed2_tensor_index"."$timestamp".npy"
  if [ -r $2/$real_file ]
  then
    mv $2/$real_file $2/$changed2_tensor_index"."$timestamp".npy"
  fi
done < $1

```
|  |  |
| --- | --- |

赋予index_to_tensorname.sh可执行权限并执行脚本。

**bash***index_to_tensorname.sh**tensor_name.txt npy_dir*

**父主题：**[扩展功能](atlasaccuracy_16_0051.html)