import csv
from Functions import *
from functools import reduce


class ProcessCSV:
    def __init__(self):

        # structure and train files
        self.structure, self.train = None, None

        # {
        #   ATTRIBUTE_NAME: 'NUMERIC' || [possible attribute value]
        # }
        self.tags = {}

        # {
        #   ATTRIBUTE_NAME: [attribute values]
        # }
        self.columns = {}

        # {
        #   ATTRIBUTE_NAME: filler_attribute_value
        # }
        self.fillers = {}

        # {
        #   CLASSIFICATION_NAME: number of instances with this classification
        # }
        self.classifications_counters = {}

        # total number of instances
        self.instances_number = 0
        # entropy level of the class attribute from known data
        self.class_entropy = 0

        # flags to make sure some functions will not work when not ready
        self.clean, self.files_loaded = False, False

    def open_files(self, path):
        try:
            # Try opening train file and structure file
            self.structure = open(path + '/Structure.txt', 'r')
            self.train = csv.DictReader(open(path + '/train.csv', 'r'))
        except FileNotFoundError:
            print('Files not found')
        # Start deconstructing the files into workable data
        self.files_loaded = not self.files_loaded
        self.loadTags()
        self.construct_columns()
        self.constructFillers()

    def loadTags(self):
        for line in self.structure:
            line = line.strip('\n').strip('@ATTRIBUTE ').split(' ')
            if line[1] != 'NUMERIC':
                line[1] = line[1].strip('{').strip('}').split(',')
            self.tags[line[0]] = line[1]

    def construct_columns(self):
        for row in self.train:
            for column in row:
                if column not in self.columns:
                    self.columns[column] = []
                self.columns[column].append(row[column])

    def constructFillers(self):
        for key in self.tags:
            self.fillers[key] = NumericAverage(
                self.columns[key]) if self.tags[key] == 'NUMERIC' else FindingCommonValue(self.columns[key])

    def clean_up(self):
        if self.files_loaded:
            self.clean = not self.clean
            self.delete_row_where_empty_class()
            self.instances_number = len(self.columns['class'])
            self.fill_empty_values()
            # after cleanup, no need to wait for user input, can start analyzing some of the data
            self.count_classes()
            self.calc_classes_entropy()

    def delete_row_where_empty_class(self):
        # Iterate over the class column values
        for index in range(len(self.columns['class']) - 1):
            if self.columns['class'][index] == '':
                # if empty, remove the whole row (meaning go over all columns, and pop the row number)
                for column in self.columns:
                    self.columns[column].pop(index)

    def fill_empty_values(self):
        for column in self.columns:
            for index in range(len(self.columns[column])):
                if self.columns[column][index] == '':
                    self.columns[column][index] = self.fillers[column]

    def count_classes(self):
        for val in self.columns['class']:
            if val in self.classifications_counters:
                self.classifications_counters[val] += 1
            else:
                self.classifications_counters[val] = 1

    def calc_classes_entropy(self):
        self.class_entropy = entropy(self.classifications_counters.values())

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

                for specific_class in self.classifications_counters:
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
                    print('gain: ', self.class_entropy - info)
                    bestGain = self.class_entropy - info
                else:
                    info = 0
                    for section in entropyTable:
                        totalSection = reduce(
                            lambda x, y: x + y, entropyTable[section].values())
                        part = totalSection / len(self.columns['age'])
                        info += part * entropy(entropyTable[section].values())
                    print('info: ', info)
                    print('gain: ', self.class_entropy - info)
                    if bestGain < self.class_entropy - info:
                        bestSplit = splitPoint
                        bestGain = self.class_entropy - info

                print(entropyTable)
                print('split point: ', splitPoint)
        print('class entropy: ', self.class_entropy)
        print('best split point: ', bestSplit, 'gain is: ', bestGain)
