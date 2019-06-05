from Functions import *
import csv
import copy


def open_files(self, path, filename):
    # Try opening train file and structure file
    self.trained_file = open(path + '' + filename, 'r')
    # Start deconstructing the files into workable data


row_file = csv.reader(open('train_discretization_4.csv', newline=''))
col_file = csv.DictReader(open('train_discretization_4.csv', 'r'))

rows = [row for row in row_file]
attributes = {}
for i, row in enumerate(col_file):
    for attribute in row:
        if attribute not in attributes:
            attributes[attribute] = []
        attributes[attribute].append(row[attribute])

data = {}
data['rows'], data['attributes'] = rows, attributes


def attributes_filter(data, _bin, max_gain_attribute):
    # filtered_data = dict(data)

    dont_keep = []

    filter_by = data['attributes'].pop(max_gain_attribute)

    for index in range(len(filter_by)):
        if filter_by[index] != _bin:
            dont_keep.append(index)

    popped = 0
    for index in dont_keep:
        data['rows'].pop(index + 1 - popped)
        for attr in data['attributes']:
            data['attributes'][attr].pop(
                index - popped)
        popped += 1

    data['rows'][0].pop(
        data['rows'][0].index(max_gain_attribute))

    return data


def count_classes(column):
    classification_counters = {}
    if len(set(column)) == 1:
        classification_counters[set(column).pop()] = len(column)
        return classification_counters
    for val in column:
        if val not in classification_counters:
            classification_counters[val] = 0
        classification_counters[val] += 1
    return classification_counters


def calc_bin_entropy(data, _bin, att):
    new_data = attributes_filter(data, _bin, att)

    return entropy(count_classes(new_data['attributes']['class']).values())


def calacGainForAtt(data):

    gains = {}
    sum_of_bins_entropy = 0
    class_entropy = entropy(list(count_classes(
        data['attributes']['class']).values()))

    for att in data['attributes']:
        if att != 'class':
            for _bin in set(data['attributes'][att]):
                bin_entropy = calc_bin_entropy(copy.deepcopy(data), _bin, att)
                sum_of_bins_entropy += len(list(filter(lambda val: val == _bin, data['attributes'][att])))/len(
                    data['attributes'][att]) * bin_entropy
        gains[att] = class_entropy - sum_of_bins_entropy
        sum_of_bins_entropy = 0
    gains.pop('class')
    return gains


def id3Tree(data):

    node = {}

    if len(data['attributes']) == 1:
        _class = FindingCommonValue(data['attributes']['class'])
        node['attribute'] = _class
        node['nodes'] = None
        return node

    gains = calacGainForAtt(data)

    max_gain_attribute = list(
        filter(lambda key: gains[key] == max(gains.values()), gains)).pop()

    node['attribute'] = max_gain_attribute
    node['nodes'] = []

    bins = set(data['attributes'][max_gain_attribute])

    for _bin in bins:
        node['nodes'].append(
            id3Tree(attributes_filter(copy.deepcopy(data), _bin, max_gain_attribute)))

    return node


root = id3Tree(data)
print('stam')
