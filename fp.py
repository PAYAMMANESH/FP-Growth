class Node:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.next = None

def read_file():
    with open('C:/Users/Payam/Desktop/InputData.txt', 'r') as file:
        lines = file.readlines()


    lines = [''.join(filter(str.isalpha, line)) for line in lines]


    dataset = [list(line) for line in lines]
    dataset.pop()
    dataset.pop(0)
    return dataset


def create_tree(dataset, min_support):
    header_table = {}
    for transaction, count in dataset.items():
        for item in transaction:
            header_table[item] = header_table.get(item, 0) + count

    header_table = {k: v for k, v in header_table.items() if v >= min_support}
    frequent_items = set(header_table.keys())
    if len(frequent_items) == 0:
        return None, None

    for item in header_table:
        header_table[item] = [header_table[item], None]

    root = Node("Null", 1, None)
    for transaction, count in dataset.items():
        filtered_transaction = [item for item in transaction if item in frequent_items]
        filtered_transaction.sort(key=lambda x: (header_table[x][0], x), reverse=True)
        insert_tree(filtered_transaction, root, header_table, count)

    return root, header_table

def insert_tree(items, node, header_table, count):
    if items[0] in node.children:
        node.children[items[0]].count += count
    else:
        node.children[items[0]] = Node(items[0], count, node)
        if header_table[items[0]][1] is None:
            header_table[items[0]][1] = node.children[items[0]]
        else:
            update_link(header_table[items[0]][1], node.children[items[0]])

    if len(items) > 1:
        insert_tree(items[1:], node.children[items[0]], header_table, count)

def update_link(node, target_node):
    while node.next is not None:
        node = node.next
    node.next = target_node

def ascend_tree(node, prefix_path):
    if node.parent is not None:
        prefix_path.append(node.item)
        ascend_tree(node.parent, prefix_path)

def find_prefix_path(base_pattern, header_table):
    base_node = header_table[base_pattern][1]
    cond_pats = {}
    while base_node is not None:
        prefix_path = []
        ascend_tree(base_node, prefix_path)
        if len(prefix_path) > 1:
            cond_pats[tuple(prefix_path[1:])] = base_node.count
        base_node = base_node.next
    return cond_pats

def find_suffix_path(base_pattern, header_table):
    base_node = header_table[base_pattern][1]
    cond_pats = {}
    while base_node.next is not None:
        base_node = base_node.next
        suffix_path = []
        ascend_tree(base_node, suffix_path)
        if len(suffix_path) > 1:
            cond_pats[tuple(suffix_path[1:])] = base_node.count
    return cond_pats

def mine_tree(node, header_table, min_support, prefix, frequent_items):
    for item in header_table:
        new_freq_set = prefix.copy()
        new_freq_set.add(item)
        if header_table[item][0] >= min_support:
            frequent_items.append((new_freq_set, header_table[item][0]))

            cond_patt_bases = find_prefix_path(item, header_table)
            cond_patt_bases.update(find_suffix_path(item, header_table))

            cond_tree, cond_header_table = create_tree(cond_patt_bases, min_support)

            if cond_header_table is not None:
                mine_tree(cond_tree, cond_header_table, min_support, new_freq_set, frequent_items)

def fpgrowth(dataset, min_support):
    tree, header_table = create_tree(dataset, min_support)
    frequent_items = []
    mine_tree(tree, header_table, min_support, set(), frequent_items)
    return frequent_items


min_support = int(input("min support: "))


dataset = read_file()


dataset_counted = {tuple(transaction): 1 for transaction in dataset}


frequent_itemsets = fpgrowth(dataset_counted, min_support)


with open('C:/Users/Payam/Desktop/Output.txt', 'w') as output_file:
    for itemset, support in frequent_itemsets:
        if support >= min_support and len(itemset) > 1:  
            itemset_str = ', '.join(sorted(itemset))
            output_file.write(f"<{itemset_str}:{support}>\n")

