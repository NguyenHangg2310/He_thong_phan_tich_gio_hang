import pandas as pd
import json


# Đọc dữ liệu từ tệp CSV vào DataFrame
rules = pd.read_csv('association_rules.csv', dtype = str)

# Lấy danh sách tất cả mặt hàng
product_catalog = []
for a in rules['Antecedents']:
    a = str(a).split(',')
    for i in a:
        if i not in product_catalog:
            product_catalog.append(i)

for c in rules['Consequents']:
    c = str(c).split(',')
    for i in c:
        if i not in product_catalog:
            product_catalog.append(i)


def remove_from_list(y, item_to_search):
    newlist = list()
    for i in y:
        if i not in item_to_search:
            newlist.append(i)
    return newlist


def search_list(item_to_search, list_to_search = rules['Antecedents']):
    print(item_to_search)
    max_lift = 0
    item_to_recommend = ''
    for i, item in enumerate(list_to_search):
        # Nếu item mình đang kiếm nằm trong 1 Antecedent nào đó
        if set(list(item_to_search)).issubset(set(list(item.split(',')))):
            # thì add Consequents của Antecedents đó vào
            y = rules['Antecedents'][i].split(',')
            x = remove_from_list(y, item_to_search)
            item_to_recommend = rules['Consequents'][i].split(',') + x

    if item_to_recommend == '':
        item_to_recommend = []
        print(f"Oops! No product recommendations available right now!: {item_to_recommend}")
    else:
        print(f"People who bought this also bought: {item_to_recommend}")
    return item_to_search, item_to_recommend


if __name__ == '__main__':
    # Từ điển với key là 1 sản phẩm và value là các gợi ý cho sp đó
    dict_to_store = {}
    for i in range(len(product_catalog)):
        key, value = search_list([product_catalog[i]])
        dict_to_store[key[0]] = value

    # Lưu vào file json
    json_file = json.dumps(dict_to_store)
    f = open("recommend_itemsets.json","w")
    f.write(json_file)

    f.close()