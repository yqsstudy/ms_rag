---
title: "准备GPU侧npy文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0006.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0006.html"
---

# 准备GPU侧npy文件

#### 使用前须知

- 在通过执行TensorFlow 1.15原始网络训练/在线推理来获取npy文件前，要求有一套完整、可执行的标准TensorFlow模型训练/在线推理工程。
- 不论采用Estimator模式还是session.run模式，首先要把脚本中所有的随机全部关闭，包括但不限于对数据集的shuffle，参数的随机初始化，以及某些算子的隐性随机初始化（比如dense算子），确认用户脚本内所有参数均非随机初始化。

#### 生成npy文件

利用TensorFlow官方提供的debug工具tfdbg生成npy文件。详细的操作方法如下：

1. 修改TensorFlow训练/在线推理脚本，添加debug选项设置。

  - 如果采用Estimator模式，采用如下方式添加tfdbg的hook。
    1. **新增from tensorflow.python import debug as tf_debug**导入debug模块。
    2. **在生成EstimatorSpec对象实例的位置（即构造网络结构代码位置），新增代码tf_debug.LocalCLIDebugHook()**。
**图1**
Estimator模式

  - 如果采用session.run模式，采用如下方式在run之前设置tfdbg装饰器。
    1. **新增from tensorflow.python import debug as tf_debug**导入debug模块。
    2. **在session初始化结束后，新增sess = tf_debug.LocalCLIDebugWrapperSession(sess, ui_type="readline")**。
**图2**
session.run模式

2. 执行训练/在线推理脚本。
3. **训练/在线推理任务停止后，命令行视图自动进入tfdbg****调试命令行交互模式，执行run**命令。

```
For more details, see help.
tfdbg> run
```

**run****命令执行完成后，可以依次执行lt****命令查询已存储的张量，执行pt**命令查看已存储的张量内容，保存数据为npy格式文件。具体操作请参见收集npy文件。

#### 收集npy文件

**run****命令执行完成后，需要收集npy文件，但由于tfdbg**一次只能dump一个tensor，为了自动收集所有npy文件，具体执行操作如下：

1. ***执行lt > gpu_dump****命令将所有tensor的名称暂存到自定义名称的gpu_dump*文件里。命令行中会有如下回显。

```
1
```

```
Wrote output to tensor_name

```
|  |  |
| --- | --- |

2. *重新开启一个命令行窗口，在新的命令行窗口进入gpu_dump*文件所在目录（默认在训练/在线推理脚本所在目录），执行下述命令，用以生成在tfdbg命令行执行的命令。
**
```
timestamp=$[$(date +%s%N)/1000] ; cat gpu_dump | awk '{print "pt",$4,$4}' | awk '{gsub("/", "_", $3);gsub(":", ".", $3);print($1,$2,"-n 0 -w "$3".""'$timestamp'"".npy")}'
```

3. **复制所有生成的存储tensor的命令（所有以“pt”开头的命令），回到tfdbg**命令行视图所在窗口，粘贴执行，即可存储所有npy文件。存储路径为训练/在线推理脚本所在目录。
npy文件默认是以numpy.save()形式存储的，上述命令会将“/”与“:”用下划线_替换。
如果命令行界面无法粘贴文件内容，可以在tfdbg命令行中输入“mouse off”指令关闭鼠标模式后再进行粘贴。

4. *检查生成的npy文件命名是否符合{op_name}.{output_index}.{timestamp}*.npy格式，如图3所示。

  - 如果因算子名较长，造成按命名规则生成的npy文件名超过255字符而产生文件名异常，这类算子不支持精度比对。
  - [因tfdbg自身原因或运行环境原因，可能存在部分生成的npy文件名不符合精度比对要求，请按命名规则手工重命名。如果不符合要求的npy文件较多，请参见生成npy文件名异常情况批量处理](atlasaccuracy_16_0059.html#ZH-CN_TOPIC_0000002536143823)重新生成npy文件。
**图3**
查询.npy文件

**父主题：**[GPU vs NPU（TensorFlow 1.15训练/在线推理）](atlasaccuracy_16_0005.html)