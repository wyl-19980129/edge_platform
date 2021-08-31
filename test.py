# coding='utf-8'
#!/usr/bin/python3
#简单使用cpu的利用率进行测试

import psutil
from decimal import *


# 获得cpu使用率
def cpuinfo():
    cpu_use = psutil.cpu_percent(interval=1)
    return cpu_use

if __name__ == "__main__":
    cpu_use = cpuinfo()
    print(cpu_use)




