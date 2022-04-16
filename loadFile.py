import math

import os
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

threadPools = [ThreadPoolExecutor(20) for i in range(os.cpu_count())]
processPool = ProcessPoolExecutor(os.cpu_count())


def list_dir(path, paths: list):
    for i in os.listdir(path):
        temp_dir = os.path.join(path, i)
        if os.path.isdir(temp_dir):
            list_dir(temp_dir, paths)
        else:
            # i里面子文件的名称
            paths.append(temp_dir)


def openFile(filePath):
    with open(filePath, 'rb') as f:
        # 模拟io
        time.sleep(1)
        print(f.name)
        # print(f.read())


def handle(item):
    threadPools[item[0]].submit(openFile, item[1])


if __name__ == '__main__':
    res = []

    list_dir('/Volumes/mac-data/机器学习/OfficeHomeDataset_10072016', res)
    basePath = '/Volumes/mac-data/机器学习/OfficeHomeDataset_10072016/'
    # for s in res:
    #     print(s)
    gap = math.ceil(len(res) / float(os.cpu_count()))
    index = 0
    for i in range(os.cpu_count()):
        if index + gap >= len(res):
            i_p = ((i, s) for s in res[index:len(res)])
            # for k, path in i_p:
            #     print(k, path)
            processPool.map(handle, i_p)
        else:
            i_p = ((i, s) for s in res[index:index + gap])
            processPool.map(handle, i_p)
            # for k, path in i_p:
            #     print(k, path)
            # index += gap

    # print(json.dumps(get_config_dirs()))
