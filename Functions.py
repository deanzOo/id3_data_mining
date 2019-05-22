# Calculate Average by column index and lists of list matrix
def NumericAverage(column):
    sum = 0
    count = 0
    for index in range(len(column)):
        # if type(column[index]) == int or type(column[index]) == float:
        sum += float(column[index])
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
