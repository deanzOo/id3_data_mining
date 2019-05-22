import csv
from Functions import *


class ProcessCSV:
    def __init__(self):
        self.tags = {}
        self.columns = {}
        self.file = ''
        self.fillers = {}

    def loadFile(self, filePath):
        self.file = csv.reader(open(filePath, 'r'))

    def loadTags(self, structureFilePath):
        structureFile = open(structureFilePath, 'r')
        for line in structureFile:
            line = line.strip('\n').strip('@ATTRIBUTE ').split(' ')
            if line[1] != 'NUMERIC':
                line[1] = line[1].strip('{').strip('}').split(',')
            self.tags[line[0]] = line[1]

    def constructColumns(self):
        columnList = []
        colLen = len(self.tags)
        for _ in range(colLen):
            columnList.append([])
        for row in self.file:
            for colIndex in range(len(self.tags)):
                columnList[colIndex].append(row[colIndex])
        for column in columnList:
            column.pop(0)
        index = 0
        for x in self.tags:
            self.columns[x] = columnList[index]
            index += 1

    def getColumns(self):
        return self.columns

    def getFile(self):
        return self.file

    def getTags(self):
        return self.tags

    def getFillers(self):
        return self.fillers

    def constructFillers(self):
        for key in self.tags:
            self.fillers[key] = NumericAverage(
                self.columns[key]) if self.tags[key] == 'NUMERIC' else FindingCommonValue(self.columns[key])

    def findRowWithEmptyClassAndDelete(self):
        for index in range(len(self.columns['class']) - 1):
            if self.columns['class'][index] == '':
                for column in self.columns:
                    self.columns[column].pop(index)

    def findEmptyColumn(self):
        for column in self.columns:
            for index in range(len(self.columns[column])):
                if self.columns[column][index] == '':
                    self.columns[column][index] = self.fillers[column]
