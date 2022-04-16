import math

import os
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

# 线程池，创建了 CPU核数个线程池，至于每个线程池里面线程对个数，考虑到创建太多，导致利用率不高，消耗资源；创建太少，导致每个CPU核可能会出现浪费到情况（等待IO完成）
threadPools = [ThreadPoolExecutor(5) for i in range(os.cpu_count())]

# 进程池，大小为CPU核心的个数
processPool = ProcessPoolExecutor(os.cpu_count())


# 获取所有文件，paths用来保存文件的路径
def list_dir(path, paths: list):
    for i in os.listdir(path):
        temp_dir = os.path.join(path, i)
        if os.path.isdir(temp_dir):
            list_dir(temp_dir, paths)
        else:
            paths.append(temp_dir)


# 对文件对操作
def openFile(filePath):
    with open(filePath, 'rb') as f:
        # 模拟io
        time.sleep(1)
        print(f.name)
        # print(f.read())


# 处理文件
def handle(item):
    threadPools[item[0]].submit(openFile, item[1])


if __name__ == '__main__':
    res = []
    list_dir('/Volumes/mac-data/机器学习/OfficeHomeDataset_10072016', res)
    # 根据图片的数目以及CPU和核数，来划分每个核应该加载多少个图片
    gap = math.ceil(len(res) / float(os.cpu_count()))
    index = 0
    for i in range(os.cpu_count()):
        if index + gap >= len(res):
            i_p = ((i, s) for s in res[index:len(res)])
            processPool.map(handle, i_p)
        else:
            i_p = ((i, s) for s in res[index:index + gap])
            processPool.map(handle, i_p)
            index += gap
