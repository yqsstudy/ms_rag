---
title: "自定义算法.py文件准备"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0057.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0057.html"
---

# 自定义算法.py文件准备

用户自定义的比对算法Python文件只能用来进行精度比对，文件安全性和传入参数的安全性由用户保证。

用户自定义算法，需要在.py格式文件内写好自定义算法脚本，按以下要求准备：

- .py文件命名需满足规则：“ alg_{algorithm_name}.py”，其中，algorithm_name为算法名。
- .py文件内容需满足以下规则：
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
```

```
def compare(my_output_dump_data, ground_truth_dump_data, args):   #算法固定头格式
#以下为算法示例
    """
    Function Description:
        compare the my output dump data and the ground truth dump data by algorithm
    Parameter:
        my_output_dump_data: the my output dump data
        ground_truth_dump_data: the ground truth dump data
        args: the algorithm arguments
    Return Value:
        the compare algorithm value, string; error_msg, string
    """

```
|  |  |
| --- | --- |
**表1**参数说明
参数

说明

my_output_dump_data

my output dump数据，一维数组。

ground_truth_dump_data

ground truth dump数据，一维数组。

args

算法参数，用户自行解析。

Return Value

返回值，包括：

  - 算法比对的结果，String格式。
  - 错误信息，String格式。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |

- 需要在当前用户的目录下创建“algorithm”目录用于保存.py文件，请确保用户对目录和文件具有读写权限。
**父主题：**[扩展功能](atlasaccuracy_16_0051.html)