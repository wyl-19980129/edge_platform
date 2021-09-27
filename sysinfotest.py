# coding='utf-8'
#!/usr/bin/python3
import requests
import psutil
import socket
import time


# 获得本机ip地址
def get_host_ip():
    """
    查询本机ip地址
    return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# 获得CPU利用率
def cpuinfo():
    cpuLoad = psutil.cpu_percent(interval=1)
    return cpuLoad

# 获得GPU利用率
def gpuinfo():
    gpuLoadFile = "/sys/devices/gpu.0/load"
    # On the Jetson TX1 this is a symbolic link to:
    # gpuLoadFile="/sys/devices/platform/host1x/57000000.gpu/load"
    # On the Jetson TX2, this is a symbolic link to:
    # gpuLoadFile="/sys/devices/platform/host1x/17000000.gp10b/load" 

    gpuFile = open(gpuLoadFile, 'r')
    fileDate = gpuFile.read()
    # The GPU load is stored as a percentage * 10, e.g 256 = 25.6%
    gpuLoad = int(fileDate)/10

    gpuFile.close()
    return gpuLoad

# 获得内存利用率
def meminfo():
    mem = psutil.virtual_memory()
    """
    mem:
    svmem(total=4156911616, available=2196254720, percent=47.2, used=1750446080, free=1401671680, active=1378832384, 
    inactive=652947456, buffers=65486848, cached=939307008, shared=50933760, slab=147169280)
    """
    return mem.percent
  

    
if __name__ == "__main__":
    ip = get_host_ip()
    print(ip)
    # 存放监控项目的名称，这些名称需要在前端提前进行注册，并且和这里保持一致
    items = ["cpuLoad", "gpuLoad", "memUsage"]
    headers = {'Connection':'close'}

    while True:
        t = int(time.time())  # 秒级时间戳
        cpuLoad = cpuinfo() 
        gpuLoad = gpuinfo()
        memUsage = meminfo()

        dataCpu = {"ip": ip, "item": items[0], "value": cpuLoad, "time": t}
        responseCpu = requests.post('http://101.132.183.48:8000/sys', data=dataCpu)
        print("the response of cpuLoad:", responseCpu)
    
        # exit()
        dataGpu = {"ip": ip, "item": items[1], "value": gpuLoad, "time": t}
        responseGpu = requests.post('http://101.132.183.48:8000/sys', data=dataGpu)
        print("the response of gpuLoad:", responseGpu)

        dataMem = {"ip": ip, "item": items[2], "value": memUsage, "time": t}
        responseMem = requests.post('http://101.132.183.48:8000/sys', data=dataMem)
        print("the response of dataMem:", responseMem)

