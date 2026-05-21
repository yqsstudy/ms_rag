---
title: "内存泄漏分析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0005.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0005.html"
---

# 内存泄漏分析

Step内的内存问题主要包括内存泄漏、踩踏、内存碎片，导致内存池空闲、内存过多等问题。msLeaks工具当前仅支持内存泄漏问题的定位。

#### 前提条件

- 请使用内存分析功能时，如果需要设置--events参数，请确保--events参数中包含alloc和free。
- 在使用内存分析功能时，请勿设置--steps参数。

#### 在线方式

[在进行内存分析时，需配合使用mstx打点功能进行问题定位，mstx打点详情参考《MindStudio mstx API参考](https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0001.html)》。

1. 使用msLeaks工具运行用户程序，Application为用户程序。
**
```
msleaks ${Application}
```

2. 执行完成后，会出现如下两种回显信息。

  1. 如果出现如图1的回显信息，表示存在内存泄漏问题。回显信息中分别展示了每张卡内存泄漏的汇总信息，包括泄漏发生的Step数、关联的kernel、地址以及泄漏大小等信息。**图1**
内存泄漏
  2. 如果出现如图2的回显信息，表示存在内存波动。回显信息中展示了单个Step内的内存波动（用最小和最大的内存池分配占用比值定义）以及最小的内存池分配占用，同时给出最小比值和最大比值作为参考，用户可根据该值判断是否存在内存泄漏风险。
在第一个Step时，内存尚未稳定，所以只支持分析从第二个Step开始的内存波动，第一个Step内存波动可忽略。
**图2**
内存波动

3. 将输出文件中的json文件（可视化内存信息）使用可视化工具展示，如图3[所示，可查看内存申请释放情况。内存问题主要依靠内存信息可视化图进行分析，可视化信息详解可参见输出说明](atlas_msleaks_0016.html#ZH-CN_TOPIC_0000002506628524)。
**图3**
内存申请释放情况

4. 用户的打点信息如图4所示，当泄漏内存申请的时间与箭头标识的时间重合时，表示此时mstx打点位置附近的代码发生了内存泄漏。
**图4**
标识打点

#### 离线方式

msLeaks支持对指定范围内的内存事件进行离线泄漏分析。使用mstx标识好泄漏分析的范围后，可以使用该功能对落盘文件进行分析。

当前离线内存泄漏分析功能仅支持HAL内存泄漏分析。

- 工具部署
[msLeaks工具进行离线内存泄漏分析时，需先安装开放态部署场景，安装操作请参见《CANN 软件安装指南 (开放态)](https://www.hiascend.com/document/detail/zh/canncommercial/82RC1/openform/instguide310/instgopen_0002.html)》。

  1. 开放态部署场景安装成功后，开启2个远程登录工具，分别登录Host侧和Device侧进行操作。
  2. [参考《CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0000.html?Mode=PmIns&InstallType=local&OS=openEuler)》下载配套版本的CANN Toolkit开发套件包和ops算子包，并解压。
  3. 请根据实际情况自行将Host侧的用户测试文件与msLeaks工具上传至Device侧。
msLeaks工具包默认位于“$HOME/Ascend/cann/tools/msleaks” 路径下，具体路径以实际安装路径为准。

[传输文件时，需打开SSH服务。文件传输完成后，请及时关闭SSH服务，保证系统安全性。SSH服务具体操作请参见《CANN 软件安装指南 (开放态)](https://www.hiascend.com/document/detail/zh/canncommercial/82RC1/openform/instguide310/instgopen_0002.html)[》的“定制文件系统 > 修改文件系统 > 打开SSH服务](https://www.hiascend.com/document/detail/zh/canncommercial/82RC1/openform/instguide310/instgopen_0016.html)”章节。

  4. 将Host侧的ACL相关依赖上传至Device侧。
当前ACL相关依赖在Host侧的“/usr/local/AscendMiniOs/acllib/lib64”路径下，需要将依赖上传至Device侧的“/usr/local/AscendMiniOs/aarch64-linux/data”路径下，Host侧和Device侧的具体路径以实际安装路径为准，请根据实际情况自行上传。

  5. 在Device侧执行以下命令，在Device侧设置环境变量。
```
export LD_LIBRARY_PATH=./lib:./lib64:./:./home/HwHiAiUser:$LD_LIBRARY_PATH;export ASCEND_OPP_PATH=./;
```

  6. 在Device侧，确认缺少的so包。
    - 用户测试文件运行前，在Device侧，执行以下命令，查看缺少的so包。此处的MyApplication为用户测试文件。**
```
ldd ${MyApplication}
```

    - 用户测试文件运行后，如果出现类似以下回显信息，代表Device侧缺少so包。
```
1
```

```
libascend_xxx.so: cannot open shared object file: No such file or directory

```
|  |  |
| --- | --- |

  7. 在Host侧查找缺少的so包，大部分so包存在于“$HOME/Ascend/cann/aarch64-linux/lib64/”路径下。
**也可在Host侧执行以下命令，查询缺失的so包所在路径。其中soName**为so包的名称。
**
```
find / -name ${soName}
```

  8. 将Host侧的so包上传至Device侧，请根据实际情况自行上传。

- 内存分析
  1. [对需要检测泄漏的范围进行mstx的mark打点。mstx打点详情参考《MindStudio mstx API参考](https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0001.html)》。
    - 打点的mark信息将用于离线分析接口的输入。
    - 使用mark打点功能标记三个点，分别称为A、B、C。在A到B范围内申请的内存，需要在C点前全部释放，否则会被判定为内存泄漏。

  2. 执行以下命令，使用msLeaks工具运行用户程序，获取落盘csv文件，Application为用户程序。**
```
msleaks ${Application}
```

  3. 执行以下命令，调用Python接口，对输出的csv文件进行离线泄漏分析。
```
1
2
```

```
import msleaks
msleaks.check_leaks(input_path="user/leaks.csv",mstx_info="test",start_index=0)

```
|  |  |
| --- | --- |

其中参数信息如下：

    - input_path：csv文件所在路径，需使用绝对路径。
    - mstx_info：mark打点使用的mstx文本信息，用于标识泄漏分析的范围。
    - start_index：内存泄漏分析开始的打点位置编号，即从第几个符合条件的mstx打点位置开始分析。
如果出现图5的回显信息，表示存在内存泄漏问题。**图5**
离线泄漏分析

**父主题：**[内存分析](atlas_msleaks_0004.html)