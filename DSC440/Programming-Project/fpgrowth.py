#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:28:32 2018

@author: kefei
"""

from time import time
import itertools

class tree:
    def __init__(self, name, count, parent):
        self.name = name  #item的名称
        self.count = count  #出现次数
        self.link = None  #相同名称的但是不同路径的item
        self.parent = parent  #父节点
        self.children = {}  #子节点，可以有多个
        
    def occur(self, num_occur):
        self.count += num_occur


def create_fptree(data, min_sup):
    """
    Create a fptree for FP-growth algorithm based on dataset and minimum support
    Input: 
        data: a list of tuples contains attributes in each tuple
        min_support: minimum support that every frequent k-itemset should follows
    Return: 
        root: root of fp-tree
        header_table: a dictionary which key is the items that appears a lot in data, 
        and value is the corresponding frequency of the item.
    """
    header_table = {}  # a dictionary which key is item and value is count
    for tmp in data:
        for item in tmp:
            header_table[item] = header_table.get(item, 0) + data[tmp]
    
    _set = set(header_table.keys())
    for key in _set:  
        if header_table[key] < min_sup:
            del header_table[key]  # delete the item which frequency 
                                   # does not satisfy the minimum support
            
    if len(header_table.keys()) == 0:
        return None, None
    
    for key in header_table:
        header_table[key] = [header_table[key], None] 
     
    root = tree('null set', 1, None)  # initialize tree
    for trans, count in data.items():  
        new_d = {}
        for item in trans:
            if item in header_table:  #  check if item is frequent item
                new_d[item] = header_table[item][0]
        if len(new_d) > 0:
            ordered_list = sorted(new_d, key=new_d.get, reverse=True)  # sort in descending order
            update_tt(ordered_list, root, header_table, count)  
    return root, header_table


def update_tt(items, root, header_table, count):
    """
    Update fp-tree and header table according to the items
    Input: 
        items: the item that choose from the header_table
        root: root of fp-tree
        header_table: a dictionary which key is the items that appears a lot in data, 
            and value is the corresponding frequency of the item.
        count: the number of occurence
    Return:
        None
    """
    if items[0] in root.children:
        root.children[items[0]].occur(count)  
    else:
        root.children[items[0]] = tree(items[0], count, root)  
        if header_table[items[0]][1] == None:  
            header_table[items[0]][1] = root.children[items[0]]
        else:  
            node = header_table[items[0]][1]  
            while(node.link != None):
                node = node.link
            node.link = root.children[items[0]]
    if len(items) > 1:
        update_tt(items[1:], root.children[items[0]], header_table, count)


def find_prefix(tree):
    """
    Find the prefix path for a given item
    Input: 
        tree: fp-tree
    Return: 
        cond_pat: the conditional patterns based on a specific item
    """
    cond_pat = {}  # a dictionary which key is path and value is count
    
    while tree != None:
        prefix = []  
        node = tree
        while node.parent != None:
            prefix.append(node.name)
            node = node.parent
        if len(prefix) > 1:
            cond_pat[frozenset(prefix[1:])] = tree.count  
        tree = tree.link
    return cond_pat


def mining(root, header_table, min_sup, prefix, freq_item_list):
    """
    Mining from the bottom of the header table in order to find the frequent itemsets.
    Input: 
        root: root of fp-tree
        header_table: a dictionary which key is the items that appears a lot in data, and value is the corresponding frequency of the item.
        min_support: minimum support that every frequent k-itemset should follows
        prefix: the prefix itemsets for given item
        freq_item_list: a list of frequent itemsets
    Return: 
        None
    """
    # sort the headertable into a list in ascending order
    ordered_list = [v[0] for v in sorted(header_table.items(), key = lambda p: p[1][0])]  
    
    for pattern in ordered_list:  # start from bottum
        freq_item = prefix.copy()
        freq_item.add(pattern)
        freq_item_list.append(freq_item)
        cond_pat_base = find_prefix(header_table[pattern][1])
        cond_tree, header = create_fptree(cond_pat_base, min_sup)
        if header != None:
            mining(cond_tree, header, min_sup, freq_item, freq_item_list)


def findsubsets(S,m):
    """
    Find all the subsets of a given set.
    Input:
        S: a set that you want to find its subsets
        m: the length of subsets
    Return:
        set(itertools.combinations(S, m)): a set of subsets of S
    """
    return set(itertools.combinations(S, m))
 
    
def initial_set(data):
    """
    Initialize the dataset in order to use it easily in other functions.
    Input: 
        data: a list of tuples contains attributes in each tuple
    Return:
        dic: a dictionary of the data which value is the items in data
    """
    dic = {}
    
    for trans in data:
        dic[frozenset(trans)] = 1
    return dic


def upload_data():
    """
    This method is to read the UCI dataset as a list.
    Input: 
        None
    Return: 
        data_set: a list of tuples contains attributes in each tuple.   
    """
    with open('adult.data') as inputfile:
        data_set = list()
        for line in inputfile.readlines():
            data_set.append(line.split(',')) 
        return data_set
    
 
def generate_association(freq_pat, support, min_conf):
    """
    This method used to generate the association rules and confidence of each rule based on the frequent itemsets.
    Input:
        L: List of Lk.
        sup_set: a dictionary which key is frequent itemsets and the value is support.
        min_conf: the minimum confidence that are given to it
    Return:
        aso_rule_list: a list that contains all association rules
    """
    aso_rule_list = []
    sub_set_list = []
    
    for i in range(0, len(freq_pat)):
        for freq_set in freq_pat[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set) and freq_set != sub_set:
                    conf = support[freq_set] / support[freq_set - sub_set]   # calculate confidence
                    aso_rule = (freq_set - sub_set, sub_set, conf)
                    if (conf >= min_conf and aso_rule not in aso_rule_list):
                        aso_rule_list.append(aso_rule)  # generate association rules
            sub_set_list.append(freq_set)
    return aso_rule_list
       

def fpgrowth(data_set, min_sup):
    """
    This method is to implement the FP-growth algorithm to the dataset that we read.
    Input: 
        data_set: a list of tuples contains attributes in each tuple
        min_support: minimum support that every frequent k-itemset should follows
    Return:
        ordered_freq_pat: ordered list of frequent itemsets according to number of items in each itemset
        support: a dictionary which key is frequent itemsets and the value is support.
        association_rules: a list that contains all association rules
    """
    init_set = initial_set(data_set)
    fp_tree, header_tab = create_fptree(init_set, min_sup)
    freq_pat = []
    mining(fp_tree, header_tab, min_sup, set([]), freq_pat)
    subset_list = []
    
    for item in freq_pat:
        for i in range(1, len(item)):
            subset = findsubsets(item, i)
            for k in subset:
                if set(k) not in freq_pat and set(k) not in subset_list:
                    subset_list.append(set(k))
                    freq_pat.append(k)
        
    freq_pat.sort(key = lambda s: len(s))
    ordered_freq_pat = []
    for i in range(1, len(max(freq_pat, key=len))+1):
        tmp = []
        for j in freq_pat:
            if len(j) == i:
                tmp.append(frozenset(j))
        ordered_freq_pat.append(tmp)  # sort the frequent itemsets by length
        
    _count = {}
    support = {}    
    for t in data_set:
        for i in range(0, len(ordered_freq_pat)):  
            for item in ordered_freq_pat[i]:
                if item.issubset(t):
                    if item not in _count:
                        _count[item] = 1
                    else:
                        _count[item] += 1
    t_num = float(len(data_set))
    
    for item in _count:
        support[item] = _count[item] / t_num  # calculate support
    
    association_rules = generate_association(ordered_freq_pat, support, min_conf = 0.7)
    return ordered_freq_pat, support, association_rules


def display(freq_pat, support, association_rules):
    """
    This method is to print the frequent patterns that the project got.
        freq_items: List of frequent itemsets.
        support: a dictionary which key is frequent itemsets and the value is support.
    Return: 
        None
    """
    freq_pat.append([])
    i = 0
    while len(freq_pat[i]) != 0:
        i += 1
        for item in freq_pat[0:i]:
            print("="*50)
            print("frequent {}-itemsets".format(str(len(list(item)[0]))))
            for freq_set in item:
                print(freq_set)
                print("Support =" + str(support[freq_set]))
    print("="*50)
    print("Association Rules Are As Follows:")
    for i in association_rules:
        print(str(list(i[0])) + "-->" + str(list(i[1])))
        print("Confidence = " + str(i[2]))
  
def main():      
    data_set = upload_data()
    Min_support = 0.23
    frequentItems, support, association_rules = fpgrowth(data_set, Min_support*len(data_set))
    display(frequentItems, support, association_rules)
    
if __name__ == "__main__":
    start = time()
    main()
    stop = time()
    print("Processing time is "+str(stop-start)+" seconds")
