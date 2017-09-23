import decision_tree as dt

def prune_Tree(node, factor):
    totalnodes=dt.get_total_nodes(node)
    p_factor = factor * totalnodes

    leaf_nodes = dt.getLeafNode(node)
    for i in leaf_nodes :
        parent=i.parent
        prune_split(node,parent)


def prune_split(node,parent):
    temp=node
    total_cost=temp.error + (0.05 * temp.get_total_nodes)
    new_tree = node.delete(parent)
    total_cost_new = new_tree.error +(0.05* new_tree.get_total_nodes())
    node = node.delete(new_tree)
    if(total_cost_new<total_cost):
        new_tree.pr