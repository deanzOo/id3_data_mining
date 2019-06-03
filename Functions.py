from math import log
import sys
import time
from functools import reduce
# Calculate Average by column index and lists of list matrix


def NumericAverage(column):
    sum = 0
    count = 0
    for index in range(len(column)):
        # if type(column[index]) == int or type(column[index]) == float:
        if column[index] == '':
            addition = 0
        else:
            addition = float(column[index])
        sum += addition
        count += 1
        # else:
        # print('The Value is NOT Numeric or the cell is Empty')
    average = sum / count
    return average


def FindingCommonValue(column):
    my_dict = {}
    for key in column:
        if (key not in my_dict):
            my_dict[key] = 1
        else:
            my_dict[key] += 1
    return [k for k in my_dict.keys() if my_dict[k] == max(my_dict.values())][0]


def entropy(vals):
    sum = 0.0
    norm = 0.0
    for v in vals:
        norm += v
    if norm == 0:
        return 0
    vals = [v / norm for v in vals]
    for v in vals:
        sum += (v * log(v, 2)) if v != 0 else 0
    return -1.0 * sum


def calc_info(entropy_table, total_number_of_instances):
    info = 0
    for section in entropy_table:
        section_values = entropy_table[section].values()
        total_instances_in_section = reduce(
            lambda x, y: x + y, section_values)
        part = total_instances_in_section / total_number_of_instances
        info += part * entropy(section_values)
    return info


def calc_gain(split_point, column, entropy_table, total_number_of_instances, total_entropy):
    return total_entropy - calc_info(entropy_table, total_number_of_instances)


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
