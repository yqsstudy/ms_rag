---
title: "运行Kernel时提示权限错误"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0166.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0166.html"
---

# 运行Kernel时提示权限错误

#### 现象描述

运行Kernel时出现以下报错：

```
1
2
```

```
raise PermissionError(f'Path {path} cannot have write permission of group.')
PermissionError: Path /any_path/_gen_module.so cannot have write permission of group.

```
|  |  |
| --- | --- |

#### 错误原因

当前用户创建的文件的默认权限过大（具有group写权限）。

#### 解决措施
先使用umask -S命令查询权限配置，再使用umask 0022命令调整权限配置。
```
1
2
3
```

```
$ umask -S
$ umask 0022
u=rwx,g=rx,o=rx

```
|  |  |
| --- | --- |
**父主题：**[FAQ](atlasopdev_16_0167.html)