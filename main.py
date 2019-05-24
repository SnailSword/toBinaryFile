#coding:utf-8
#! /bin/python
import os
# import sys
# import os.path
# import pickle
import struct
import random

# 每行中数字间的分隔符
delimiter = ' '
# 需要忽略的符号
ignorChar = ['[', ']']
# 需要忽略的行
ignorLine = ['[', ']']
# 需要转的文件
types = ['.txt', '.json']
# 转之前的
originDir = './test'
# 转之后的文件夹
resultDir = './bin'
# 转换后的后缀
ext = '.dat'
# 格式 可选内容参考：https://docs.python.org/3/library/struct.html?#format-characters
formatter = 'd'
# 打点率
dotPrintRatio = 0.005

def dfs(rootDir):
    for item in os.listdir(rootDir):
        path = os.path.join(rootDir, item)
        if os.path.isdir(path):
            dfs(path)
        else:
            process(path)
            # print(path)

def process(path):
    (curFile, curType) = os.path.splitext(path)
    if curType in types:
        originFile = open(path, 'r')
        lines = originFile.readlines()
        newFilePath = resultDir + curFile[len(originDir):] + ext
        newFileDir = os.path.dirname(newFilePath)
        if not os.path.exists(newFileDir):
            os.makedirs(newFileDir)
        resultFile = open(newFilePath ,'wb')
        print('开始写啦' + newFilePath)
        for line in lines:
            if (line in ignorLine) or (line.strip() in ignorLine):
                continue
            curLine = line.strip().split(delimiter)
            for i in curLine:
                if (not len(i.strip())) or (i in ignorChar):
                    continue
                if random.random() < dotPrintRatio:
                    print('.', end = '')
                parsedata = struct.pack('d', float(i))
                resultFile.write(parsedata)
        originFile.close()
        resultFile.close()
        print('\n')
        print('写完啦' + newFilePath)

dfs(originDir);
