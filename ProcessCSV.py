import csv
from Functions import *
from functools import reduce


class ProcessCSV:
    def __init__(self):
        self.tags = {}              # Structure of the data
        self.columns = {}           # each key = 1 actual column from the file
        self.file = ''              # this var will hold the file reader
        # for each attribute, hold a value to fill in in case its empty in the actual data
        self.fillers = {}
        self.totalClasses = 0       # counter for how many classifications we have
        self.classesCounters = {}   # counters for each of the classification
        self.classEntropy = 0       # entropy level of the current classification

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

    def getClassesEntropy(self):
        return self.classEntropy

    def getClassesCounter(self):
        return self.classesCounters

    def getTotalClasses(self):
        return self.totalClasses

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

    def findClassEntropy(self):
        for val in self.columns['class']:
            if val in self.classesCounters:
                self.classesCounters[val] += 1
            else:
                self.classesCounters[val] = 1
        self.classEntropy = entropy(self.classesCounters.values())
        self.totalClasses = reduce(
            lambda x, y: x + y, self.classesCounters.values())

    def findSplitPosition(self, column):
        bestGain = -1
        bestSplit = -1
        for index in range(len(column)):
            for secondIndex in range(index + 1, len(column)):
                splitPoint = (float(column[index]) +
                              float(column[secondIndex])) / 2
                entropyTable = {
                    'belowSplitPoint': {},
                    'notBelowSplitPoint': {}
                }

                for specific_class in self.classesCounters:
                    entropyTable['belowSplitPoint'][specific_class] = 0
                    entropyTable['notBelowSplitPoint'][specific_class] = 0

                for col_value_index in range(len(column)):
                    if float(column[col_value_index]) < splitPoint:
                        entropyTable['belowSplitPoint'][self.columns['class']
                                                        [col_value_index]] += 1
                    else:
                        entropyTable['notBelowSplitPoint'][self.columns['class']
                                                           [col_value_index]] += 1

                if bestSplit == -1:
                    bestSplit = splitPoint
                    info = 0
                    for section in entropyTable:
                        totalSection = reduce(
                            lambda x, y: x + y, entropyTable[section].values())
                        part = totalSection / len(self.columns['age'])
                        info += part * entropy(entropyTable[section].values())
                    print('info: ', info)
                    print('gain: ', self.classEntropy - info)
                    bestGain = self.classEntropy - info
                else:
                    info = 0
                    for section in entropyTable:
                        totalSection = reduce(
                            lambda x, y: x + y, entropyTable[section].values())
                        part = totalSection / len(self.columns['age'])
                        info += part * entropy(entropyTable[section].values())
                    print('info: ', info)
                    print('gain: ', self.classEntropy - info)
                    if bestGain < self.classEntropy - info:
                        bestSplit = splitPoint
                        bestGain = self.classEntropy - info

                print(entropyTable)
                print('split point: ', splitPoint)
        print('class entropy: ', self.classEntropy)
        print('best split point: ', bestSplit, 'gain is: ', bestGain)
