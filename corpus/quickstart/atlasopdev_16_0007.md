---
title: "算子调试（msDebug）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasopdev_16_0007.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasopdev_16_0007.html"
---

# 算子调试（msDebug）

msDebug支持调试所有昇腾算子，用户可以根据实际情况选择使用不同的功能，例如，可以设置断点、打印变量和内存、进行单步调试、中断运行、核切换等。

1. [安装NPU驱动固件，具体请参见《算子开发工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0002.html)[》的“算子调试（msDebug）> 工具概述](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0062.html)”章节。
2. 在${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch目录执行以下命令，生成自定义算子工程，进行host侧和kernel侧的算子实现。
****
```
bash install.sh -v Ascendxxxyy    # xxxyy为用户实际使用的具体芯片类型
```

3. **在${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/CustomOp目录下修改CMakePresets.json文件的cacheVariables的配置项，将Release****修改为Debug**。

```
"cacheVariables": {
    "CMAKE_BUILD_TYPE": {
      "type": "STRING",
      "value": "Debug"
    },
    ...
  }
```

4. 执行以下命令，重新编译部署算子。

  1. 在${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/CustomOp目录下，执行以下命令，重新编译部署算子。********
```
bash build.sh
./build_out/custom_opp_<target_os>_<target_architecture>.run  // 当前目录下run包的名称
```

  2. **切换到${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation目录，并执行以下命令，将会在./output****路径下生成可执行文件execute_add_op**。
```
bash run.sh
cd  ./output
```

5. 在调试前，配置如下环境变量，指定算子加载路径，导入调试信息，示例如下。
****
```
export LAUNCH_KERNEL_PATH=${INSTALL_DIR}/opp/vendors/customize/op_impl/ai_core/tbe/kernel/${soc_version}/add_custom/AddCustom_1e04ee05ab491cc5ae9c3d5c9ee8950b.o   //soc_version为昇腾AI处理器的Chip Name，需为小写
```

6. 指定算子依赖的动态库路径，将动态库so文件加载进来。

```
export LD_LIBRARY_PATH=${INSTALL_DIR}/opp/vendors/customize/op_api/lib:$LD_LIBRARY_PATH
```

7. **在可执行文件目录下执行msdebug execute_add_o****p**，进入msDebug工具。

```
msdebug execute_add_op
```

8. 断点设置。

  1. 设置断点。
```
(msdebug) b add_custom.cpp:55
```

  2. 回显将会显示断点信息添加成功。
```
Breakpoint 1: where = AddCustom_1e04ee05ab491cc5ae9c3d5c9ee8950b.o`KernelAdd::Compute(int) (.vector) + 68 at add_custom.cpp:55:9, address = 0x00000000000014f4
```

9. **键盘输入r**命令，运行算子程序，等待直到命中断点。

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
15
16
17
18
19
20
21
22
23
```

```
(msdebug) r
Process 1454802 launched: '${INSTALL_DIR}/add_cus/AclNNInvocation/output/execute_add_op' (aarch64)
[INFO]  Set device[0] success
[INFO]  Get RunMode[1] success
[INFO]  Init resource success
[INFO]  Set input success
[INFO]  Copy input[0] success
[INFO]  Copy input[1] success
[INFO]  Create stream success
[INFO]  Execute aclnnAddCustomGetWorkspaceSize success, workspace size 0
[Launch of Kernel AddCustom_1e04ee05ab491cc5ae9c3d5c9ee8950b on Device 0]
[INFO]  Execute aclnnAddCustom success
Process 1454802 stopped
[Switching to focus on Kernel AddCustom_1e04ee05ab491cc5ae9c3d5c9ee8950b, CoreId 39, Type aiv]
* thread #1, name = 'execute_add_op', stop reason = breakpoint 1.1
    frame #0: 0x00000000000014f4 AddCustom_1e04ee05ab491cc5ae9c3d5c9ee8950b.o`KernelAdd::Compute(this=0x00000000003078a8, progress=0) (.vector) at add_custom.cpp:55:9
   52       __aicore__ inline void Compute(int32_t progress)
   53       {
   54           LocalTensor<DTYPE_X> xLocal = inQueueX.DeQue<DTYPE_X>();
-> 55           LocalTensor<DTYPE_Y> yLocal = inQueueY.DeQue<DTYPE_Y>();   //断点处的行号正确即可，其余信息以实际为准
   56           LocalTensor<DTYPE_Z> zLocal = outQueueZ.AllocTensor<DTYPE_Z>();
   57           Add(zLocal, xLocal, yLocal, this->tileLength);
   58           outQueueZ.EnQue<DTYPE_Z>(zLocal);

```
|  |  |
| --- | --- |

10. 继续运行。

  1. 键盘输入以下命令，继续运行。****
```
(msdebug) c
```

  2. 显示程序再次命中该断点。
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
Process 1454802 resuming
Process 1454802 stopped
[Switching to focus on Kernel AddCustom_1e04ee05ab491cc5ae9c3d5c9ee8950b, CoreId 39, Type aiv]
* thread #1, name = 'execute_add_op', stop reason = breakpoint 1.1
    frame #0: 0x00000000000014f4 AddCustom_1e04ee05ab491cc5ae9c3d5c9ee8950b.o`KernelAdd::Compute(this=0x00000000003078a8, progress=0) (.vector) at add_custom.cpp:55:9
   52       __aicore__ inline void Compute(int32_t progress)
   53       {
   54           LocalTensor<DTYPE_X> xLocal = inQueueX.DeQue<DTYPE_X>();
-> 55           LocalTensor<DTYPE_Y> yLocal = inQueueY.DeQue<DTYPE_Y>();  //断点处的行号正确即可，其余信息以实际为准
   56           LocalTensor<DTYPE_Z> zLocal = outQueueZ.AllocTensor<DTYPE_Z>();
   57           Add(zLocal, xLocal, yLocal, this->tileLength);
   58           outQueueZ.EnQue<DTYPE_Z>(zLocal);

```
|  |  |
| --- | --- |

11. 结束调试。

```
(msdebug) q
```

**父主题：**[算子开发工具快速入门](tools_qucikstart_0006.html)