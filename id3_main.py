import json
import math
import sys

import pandas as pd
import yaml

from decision_tree import *


# Read the file from the given path
def read_file(path):
    table = pd.read_csv(path)
    table = table.dropna()
    return table


# find the entropy of the given dataframe based on a column name
def find_entropy(dataframe, colname):
    total_record = len(dataframe)
    grouped = dataframe.groupby(colname)
    whole_sum = 0.0
    for series in grouped:
        column_size = len(series[1])
        sum = 0.0
        y_n_group = series[1].groupby("Class")
        for y_or_n in y_n_group:
            group_size = len(y_or_n[1])
            div_value = float(group_size) / float(column_size)
            sum -= ((div_value) * math.log(div_value, 2))
        sum *= float(column_size) / float(total_record)
        whole_sum += sum
    return whole_sum


def no_of_parts(total_data, column_name):
    list_node = {column_name: []}  # DE
    tree_node = Node(column_name)
    grouped_data = total_data.groupby(column_name)
    for parts in grouped_data:
        part_dict = {str(parts[0]): []}  # de
        new_sliced_data = parts[1].drop(column_name, 1)
        part_dict[str(parts[0])], sub_node = column_at_level(new_sliced_data)  # first ard
        list_node[column_name].append(part_dict)  # de

        # sub_node = column_at_level(new_sliced_data)

        if isinstance(sub_node, str):
            tree_node.setPrediction(sub_node)
        elif parts[0] == 0:
            tree_node.insert_left(sub_node)
        else:
            tree_node.insert_right(sub_node)

    return list_node, tree_node  # first arg


def column_at_level(sliced_data):
    col_list = sliced_data.columns.values
    entropy = []
    for x in col_list:
        entropy.append(find_entropy(sliced_data, x))

    if (all_zero(entropy)):
        return str(sliced_data.iloc[0, len(col_list) - 1]), str(sliced_data.iloc[0, len(col_list) - 1])  # de 2nd param
    else:
        entropy.pop(len(entropy) - 1)
        selected_column_no = entropy.index(min(entropy))
        selected_column = col_list[selected_column_no]
        return no_of_parts(sliced_data, selected_column)


def all_zero(given_list):
    new_list = []
    for x in given_list:
        if x != 0.0:
            new_list.append(x)
    if len(new_list) == 0:
        return True
    else:
        return False


def print_tree(tree_dict):
    json.dumps(tree_dict, indent=4)
    json_tree = json.loads(json.dumps(tree_dict, indent=4))
    print(yaml.safe_dump(json_tree, allow_unicode=True, default_flow_style=False))


def predict(row, tree_dict):
    key = list(tree_dict.keys())[0]
    val = row[key]

    if list(tree_dict[key][0].keys())[0] == str(val):
        next_node = tree_dict[key][0][str(val)]
    else:
        next_node = tree_dict[key][1][str(val)]
    if isinstance(next_node, str):
        return int(next_node)
    return predict(row, next_node)


def predict_tree(row, tree):
    key = tree.getData()
    val = row[key]

    if val == 0:
        if tree.getLeftChild() is None:
            return tree.getPrediction()
        return predict_tree(row, tree.getLeftChild())
    else:
        if tree.getRightChild() is None:
            return tree.getPrediction()
        return predict_tree(row, tree.getRightChild())


def find_accuracy(df, tree_dict, tree, data_type):
    predicted_output = df.apply(lambda row: predict_tree(row, tree), axis=1)  # rename to predicted_output
    count = 0
    given_output = df["Class"]
    for i in range(len(predicted_output)):
        if predicted_output[i] == given_output[i]:
            count += 1

    print("Number of ", data_type, " instances = %d" % len(df))
    print("Number of ", data_type, " attributes = %d" % (len(df.columns.values) - 1))
    print("Accuracy: %f" % (count / len(predicted_output) * 100))


def find_error(df, tree):
    predicted_output = df.apply(lambda row: predict_tree(row, tree), axis=1)  # rename to predicted_output
    count = 0
    given_output = df["Class"]
    for i in range(len(predicted_output)):
        if predicted_output[i] == given_output[i]:
            count += 1
    return 1 - (count / len(predicted_output) * 100)


def prune_Tree(node, pruning_factor):
    leaf_nodes = node.getLeafNode()
    for i in leaf_nodes:
        parent = i.parent
        node, pruning_factor = prune_split(node, parent, pruning_factor)
    return node


def prune_split(node, parent, pruning_factor):
    temp = node
    total_cost = find_error(temp) + (0.05 * temp.get_total_nodes)
    new_tree = temp.delete(parent)
    total_cost_new = find_error(new_tree) + (0.05 * new_tree.get_total_nodes())

    if total_cost_new < total_cost:
        pruning_factor -= 1
        return new_tree, pruning_factor
    else:
        return node, pruning_factor


if __name__ == "__main__":
    cmd_line = sys.argv

    # reading and cleaning Data
    decision_data = pd.DataFrame(read_file(cmd_line[1]))
    test_data = pd.DataFrame(read_file(cmd_line[2]))
    validation_data = pd.DataFrame(read_file(cmd_line[3]))
    pruning_factor = float(cmd_line[4])

    col_list = decision_data.columns.values
    entropy = []
    for x in col_list:
        entropy.append(find_entropy(decision_data, x))
    entropy.pop(len(entropy) - 1)

    selected_column_no = entropy.index(min(entropy))
    selected_column = col_list[selected_column_no]

    tree_dict, tree = no_of_parts(decision_data, selected_column)
    print(tree_dict)
    print_tree(tree_dict)

    print("Pre-Pruned Accuracy")
    print("----------------------")
    print("Total Leaf nodes :" + str(tree.count_leaves()))
    find_accuracy(decision_data, tree_dict, tree, "Training")
    find_accuracy(test_data, tree_dict, tree, "Test")
    find_accuracy(validation_data, tree_dict, tree, "Validation")

    pruning_factor = pruning_factor * get_total_nodes(tree)
    new_Tree = prune_Tree(tree, pruning_factor)

    print("Post-Pruned Accuracy")
    print("----------------------")
    print("Total Leaf nodes :" + str(tree.count_leaves()))
    find_accuracy(decision_data, tree_dict, tree, "Training")
    find_accuracy(test_data, tree_dict, tree, "Test")
    find_accuracy(validation_data, tree_dict, tree, "Validation")
