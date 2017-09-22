import json
import math
import sys
from decision_tree import *
import pandas as pd
import yaml


def read_file(path):
    table = pd.read_csv(path)
    table = table.dropna()
    return table


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
    # node = {column_name: []}
    node  = Node(column_name)
    grouped_data = total_data.groupby(column_name)
    for parts in grouped_data:
        # part_dict = {str(parts[0]): []}
        new_sliced_data = parts[1].drop(column_name, 1)
        sub_node = column_at_level(new_sliced_data)
        if (isinstance(sub_node,str)):
            node.setPrediction(sub_node)
        elif (parts[0] == 0):
            node.insert_left(sub_node)
        else:
            node.insert_right(sub_node)
        # node[column_name].append(part_dict)
    return node


def column_at_level(sliced_data):
    col_list = sliced_data.columns.values
    entropy = []
    for x in col_list:
        entropy.append(find_entropy(sliced_data, x))

    if (all_zero(entropy)):
        return str(sliced_data.iloc[0, len(col_list) - 1])
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


def find_accuracy(df, tree_dict):
    predicted_output = df.apply(lambda row: predict(row, tree_dict), axis=1)
    count = 0
    given_output = df["Class"]
    for i in range(len(predicted_output)):
        if predicted_output[i] == given_output[i]:
            count += 1

    print("Accuracy: %f" % (count / len(predicted_output) * 100))
    # print(predicted_output)


if __name__ == "__main__":
    cmdLine = sys.argv
    print(len(sys.argv))
    print(sys.argv)

    # reading and cleaning Data
    decision_data = pd.DataFrame(read_file(cmdLine[1]))
    # print(decision_data)
    testData = pd.DataFrame(read_file(cmdLine[2]))
    # print(testData)

    col_list = decision_data.columns.values
    entropy = []
    for x in col_list:
        entropy.append(find_entropy(decision_data, x))
    entropy.pop(len(entropy) - 1)

    selected_column_no = entropy.index(min(entropy))
    selected_column = col_list[selected_column_no]
    # print(selected_column)

    tree = no_of_parts(decision_data, selected_column)
    print_inorder(tree)
    # print(tree_dict)
    # print_tree(tree_dict)
    #
    # find_accuracy(decision_data, tree_dict)
    # find_accuracy(testData, tree_dict)
