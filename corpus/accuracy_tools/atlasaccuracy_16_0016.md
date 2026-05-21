---
title: "准备全网层信息文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0016.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0016.html"
---

# 准备全网层信息文件

[以下介绍通过ATC模型转换工具获取离线模型的操作步骤，更多操作请参见《ATC离线模型编译工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/atctool/atlasatc_16_0031.html)》。

1. 以运行用户登录Ascend-cann-toolkit所在环境。
2. 获取原始模型文件并保存在任意目录下。

例如：$HOME/module/resnet50_tensorflow*.pb

3. 执行ATC模型转换。
**************
```
atc --model=$HOME/module/resnet50_tensorflow*.pb --framework=3 --output=$HOME/module/out/tf_resnet50 --soc_version=<soc_version>
```
若提示如下信息，则说明模型转换成功。
```
1
```

```
ATC run success

```
|  |  |
| --- | --- |

成功执行命令后，在--output参数指定的路径下可查看离线模型（如：tf_resnet50.om）。

4. 生成json文件。
****************
```
atc --mode=1 --om=$HOME/module/out/tf_resnet50.om  --json=$HOME/module/out/tf_resnet50.json
```

若提示如下信息，则说明转换json文件成功。

```
1
```

```
ATC run success

```
|  |  |
| --- | --- |

成功执行命令后，在--json参数指定的路径下可查看转换后的json文件。

**父主题：**[GPU vs NPU（TensorFlow离线推理）](atlasaccuracy_16_0013.html)