import time
import networkx as nx
import matplotlib.pyplot as plt
import FPTree
from collections import defaultdict
import pandas as pd
from pymongo import MongoClient


def build_tree(trans, minimum_support):
    master = FPTree.FPTree()

    items = defaultdict(lambda: 0)

    for transaction in transactions:
        for item in transaction:
            items[item] += 1

    items = dict((item, support) for item, support in items.items() if support >= minimum_support * len(transactions))

    def clean_transaction(transaction):
        transaction = filter(lambda v: v in items, transaction)
        transaction_list = list(transaction)
        transaction_list.sort(key=lambda v: items[v], reverse=True)
        return transaction_list

    for transaction in map(clean_transaction, transactions):
        master.add(transaction)

    return master


def hierarchy_pos(G, root=None, width=1., vert_gap=0.1, vert_loc=0, xcenter=0.5):
    pos = {}

    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)

        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)

        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                     pos=pos, parent=root, parsed=parsed)
        return pos

    if root is None:
        root = next(iter(nx.topological_sort(G)))
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


def draw_fptree(tree, image_file = None, dpi = 300):
    G = nx.DiGraph()

    def add_nodes_edges(tree_node, parent=None):
        node_key = (tree_node.item, tree_node.count)

        if parent is None:
            G.add_node(node_key, color='red')
        else:
            G.add_node(node_key, color='pink')
            parent_key = (parent.item, parent.count)
            G.add_edge(parent_key, node_key)

        for child in tree_node.children:
            add_nodes_edges(child, parent=tree_node)

    add_nodes_edges(tree.root)

    pos = hierarchy_pos(G)

    labels = {node: f"({node[0]}: {node[1]})" for node in G.nodes()}

    plt.figure(figsize=(10,5))

    nx.draw(G, pos, with_labels=True, labels = labels, arrows=True,
            node_color=[G.nodes[node]['color'] for node in G.nodes()],
            node_size=10, edge_color='orange', font_size=6)

    if image_file != None:
        plt.savefig(image_file, dpi=dpi)

    plt.show()



if __name__ == '__main__':
    # Kết nối tới MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    mydb = client['customer_data']
    collect = mydb['general_data']

    # Lấy dữ liệu
    colName = ['OrderID', 'ProductID']
    data = collect.find({}, colName)
    dataFrame = pd.DataFrame(data).drop(columns='_id')
    dataFrame['ProductID'] = dataFrame['ProductID'].str[-3:]
    grouped = dataFrame.groupby('OrderID')['ProductID'].agg(list).reset_index()
    transactions = grouped['ProductID']


    minsup = 0.25

    # Xây dựng cây FP-tree
    tree = build_tree(transactions, minsup)

    # Vẽ cây
    draw_fptree(tree, 'FPTree.png', dpi=700)
