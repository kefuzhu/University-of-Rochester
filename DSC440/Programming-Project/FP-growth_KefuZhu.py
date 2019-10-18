#!/usr/bin/python3
# Signature: Kefu Zhu

from time import time
import itertools

# Class defnied for treeNode in the FP-Tree
class treeNode:
    def __init__(self, item, count, parent):
        # Item contained in the node
        self.item = item
        # The frequency of the item
        self.count = count
        # The link between similar items
        self.nodeLink = None
        # Parent node
        self.parent = parent
        # Child nodes
        self.children = {}
        
    def increment(self, num_occur):
        self.count += num_occur

    # Print out the tree in text, mainly used for debugging
    def display(self, ind=1):
        print(' '*ind + self.name + ' ' + self.count)
        for child in self.children.values():
            child.disp(ind+1)

def createTree(db, min_sup):
    """
    Create a fptree for FP-growth algorithm based on database and minimum support
    """

    # The header table contains the names of all items and their counts
    headerTable = {}

    # Fill the header table
    for transaction in db:
        for item in transaction:
            headerTable[item] = headerTable.get(item, 0) + db[transaction]
    
    itemSet = set(headerTable.keys())
    # Remove items from header table if not meeting the minimum support
    for item in itemSet:  
        if headerTable[item] < min_sup:
            del headerTable[item]
    
    # Return None if the header table is empty (no items meet minimum support)
    if not headerTable:
        return None, None
    
    for key in headerTable:
        headerTable[key] = [headerTable[key], None] 
    
    # Create the root of tree (Null set)
    root = treeNode('Ø (Null Set)', 1, None)

    # Iterate over all transactions in the database
    for trans, count in db.items():
        # Initialize a dictionary to store 
        new_d = {}
        for item in trans:
            # If the item in header table (aka. The item is frequent)
            if item in headerTable:
                new_d[item] = headerTable[item][0]
        if len(new_d) > 0:
            ordered_list = sorted(new_d, key=new_d.get, reverse=True)  # sort in descending order
            updateTree(ordered_list, root, headerTable, count)

    return root, headerTable

def updateTree(items, root, headerTable, count):
    """
    Update fp-tree and header table according to the items
    """
    if items[0] in root.children:
        root.children[items[0]].increment(count)  
    else:
        root.children[items[0]] = treeNode(items[0], count, root)  
        if headerTable[items[0]][1] == None:  
            headerTable[items[0]][1] = root.children[items[0]]
        else:  
            node = headerTable[items[0]][1]  
            while(node.nodeLink != None):
                node = node.nodeLink
            node.nodeLink = root.children[items[0]]
    if len(items) > 1:
        updateTree(items[1:], root.children[items[0]], headerTable, count)


def find_prefix(tree):
    """
    Find the prefix path for a given item
    """

    # Initialize a dictionary to store the list of prefix
    # Note: Key is the prefix and value is the number of the occurence
    cond_pattern = {}
    
    while tree is not None:
        prefix = []  
        node = tree
        # If this is not the root node
        while node.parent != None:
            # Add the item to the prefix
            prefix.append(node.item)
            # Move to its parent node
            node = node.parent
        if len(prefix) > 1:
            cond_pattern[frozenset(prefix[1:])] = tree.count

        tree = tree.nodeLink
    return cond_pattern


def mine(root, headerTable, min_sup, prefix, freq_item_list):
    """
    Mine frequent patterns (itemsets) 
    """

    # sort the headertable into a list in ascending order
    ordered_list = [v[0] for v in sorted(headerTable.items(), key = lambda p: p[1][0])]  
    
    for pattern in ordered_list:  # start from bottum
        freq_item = prefix.copy()
        freq_item.add(pattern)
        freq_item_list.append(freq_item)
        cond_pattern_base = find_prefix(headerTable[pattern][1])
        cond_tree, header = createTree(cond_pattern_base, min_sup)
        # Recursively mine the frequent patterns
        if header != None:
            mine(cond_tree, header, min_sup, freq_item, freq_item_list) 
    
def createInitSet(db):
    """
    Initialize the database, {'Transaction#1':1, 'Transaction#2':1, ...}
    """

    # Initialize a dictionary to store all transactions
    d = {}
    # For each transaction in the database, record it in the dictionary and set frequency to 1
    for trans in db:
        d[frozenset(trans)] = 1

    return d

def create_database(file):
    """
    Read the UCI dataset as a list. 
    """

    print('Opening input file...')
    with open(file) as f:
        print('Loading data from input file...')
        database = list()
        for line in f.read().splitlines():
            database.append(line.split(', '))
        print('Complete the construction of database!')
        return database

def FP_Growth(db, min_sup):
    """
    Main function that mines frequent pattern in a given database based on minimum support
    """

    # Transform the database
    initSet = createInitSet(db)
    # Create FP-Tree
    fp_tree, header_tab = createTree(initSet, min_sup)
    # Inialize an empty list to store thee frequent patterns
    freq_pattern = []
    # Mine the frequent patterns
    mine(fp_tree, header_tab, min_sup, set([]), freq_pattern)
    # Initialize an empty list to store subsets
    subset_list = []
    
    # For each items frequent pattern list
    for item in freq_pattern:
        # For different lenght of subsets
        for i in range(1, len(item)):
            # Find all the length of i-subsets of item
            subset = set(itertools.combinations(item, i))
            for k in subset:
                if set(k) not in freq_pattern and set(k) not in subset_list:
                    subset_list.append(set(k))
                    freq_pattern.append(k)
    
    freq_pattern.sort(key = lambda s: len(s))
    ordered_freq_pattern = []

    # Sort the frequent patterns by length
    for i in range(1, len(max(freq_pattern, key=len))+1):
        tmp = []
        for pattern in freq_pattern:
            if len(pattern) == i:
                tmp.append(frozenset(pattern))
        ordered_freq_pattern.append(tmp)
        
    # Compute frequency of each pattern
    count_dict = {}

    # Iterate over each transaction in the database
    for transaction in db:
        for pattern in ordered_freq_pattern:
            for item in pattern:
                if item.issubset(transaction):
                    # If this is the first time seeing the item
                    if item not in count_dict:
                        count_dict[item] = 1
                    # If the item is already in the dictionary, increment the frequency count by one
                    else:
                        count_dict[item] += 1

    # Total number of transactions in the database
    num_transaction = float(len(db))
    
    # Compute the support for each item
    support = {}  
    for item in count_dict:
        support[item] = count_dict[item] / num_transaction  

    return ordered_freq_pattern, support
  
def main():
    import time
    
    start = time.time()
    db = create_database(file = 'adult.data')
    # Minimum support
    min_support = 0.2
    # Mine the data using FP-Growth
    frequentItems, support = FP_Growth(db, min_support*len(db))
    # Print all frequent itemsets (Comment the following code out if needed)
    frequentItems.append([])
    i = 0
    while len(frequentItems[i]) != 0:
        i += 1
        for item in frequentItems[0:i]:
            print("="*50)
            print("frequent {}-itemsets".format(str(len(list(item)[0]))))
            for freq_set in item:
                print(freq_set)
                print("Support: {:.2f}".format(support[freq_set]))

    stop = time.time()

    print()
    print("Frequent pattern mining using FP-growth took {:.2f} minutes".format((stop-start)/60))
    
if __name__ == "__main__":
    main()
