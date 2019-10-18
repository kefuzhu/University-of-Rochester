#!/usr/bin/python3
# Signature: Kefu Zhu

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

def find_frequent_1_itemsets(db):
    """
    Find frequent candidate 1-itemset C1.   
    """

    C1 = set()
    
    for i in db:
        for attr in i:
            attr_set = frozenset([attr])
            C1.add(attr_set)
    return C1


def has_infrequent_subset(item_in_Ck, Lk_sub1, l1, l2):
    """
    Check whether any item in item_in_Ck has infrequent subset
    """

    for attr in item_in_Ck:
        sub_Ck = item_in_Ck - frozenset([attr])
        ##############
        # Improvment #
        ##############
        
        # Since we know l1 and l2 are frequent, we do not need to check them against Lk_sub1 again,
        # where Lk_sub1 can potentially be a very long list if the dataset is huge
        if (sub_Ck == l1) or (sub_Ck) == l2:
            pass
        elif sub_Ck not in Lk_sub1:
            return True

    return False


def find_Ck(Lk_sub1, k):
    """
    find candidate k-itemsets Ck by Lk-1.
    """

    Ck = set()
    _len = len(Lk_sub1)
    _list = list(Lk_sub1)
    
    for i in range(_len):
        for j in range(1, _len):
            l1 = sorted(list(_list[i]))
            l2 = sorted(list(_list[j]))
            if l1[0:k-2] == l2[0:k-2]:
                item_in_Ck = _list[i] | _list[j]
                if has_infrequent_subset(item_in_Ck, Lk_sub1, l1, l2): 
                    pass
                else:
                    Ck.add(item_in_Ck)
    return Ck


def find_Lk(db, Ck, min_sup, sup_set):
    """
    Find frequent k-itemset Lk and calculate support for each frequent k-itemsets.
    """

    Lk = set()
    frequency = {}
    
    for transaction in db:
        for item in Ck:
            if item.issubset(transaction):
                if item not in frequency:
                    frequency[item] = 1  
                else:
                    frequency[item] += 1
                    
    transaction_num = float(len(db))
    for item in frequency:
        if (frequency[item]/transaction_num) >= min_sup:
            Lk.add(item)
            sup_set[item] = frequency[item]/transaction_num
    return Lk


def find_L(db, k, min_sup):
    """
    Find all frequent itemsets.    
    """
    import copy
    sup_set = {}
    C1 = find_frequent_1_itemsets(db)
    L1 = find_Lk(db, C1, min_sup, sup_set)
    Lk_sub1 = copy.deepcopy(L1)
    L = []
    L.append(Lk_sub1)
    print('Completed mining frequent 1-itemsets!')
    
    for i in range(2, k+1):
        Ci = find_Ck(Lk_sub1, i)
        Li = find_Lk(db, Ci, min_sup, sup_set)
        Lk_sub1 = copy.deepcopy(Li)
        L.append(Lk_sub1)
        print('Competed mining frequent {}-itemsets!'.format(i))
        
    return L, sup_set

def main():
    import time
    start = time.time()
    min_support = 0.2
    db = create_database(file = 'adult.data')
    
    # Number of attributes in the database
    k = len(db[0])
    # Find all frequent itemsets and their supports
    print('Start mining all frequent itemsets using Apriori with minimum support = {}...'.format(min_support))
    L, sup_set = find_L(db, k, min_sup = min_support)

    # Print all frequent itemsets (Comment the following code out if needed)
    i = 0
    while len(L[i]) != 0:
        i += 1
        for Lk in L[0:i]:
            print("#"*50)
            print("Frequent {}-itemsets".format(len(list(Lk)[0])))
            for freq_set in Lk:
                print(freq_set)
                print("Support: {:.2f}".format(sup_set[freq_set]))

    stop = time.time()
    print()
    print("Frequent pattern mining using Apriori took {:.2f} minutes".format((stop-start)/60))

if __name__ == "__main__":   
    main()
    