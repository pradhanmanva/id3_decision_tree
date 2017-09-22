class Node:
    def __init__(self, data, error=None, left=None, right=None):
        self.data = data
        self.error = error
        self.left = left
        self.right = right
        self.prediction = None

    def getPrediction(self):
        return self.prediction

    def setPrediction(self, value):
        self.prediction = value

    def getLeftChild(self):
        return self.left

    def getRightChild(self):
        return self.right

    def getData(self):
        return self.data

    def getError(self):
        return self.error

    def setData(self, value):
        if self.data is not None:
            self.data = value
        else:
            return None

    def setError(self, value):
        if self.error is not None:
            self.error = value
        else:
            return None

    def insert_left(self, new_data):
        self.left = new_data

    def insert_right(self, new_data):
        self.right = new_data

    def is_leaf(self):
        return self.right is None and self.left is None

    def is_node(self):
        return self.right is not None or self.left is not None

    def count_leaves(self):
        if self.is_leaf():
            return 1
        count = 0
        if self.right is not None:
            count += self.right.count_leaves()
        if self.left is not None:
            count += self.left.count_leaves()
        return count


def print_inorder(tree):
    if tree:
        print(tree.data)
        print_inorder(tree.left)
        print_inorder(tree.right)
