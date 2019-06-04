from Functions import *


class Node:

    def __init__(self, data):
        if len(data) == 1:
            return
        selected_attribute_column = calc_best_attribute_gain(data)
        bins = set(column)
        for _bin in bins:
            for column in data:
                if column is not selected_attribute_column:
                    for val in

    # def print_node(self):
    #     print(self.data)

    def calc_bin_entropy(selected_bin, attribute_column):
        return entropy(list(filter(lambda value: value == selected_bin, attribute_column)))

    def calacGainForAtt(self, colms):

        gains = {}
        sum_of_bins_entropy = 0

        class_entropy = entropy(colms['class'].values())

        for att in colms:
            if att is not 'class':
                for b in att:
                    bin_entropy = self.calc_bin_entropy(b, att)
                    sum_of_bins_entropy += bin_entropy
                sum_of_bins_entropy = 0
            gains[att] = class_entropy - sum_of_bins_etropy

        return gains

        def id3Tree(self, exemples):

            if len(exemples) == 1:
                _class = FindingCommonValue(exemples['class'].values())
                return Node(_class)

            gains = calacGainForAtt(exemples)
            max_gain_attribute = gains.keys()[max(gains.values())]

            root = Node(max_gain_attribute, )

            root = Node(exemples)

            new_root = Node(None)

            while root == None:
                if new_root == None:
                    new_root = Node(exemples[max])
                    if 'max' in exemples:
                        del exemples['max']
                    elif root.right == None:
                        root.right = Node(exemples[max])
                        if 'max' in exemples:
                            del exemples['max']
                    else:
                        new_root.left = Node(exemples[max])
                        if 'max' in exemples:
                            del exemples['max']

        # def build_for_att_bins_and_numbers(col, bin_num)

    #     {age: 0: {yes: 4, no: 5}, 1: {yes: 4, no: 5}, 2: {yes: 4, no: 5}}
