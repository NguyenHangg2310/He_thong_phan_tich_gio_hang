import time
import pandas as pd
from pymongo import MongoClient
from FPTree import find_frequent_itemsets


# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
mydb = client['customer_data']
collect = mydb['general_data']

# Lấy dữ liệu
colName = ['OrderID', 'ProductID']
data = collect.find({}, colName)
dataFrame = pd.DataFrame(data).drop(columns='_id')
grouped = dataFrame.groupby('OrderID')['ProductID'].agg(list).reset_index()
transactions = grouped['ProductID']


def getItemsets(transactions = transactions, minimum_support = 0, include_support=False):
    n = len(transactions)
    frequent_itemsets = find_frequent_itemsets(transactions, minimum_support=minimum_support*n, include_support=include_support)

    result = []
    for itemset, support in frequent_itemsets:
        result.append((itemset, support/n))

    result = sorted(result, key=lambda i: i[1], reverse=True)   # xắp xếp theo support giảm dần
    return result


if __name__ == '__main__':
    start = time.time()

    # Lấy ra frequent itemset
    freq_itemsets = getItemsets(minimum_support=0.01, include_support=True)

    print(len(freq_itemsets))
    for itemset, support in freq_itemsets:
        print(str(itemset) + ' ' + str(support))

    end = time.time()
    print('Thời gian chạy', str(end - start))