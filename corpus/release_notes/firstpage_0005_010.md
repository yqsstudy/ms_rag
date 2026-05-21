---
title: "文件校验标准"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/releasenote/firstpage_0005_010.html"
date_collected: "2026-05-04"
category: "release_notes"
original_path: "zh/mindstudio/830/releasenote/firstpage_0005_010.html"
---

# 文件校验标准

MindStudio默认使用普通用户安装，且推荐使用普通用户进行操作，不建议使用root用户进行操作。

文件类型

校验标准

输入数据文件

确保输入的数据文件存在且可读，路径长度适中，文件大小适中，且非软链接。该文件的属主为root用户或当前用户，group和other用户组均不可写。

输入文件夹

- 确保输入的文件夹存在、可读、路径长度适中且非软链接。文件夹的属主为root用户或当前用户，group
- 和other用户组均不可写。
- 输入文件夹内的文件也需满足存在、可读、文件大小适中且非软链接的要求。文件的属主为root用户或当前用户，group和other用户组均不可写。

输出文件路径

输出文件的路径必须存在，且不能为软链接。该目录的属主为当前用户，other用户组不可写。

输出文件

输出文件不能为软链接，其属主为当前用户。此外，输出文件的权限不大于640，这意味着除了属主以外的任何人（包括同组用户和其他用户）都不能读取或写入该文件。

输出路径

输出路径需要确保可写，且不能为软链接。该路径的属主为root或当前用户，group和other用户组均不可写。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |