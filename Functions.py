from math import log

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
    vals = [float(v) / norm for v in vals]
    for v in vals:
        sum += (v * log(v, 2)) if v != 0 else 0
    return -1.0 * sum
