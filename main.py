#coding:utf-8
#! /bin/python
import os
import struct
import random

class BinaryFileConverter:
    def __init__(self, delimiter, ignorChar, ignorLine, types, originDir, resultDir, ext, formatter, dotPrintRatio, merge):
        # 每行中数字间的分隔符
        self.delimiter = delimiter
        # 需要忽略的符号
        self.ignorChar = ignorChar
        # 需要忽略的行
        self.ignorLine = ignorLine
        # 需要转的文件
        self.types = types
        # 转之前的
        self.originDir = originDir
        # 转之后的文件夹
        self.resultDir = resultDir
        # 转换后的后缀
        self.ext = ext
        # 格式 可选内容参考：https://docs.python.org/3/library/struct.html?#format-characters
        self.formatter = formatter
        # 打点率
        self.dotPrintRatio = dotPrintRatio
        # 合成几个文件 0代表不合并
        self.merge = merge
        self.i = 0

    def dfs(self, rootDir):
        for item in sorted(os.listdir(rootDir)):
            path = os.path.join(rootDir, item)
            if os.path.isdir(path):
                self.dfs(path)
            else:
                self.process(path)
                # print(path)

    def process(self, path):
        (curFile, curType) = os.path.splitext(path)
        if curType in self.types:
            originFile = open(path, 'r')
            if not self.merge:
                newFilePath = self.resultDir + curFile[len(self.originDir):] + self.ext
                newFileDir = os.path.dirname(newFilePath)
                if not os.path.exists(newFileDir):
                    os.makedirs(newFileDir)
                self.resultFile = open(newFilePath ,'wb')
            print('开始写啦' + path)
            self.writeToFile(originFile, self.resultFile)
            if not self.merge:
                self.resultFile.close()
            print('\n')
            print('写完啦' + path)

    def writeToFile(self, originFile, resultFile):
        lines = originFile.readlines()
        for line in lines:
            if (line in self.ignorLine) or (line.strip() in self.ignorLine):
                continue
            curLine = line.strip().split(self.delimiter)
            for i in curLine:
                if (not len(i.strip())) or (i in self.ignorChar):
                    continue
                if random.random() < self.dotPrintRatio:
                    print('.', end = '')
                self.i += 1
                parsedata = struct.pack(self.formatter, float(i))
                resultFile.write(parsedata)
        originFile.close()

    def convert(self):
        if self.merge:
            if not os.path.exists(self.resultDir):
                os.makedirs(self.resultDir)
            self.resultFile = open(self.resultDir + '_allData.dat' ,'wb')
        self.dfs(self.originDir)
        if self.merge:
            self.resultFile.close()
        print(self.i)

BinaryFileConverter(
    delimiter = ',', 
    ignorChar = ['[', ']'], 
    ignorLine = ['[', ']'], 
    types = ['.txt', '.json'], 
    originDir = './mobileNet', 
    resultDir = './bin', 
    ext = '.dat', 
    formatter = 'd', 
    dotPrintRatio = 0, 
    merge = 1).convert()

