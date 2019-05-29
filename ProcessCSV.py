import csv
from Functions import *
import random
import queue


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

        self.classification_column = None

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
        self.classifier_column = self.columns['class']

    def clean_up(self):
        if self.files_loaded:
            self.clean = not self.clean
            self.delete_row_where_empty_class()
            self.instances_number = len(self.classifier_column)
            self.fill_empty_values()
            self.convert_numeric_columns()
            # after cleanup, no need to wait for user input, can start analyzing some of the data
            self.count_classes()
            self.calc_classes_entropy()

    def convert_numeric_columns(self):
        for label in self.tags:
            if self.tags[label] == 'NUMERIC':
                self.columns[label] = list(
                    map(lambda x: float(x), self.columns[label]))

    def delete_row_where_empty_class(self):
        # Iterate over the class column values
        for index in range(len(self.classifier_column) - 1):
            if self.classifier_column[index] == '':
                # if empty, remove the whole row (meaning go over all columns, and pop the row number)
                for column in self.columns:
                    self.columns[column].pop(index)

    def fill_empty_values(self):
        for column in self.columns:
            for index in range(len(self.columns[column])):
                if self.columns[column][index] == '':
                    self.columns[column][index] = self.fillers[column]

    def count_classes(self):
        for val in self.classifier_column:
            if val in self.classifications_counters:
                self.classifications_counters[val] += 1
            else:
                self.classifications_counters[val] = 1

    def calc_classes_entropy(self):
        self.class_entropy = entropy(self.classifications_counters.values())

    def find_best_descritization_split_by_entropy(self, column):
        """ For each split point build table to use for calculates """
        """ #################################################### """
        """ ################ class a ##### class b  ########### """
        """ ### < split ####### x ############ y ############# """
        """ #### >= split ###### z ############ w ########## """
        """ ############################################### """
        def construct_entropy_table_for_split_point(classifications_counters, split_point, column, classifier_column):
            entropy_table = {
                '<': {},
                '>=': {}
            }

            for specific_class in classifications_counters:
                entropy_table['<'][specific_class] = 0
                entropy_table['>='][specific_class] = 0

            for col_value_index in range(len(column)):
                if column[col_value_index] < split_point:
                    entropy_table['<'][classifier_column
                                       [col_value_index]] += 1
                else:
                    entropy_table['>='][classifier_column
                                        [col_value_index]] += 1
            return entropy_table

        # If column has 1 element, return the element
        if (len(column) == 1):
            return column[0]
        # other wise check for all possible split points
        possible_split_points = set()

        col_len = len(column)

        # define possible split points
        for x in range(col_len):
            for y in range(x + 1, col_len):
                possible_split_points.add((column[x] + column[y]) / 2)

        if len(possible_split_points) == 1:
            return possible_split_points.pop()
        # calculate gains of each possible split point
        gains = dict(map(lambda split_point: (split_point,
                                              calc_gain(split_point,
                                                        column,
                                                        construct_entropy_table_for_split_point(self.classifications_counters,
                                                                                                split_point,
                                                                                                column,
                                                                                                self.classifier_column
                                                                                                ),
                                                        self.instances_number,
                                                        self.class_entropy
                                                        ),

                                              ),
                         possible_split_points
                         )
                     )
        # save only those with best gains (for the posibillity of multiple splits having the same score)
        best_gains = list(filter(lambda x: gains[x] == max(
            list(gains.values())), gains))

        # if found 1 best gain return it
        if len(best_gains) == 1:
            return best_gains[0]
        else:
            # return some random split point with a highest gain
            return best_gains[random.randint(0, len(best_gains) - 1)]

    def entropy_discretization(self, column, num_of_bins):

        if num_of_bins == len(column):
            return column
        elif num_of_bins == 1:
            return column
        else:

            def calc_split_index(column_to_split, best_split):
                col = list(filter(lambda x: x < best_split, column_to_split))
                return len(col) - 1 if len(col) > 0 else len(col)

            sorted_col = sorted(column)
            bins = []
            column_queue = queue.Queue()
            column_queue.put(sorted_col)

            while(len(bins) < num_of_bins):
                if column_queue.not_empty:
                    current_col = column_queue.get()
                    best_split = self.find_best_descritization_split_by_entropy(
                        current_col)
                    bins.append(best_split)
                    split_index = calc_split_index(current_col, best_split)
                    if (len(sorted_col) > 2):
                        column_queue.put(sorted_col[:split_index + 1])
                        column_queue.put(sorted_col[split_index + 1:])

            return sorted(bins)

    def discretisize(self, num_of_bins):

        def check_new_label(value, bins):
            for label_index in range(len(bins)):
                if value <= bins[label_index]:
                    return label_index
            return len(bins) - 1

        for column in self.columns:
            if self.tags[column] == 'NUMERIC':
                bins = self.entropy_discretization(
                    self.columns[column], num_of_bins)
                self.columns[column] = list(map(lambda x: check_new_label(
                    x, bins), self.columns[column]))

        # def get_attr_numbers(self):
        # attrs = {}
        # for col in self.columns:
        #     attrs[col] = {}
        #     for attr in self.columns[col]:
        #         if attr not in attrs[col]:
        #             attrs[col][attr] = 1
        #         else:
        #             attrs[col][attr] = attrs[col][attr] + 1
        # print(attrs)
