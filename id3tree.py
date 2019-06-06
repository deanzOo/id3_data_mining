from Functions import *
import csv
import copy


def open_files(self, path, filename):
    # Try opening train file and structure file
    self.trained_file = open(path + '' + filename, 'r')
    # Start deconstructing the files into workable data


col_file = csv.DictReader(open('train_discretization_3.csv', 'r'))

attributes = {}
for row in col_file:
    for attribute in row:
        if attribute not in attributes:
            attributes[attribute] = []
        attributes[attribute].append(row[attribute])


def attributes_filter(data, _bin, max_gain_attribute):
    # filtered_data = dict(data)

    dont_keep = []

    max_gain_attribute_column = data.pop(max_gain_attribute)

    for index in range(len(max_gain_attribute_column)):
        if max_gain_attribute_column[index] != _bin:
            dont_keep.append(index)

    popped = 0
    for index in dont_keep:
        for attr in data:
            data[attr].pop(
                index - popped)
        popped += 1

    return data


def count_categorized_instances_in_attribute(column):
    categories_counters = {}
    if len(set(column)) == 1:
        categories_counters[set(column).pop()] = len(column)
        return categories_counters
    for val in column:
        if val not in categories_counters:
            categories_counters[val] = 0
        categories_counters[val] += 1
    return categories_counters


def calc_bin_entropy(data, _bin, attribute):
    filtered_data_by_bin = attributes_filter(data, _bin, attribute)

    return entropy(count_categorized_instances_in_attribute(filtered_data_by_bin['class']).values())


def calc_gains_of_attributes(data):

    class_entropy = entropy(list(count_categorized_instances_in_attribute(
        data['class']).values()))
    if class_entropy == 0:
        return 0

    gains = {}
    sum_of_bins_entropy = 0

    for att in data:
        if att != 'class':
            for _bin in set(data[att]):
                bin_entropy = calc_bin_entropy(copy.deepcopy(data), _bin, att)
                sum_of_bins_entropy += len(list(filter(lambda val: val == _bin, data[att])))/len(
                    data[att]) * bin_entropy
        gains[att] = class_entropy - sum_of_bins_entropy
        sum_of_bins_entropy = 0
    gains.pop('class')
    return gains


def id3Tree(data):

    node = {}
    most_common = FindingCommonValue(data['class'])
    total_instances = len(data['class'])
    instances_by_common_class = len(list(filter(lambda val: val == most_common, data['class'])))
    node['instances_num'] = total_instances
    node['error'] = (total_instances + instances_by_common_class + 0.5) / total_instances

    if len(data) == 1:
        # only class column left => find most common value and create leaf
        node['attribute'] = most_common
        node['nodes'] = None 
        return node

    gains = calc_gains_of_attributes(data)

    if gains == 0:
        # gains = 0 if class_entropy = 0 which means we can decide a leaf based on common value
        # most_common = FindingCommonValue(data['class'])
        node['attribute'] = most_common
        node['nodes'] = None
        return node

    max_gain_attribute = list(
        filter(lambda key: gains[key] == max(gains.values()), gains)).pop()

    # create node using the attribute with maximum gain
    node['attribute'] = max_gain_attribute
    # create empty dict for children (each index = bin label)
    node['nodes'] = {}
    # check for labels with no repeats, sorted to be used as indexs
    bins = sorted(set(data[max_gain_attribute]))

    # for each label
    for _bin in bins:
        # => copy data to avoid mutation from lower level
        # => filter data by bin
        # => create a new sub tree from the result of id3 tree creation on the filtered data
        # => add bin to children of current node
        node['nodes'][_bin] = id3Tree(attributes_filter(
            copy.deepcopy(data), _bin, max_gain_attribute))
        # if child is not a leaf, remove attribute from data
        if node['nodes'][_bin]['nodes'] is not None:
            data.pop(node['nodes'][_bin]['attribute'])

    return node


root = id3Tree(attributes)
print(root)
