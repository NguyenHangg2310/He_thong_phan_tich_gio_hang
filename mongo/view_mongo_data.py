"""This file is just to view data"""

import pandas as pd
from pymongo import MongoClient
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
mydb = client['customer_data']
collect = mydb['general_data']


def getDataFromMGDB(collectName, colName):
    data = collectName.find({}, colName)
    dataFrame = pd.DataFrame(data).drop(columns='_id')
    return dataFrame


def view_general():
    colName = ['OrderID', 'ProductID', 'ProductName', 'Type', 'DeliveryDate', 'SalesAgent', 'CustomerID','CustomerName','QuantityOrder', 'QuantityDelivery','Price', 'TotalPrice']
    data = getDataFromMGDB(collect, colName)
    print(data)


def view_basket():
    colName = ['OrderID', 'ProductID']  # Thay đổi các cột muốn lấy ở đây
    data = getDataFromMGDB(collect, colName)

    grouped = data.groupby('OrderID')['ProductID'].agg(list).reset_index()
    print(grouped)


if __name__ == '__main__':
    # view_general()
    view_basket()