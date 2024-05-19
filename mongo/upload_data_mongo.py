"""
Đọc dữ liệu từ file excel và đẩy lên MongoDB
Format:
    mỗi hàng là một sản phẩm được mua
    có các cột: ['OrderID', 'ProductID', 'ProductName', 'Type', 'DeliveryDate', 'SalesAgent',
                'CustomerID','CustomerName','QuantityOrder', 'QuantityDelivery','Price', 'TotalPrice']
"""

import pandas as pd

# Kết nối tới MongoDB
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
mydb = client['customer_data']
collect = mydb['general_data']


# Hàm đọc dữ liệu
def readFile(pathFile):
    sheet_index = 1
    df = pd.read_excel(pathFile, sheet_name=sheet_index, header=2)
    df['Mã đơn hàng'] = df['Mã đơn hàng'].astype(str)
    df['Khuyến mãi / Trả thưởng'].fillna(0, inplace=True)
    df = df.drop(df[(df['Đơn giá'] == 0) | (df['Đơn giá'] == 1000) | (df['Đơn giá'] == 1)].index)
    df = df.iloc[:,:12]
    df = df.dropna()
    return df


df1 = readFile('../data/MỸ-KHỞI-TK-MÌ-CAO-CẤP-KM-T1.2023.xlsb')
df2 = readFile('../data/MỸ-KHỞI-TỔNG-KẾT-MÌ-ZEPPIN-GÓI-MÌ-LY-ZEPPIN-T2.2023.xlsb')
df3 = readFile('../data/MỸ-KHỞI-BG-TK-PHỞ-ĐỆ-NHẤT-T3.2023.xlsb')
df4 = readFile('../data/MỸ-KHỞI-FORM-TK-PHỞ-ĐỆ-NHẤT-HỦ-TIẾU-KM-T4.2023.xlsb')

# Gộp dữ liệu từ 4 file
merged_df = pd.concat([df1, df2, df3, df4], axis=0)
eng_name = ['OrderID', 'ProductID', 'ProductName', 'Type', 'DeliveryDate', 'SalesAgent', 'CustomerID','CustomerName','QuantityOrder', 'QuantityDelivery','Price', 'TotalPrice']
merged_df.columns = eng_name
merged_df['TotalPrice'] = merged_df['QuantityDelivery'] * merged_df['Price']


# Đẩy dữ liệu lên MongoDB
def postDataToMGBD(data, collection):
    data_records = data.to_dict(orient='records')

    # Chèn dữ liệu vào MongoDB
    collection.insert_many(data_records)


if __name__ == '__main__':

    try:
        postDataToMGBD(merged_df, collect)
        print('Data posted')
    except:
        print('cannot post data')