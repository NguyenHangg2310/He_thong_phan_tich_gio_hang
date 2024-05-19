"""This file is to delete mongoDB collection if u want"""

from pymongo import MongoClient

if __name__ == '__main__':

    client = MongoClient('mongodb://localhost:27017/')
    mydb = client['customer_data']
    collection = mydb['general_data']

    mydb.drop_collection(collection)
    print('collection deleted')
