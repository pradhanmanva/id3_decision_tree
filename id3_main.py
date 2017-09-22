import sys
import math
import numpy as np
import pandas as pd
from decision_tree import *

def read_file(path):
    table = pd.read_csv(path)
    table = table.dropna()
    return table


def subtables(data, col, delete):
    dict = {}
    items = np.unique(data[:, col])
    count = np.zeros((items.shape[0], 1), dtype=np.int32)

    for x in range(items.shape[0]):
        for y in range(data.shape[0]):
            if data[y, col] == items[x]:
                count[x] += 1

    for x in range(items.shape[0]):
        dict[items[x]] = np.empty((count[x], data.shape[1]), dtype="|S32")
        pos = 0
        for y in range(data.shape[0]):
            if data[y, col] == items[x]:
                dict[items[x]][pos] = data[y]
                pos += 1
        if delete:
            dict[items[x]] = np.delete(dict[items[x]], col, 1)

    return items, dict

def find_entropy(S):
    items = np.unique(S)
    if items.size == 1:
        return 0
    counts = np.zeros((items.shape[0], 1))
    sums = 0
    for x in range(items.shape[0]):
        counts[x] = sum(S == items[x]) / (S.size * 1.0)
    for count in counts:
        sums += -1 * count * math.log(count, 2)
    return sums


def gain_ratio(data, col):
    items, dict = subtables(data, col, delete=False)
    total_size = data.shape[0]
    entropies = np.zeros((items.shape[0], 1))
    intrinsic = np.zeros((items.shape[0], 1))
    for x in range(items.shape[0]):
        ratio = dict[items[x]].shape[0] / (total_size * 1.0)
        entropies[x] = ratio * entropy(dict[items[x]][:, -1])
        intrinsic[x] = ratio * math.log(ratio, 2)

    total_entropy = entropy(data[:, -1])
    iv = -1 * sum(intrinsic)

    for x in range(entropies.shape[0]):
        total_entropy -= entropies[x]

    return total_entropy / iv

if __name__ == "__main__":
    cmdLine = sys.argv
    print(len(sys.argv))
    # print(sys.argv)

    trainData = read_file(cmdLine[1])
    print(trainData)
    testData = read_file(cmdLine[2])
    print(testData)
    validationData = read_file(cmdLine[3])
    print(validationData)


    col_list = trainData.columns.values
    trainingInstances = trainData.length
    entropy = []
    for x in col_list:
        entropy.append(find_entropy(trainData, x))
    entropy.pop(len(entropy) - 1)

    selected_column_no = entropy.index(min(entropy))
    selected_column = col_list[selected_column_no]
    print(selected_column)
