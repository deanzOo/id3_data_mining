from Functions import *
from id3tree import *
import csv


def pre_order_pruning(tree):
    pre_order_pruning(tree)


def pessimistic_error_pruning(tree):
    if tree['nodes'] == None:
        return tree
    for node in tree['nodes']:
        tree['nodes'][node] = pessimistic_error_pruning(tree['nodes'][node])
    if should_prune(tree):
        tree['attribute'] = tree['most_common']
        tree['nodes'] = None
    return tree


def should_prune(tree):

    def subtree_error(tree):
        counts = {
            'total_error': 0,
            'instances_num': 0
        }
        if tree['nodes'] == None:
            counts['total_error'] += tree['error']
            counts['instances_num'] += tree['instances_num']
        else:
            for node in tree['nodes']:
                subtree_count = subtree_error(tree['nodes'][node])
                counts['total_error'] += subtree_count['total_error']
                counts['instances_num'] += subtree_count['instances_num']
        return counts

    qv = tree['error']
    counts = subtree_error(tree)
    qt = counts['total_error'] / counts['instances_num']

    return qv <= qt


# pessimistic_error_pruning(id3Tree(attributes, None)) ------------- RUN EXAMPLE, RESULTS IN TREE AFTER PRUNING
pruned_tree = pessimistic_error_pruning(id3Tree(attributes, None))

with open('rules.csv', mode='w', newline='') as rules_file:
    rules_writer = csv.writer(
        rules_file, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')

    # rules_writer.writerow(['John Smith', 'Accounting', 'November'])
    # rules_writer.writerow(['Erica Meyers', 'IT', 'March'])

    sweep_tree(pruned_tree, [], rules_writer)
    rules_file.close()
