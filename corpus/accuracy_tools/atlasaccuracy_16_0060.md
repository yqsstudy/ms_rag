---
title: "Windows dump文件转换为Linux dump文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0060.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0060.html"
---

# Windows dump文件转换为Linux dump文件

1. 在Linux上准备转换脚本windows_to_linux.py，内容如下。

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
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
```

```
import argparse
import os
import sys

class WindowsToLinux:
    """
    The class for format windows to linux
    """

    def __init__(self):
        parse = argparse.ArgumentParser()
        parse.add_argument("-i", dest="windows_dump_path", default="",
                           help="<Required> the dump file path", required=True)
        parse.add_argument("-o", dest="output_path", default="",
                           help="<Required> the output path", required=True)
        args, _ = parse.parse_known_args(sys.argv[1:])
        self.windows_dump_path = os.path.realpath(args.windows_dump_path)
        self.output_path = os.path.realpath(args.output_path)

    def windows_to_linux(self, dump_path):
        try:
            with open(dump_path, "rb") as dump_file:
                content = dump_file.read()
                new_content = content.replace(b"\r\n", b"\n")
                output_file_path = os.path.join(self.output_path, os.path.basename(dump_path))
                with open(output_file_path, "wb") as new_dump_file:
                    new_dump_file.write(new_content)
                    print('Info: convert dump to linux for "%s" successfully.' % dump_path)
        except (OSError, IOError, MemoryError, SystemError) as error:
            print('Error: convert windows dump file "%s" to linux dump file failed. %s' % (dump_path, error))

    def convert(self):
        try:
            if not os.path.exists(self.windows_dump_path) and \
                    not os.access(self.windows_dump_path, os.R_OK):
                print('Error: the path "%s" does not exist or is not readable.')
                sys.exit()

            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)
            if not os.path.exists(self.output_path) and \
                    not os.access(self.output_path, os.W_OK):
                print('Error: the path "%s" does not exist or can not writable.')
                sys.exit()

            if os.path.isfile(self.windows_dump_path):
                self.windows_to_linux(self.windows_dump_path)
            else:
                for file_name in os.listdir(self.windows_dump_path):
                    self.windows_to_linux(os.path.join(self.windows_dump_path, file_name))
        except (OSError, IOError, MemoryError, SystemError) as error:
            print('Error: convert windows dump file to linux dump file failed. %s' % error)
            sys.exit()

if __name__ == "__main__":
    main = WindowsToLinux()
    main.convert()

```
|  |  |
| --- | --- |

2. 将Windows的dump文件拷贝到Linux某个目录下。
3. 在Linux上执行转换脚本。
********
```
# windows_dump_path是步骤2中Windows的dump文件拷贝到Linux的目录
# linux_dump_path是生成的Linux的dump文件存放路径
python3 windows_to_linux.py -i {windows_dump_path} -o {linux_dump_path}
```

**父主题：**[扩展功能](atlasaccuracy_16_0051.html)