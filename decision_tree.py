class Tree:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.data)

    def getLeftChild(self):
        return self.left

    def getRightChild(self):
        return self.right

    def getData(self):
        return self.data

    def setLeftChild(self, value):
        if self.left is not None:
            self.left = value
        else:
            return None

    def setRightChild(self,value):
        if self.right is not None:
            self.right = value
        else:
            return None

    def setData(self,value):
        if self.data is not None:
            self.data = value
        else:
            return None


def print_inorder(tree):
    if(tree is not None):
        print_inorder(tree.left)
        print(tree.data)
        print_inorder(tree.right)



