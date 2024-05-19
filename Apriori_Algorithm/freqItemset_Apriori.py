import time

import pandas as pd
from pymongo import MongoClient
import warnings
import numpy as np
from collections import Counter

warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
mydb = client['customer_data']
collection = mydb['general_data']


# Lấy dữ liệu
def getDataFromMGDB(collectName, colName):
    data = collectName.find({}, colName)
    dataFrame = pd.DataFrame(data)
    return dataFrame


colName = ['OrderID', 'ProductID']  # Thay đổi các cột muốn lấy ở đây
data = getDataFromMGDB(collection, colName)
transactions = data.groupby('OrderID')['ProductID'].agg(list).reset_index()


# Xây dựng thuật toán apriori
def apriori_from_scratch(transactions = transactions, sp = 0):
    init = set()
    for transaction in transactions['ProductID']:
        init.update(transaction)
    init = np.array(list(init))
    s = sp
    n=len(transactions)

    c = Counter()
    for i in init:
        for d in transactions['ProductID']:
            if (i in d):
                c[i] += 1

    l = Counter()
    for i in c:
        if (c[i]/n >= s):
            l[frozenset([i])] += c[i]

    pl = l
    pos = 1
    L = []
    for itemset, support in pl.items():
        L.append((list(itemset), support/n))

    for count in range(2, 1000):
        nc = set()
        temp = list(l)
        for i in range(0, len(temp)):
            for j in range(i + 1, len(temp)):
                t = temp[i].union(temp[j])
                if (len(t) == count):
                    nc.add(temp[i].union(temp[j]))
        nc = list(nc)
        c = Counter()
        for i in nc:
            c[i] = 0
            for q in transactions['ProductID']:
                temp = set(q)
                if (i.issubset(temp)):
                    c[i] += 1

        l = Counter()
        for i in c:
            if (c[i]/n >= s):
                l[i] += c[i]

        if (len(l) == 0):
            break
        pl = l
        pos = count

        for itemset,support in pl.items():
            L.append((list(itemset),support/n))

    L = sorted(L, key=lambda i: i[1], reverse=True)   # xắp xếp theo support giảm dần
    return L
    # return pd.DataFrame(L, columns=['Itemset', 'Support'])


if __name__ == '__main__':
    start = time.time()

    # Lấy ra frequent itemset
    freq_itemsets = apriori_from_scratch(transactions, 0.01)

    print(len(freq_itemsets))
    for itemset, support in freq_itemsets:
        print(str(itemset) + ' ' + str(support))

    end = time.time()
    print('Thời gian chạy', str(end - start))


