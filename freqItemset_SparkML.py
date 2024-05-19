'''
Tìm tập phổ biến sử dụng thư viện spark ml
'''

import pandas as pd
from pyspark.sql import SparkSession
from pymongo import MongoClient
from pyspark.ml.fpm import FPGrowth
import warnings
warnings.filterwarnings('ignore')


# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
mydb = client['customer_data']
collect = mydb['marketBasket']

result = collect.find({}, {'Mã sản phẩm': 1, '_id': 0})

# Chuyển kết quả thành một danh sách
# Tạo DataFrame từ danh sách
data = pd.DataFrame(list(result))

# Chuyển thành spark dataframe
spark = SparkSession.builder.appName("mba").getOrCreate()
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
spark.conf.set("spark.sql.execution.arrow.pyspark.fallback.enabled", "true")

df = spark.createDataFrame(data)
# df.show()

# frequent itemset - cách 1
freq_items1 = df.freqItems(['Mã sản phẩm'], 0.001)

# frequent itemset - cách 2: spark ML - FPGrowth
fp = FPGrowth(minSupport=0.001, minConfidence=0.001, itemsCol='Mã sản phẩm', predictionCol='prediction')
model = fp.fit(df)
freq_items2 = model.freqItemsets

# show result
# print('cach1: Pandas frequent itemset')
# freq_items1.show(10, False)
print('cach 2: spark ML - FPGrowth')
# print(freq_items2.count())
# freq_items2.show(100, False)


# association rule
print('association rule')
model.associationRules.filter(model.associationRules.confidence>0.15).show(20, False)

