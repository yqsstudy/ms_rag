---
title: "调用Ascend CL单算子"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0075.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0075.html"
---

# 调用Ascend CL单算子

#### 前提条件
[单击Link](https://gitee.com/ascend/samples/tree/master/operator/ascendc/0_introduction/1_add_frameworklaunch/AddCustom)获取算子样例工程，为进行算子调试做准备。
- 此样例工程不支持Atlas A3 训练系列产品。
- 下载代码样例时，需执行以下命令指定分支版本。
```
git clone https://gitee.com/ascend/samples.git -b master
```

#### 操作步骤

1. 切换到msOpGen脚本install.sh所在目录。

```
cd ${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch
```

2. 执行以下命令，生成自定义算子工程，并进行Host侧和Kernel侧的算子实现。
****
```
bash install.sh -v Ascendxxxyy    # xxxyy为用户实际使用的具体芯片类型
```

3. **在${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/CustomOp目录下修改CMakePresets.json文件的cacheVariables的配置项，将"Release"****修改为"Debug"**。

```
1
2
3
4
5
6
7
```

```
"cacheVariables": {               
       "CMAKE_BUILD_TYPE": {                    
            "type": "STRING",                    
            "value": "Debug"               
  },
...
}

```
|  |  |
| --- | --- |

4. [参考算子编译部署](atlasopdev_16_0024.html#ZH-CN_TOPIC_0000002504880720)完成算子的编译部署。
5. [切换到msOpGen脚本install.sh所在目录，并参考README](https://gitee.com/ascend/samples/blob/master/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation/README.md)**编译单算子调用应用并得到可执行文件execute_add_op**。

```
cd ${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation
```

6. 导入算子动态加载路径。

**将自定义算子工程编译后输出在build_out目录下Kernel侧的.o**文件路径导入环境变量。
**********
```
export LAUNCH_KERNEL_PATH=/{path_to_kernel}/kernel_name.o  //{path_to_kernel}表示对算子Kernel侧实现编译后生成的算子二进制文件*.o所在路径，请根据实际情况进行替换
```

**算子的多个dtype在Kernel侧可能会编译出多个.o**文件，请选择步骤3**示例中所调用的.o**文件进行导入。

7. 使用msDebug工具加载步骤5中得到的单算子可执行文件execute_add_op。
****
```
export LD_LIBRARY_PATH=$ASCEND_HOME_PATH/opp/vendors/customize/op_api/lib:$LD_LIBRARY_PATH
cd AclNNInvocation/output
msdebug execute_add_op
(msdebug) target create "execute_add_op"
Current executable set to '/home/AclNNInvocation/output/execute_add_op' (aarch64).
(msdebug)
```

8. 断点设置。
****
```
b add_custom.cpp:55
```

9. 运行算子程序，等待直到命中断点。

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
```

```
(msdebug) r
Process 1385976 launched: '$HOME/shelltest/test/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocationNaive/build/execute_add_op' (aarch64)
[Launch of Kernel anonymous on Device 0]
Process 1385976 stopped
[Switching to focus on Kernel anonymous, CoreId 24, Type aiv]
* thread #1, name = 'execute_add_op', stop reason = breakpoint 1.1
    frame #0: 0x0000000000001564 AddCustom_1e04ee05ab491cc5ae9c3d5c9ee8950b.o`KernelAdd::Compute(this=0x000000000028f8a8, progress=0) (.vector) at add_custom.cpp:55:19
   52  	        LocalTensor<DTYPE_Y> yLocal = inQueueY.DeQue<DTYPE_Y>();
   53  	        LocalTensor<DTYPE_Z> zLocal = outQueueZ.AllocTensor<DTYPE_Z>();
   54  	        Add(zLocal, xLocal, yLocal, this->tileLength);
-> 55  	        outQueueZ.EnQue<DTYPE_Z>(zLocal);
   56  	        inQueueX.FreeTensor(xLocal);
   57  	        inQueueY.FreeTensor(yLocal);
   58  	    }
(msdebug) 

```
|  |  |
| --- | --- |

[后续调试过程可参考导入调试信息](atlasopdev_16_0063.html#ZH-CN_TOPIC_0000002536920529__zh-cn_topic_0000002534426397_section1689328161710)[、内存与变量打印](atlasopdev_16_0067.html#ZH-CN_TOPIC_0000002536800563)[及核切换](atlasopdev_16_0070.html#ZH-CN_TOPIC_0000002505040604)等，与其操作一致。

**父主题：**[典型案例](atlasopdev_16_0073.html)