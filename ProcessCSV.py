import csv
from Functions import *


class ProcessCSV:
    def __init__(self):
        self.tags = {}
        self.rows = []
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

    def constructRows(self):
        for row in self.file:
            self.rows.append(row)
        self.rows.pop(0)

    def constructColumns(self):
        columnList = []
        colLen = len(self.rows[0])
        for _ in range(colLen):
            columnList.append([])
        for rowIndex in range(len(self.rows)):
            for colIndex in range(len(self.rows[rowIndex])):
                columnList[colIndex].append(self.rows[rowIndex][colIndex])
        index = 0
        for x in self.tags:
            self.columns[x] = columnList[index]
            index += 1

    def getRows(self):
        return self.rows

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
        for row in range(len(self.rows) - 1):
            colNum = len(self.rows[row])
            if self.rows[row][colNum-1] == '':
                self.rows.pop(row)
