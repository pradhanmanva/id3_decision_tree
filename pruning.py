from decision_tree import *

def prune_tree(root_node,pruning_factor):
    if(root_node.left.isNode()):
        prune_tree(root_node.left,pruning_factor)

    if(root_node.right.isNode()):
        prune_tree(root_node.right,pruning_factor)

    if(root_node.left.isLeaf() and root_node.right.isLeaf()):


