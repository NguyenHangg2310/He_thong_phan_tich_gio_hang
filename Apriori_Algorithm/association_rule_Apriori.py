'''
Sinh luật kết hợp từ frequent itemset
Lưu các luật ra file csv dưới dạng: 'Antecedents', 'Consequents', 'Confidence'
'''

from itertools import chain, combinations
from freqItemset_Apriori import apriori_from_scratch
import csv


def generate_association_rules(frequent_itemsets, min_confidence):
    association_rules = []

    for itemset, support in frequent_itemsets:
        itemset = frozenset(itemset)
        if len(itemset) < 2:
            continue
        for antecedent in powerset(itemset):
            if antecedent:
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent
                confidence = support / frequent_itemset_support(frequent_itemsets, antecedent)
                if confidence >= min_confidence:
                    association_rules.append((antecedent, consequent, confidence))

    association_rules = [(list(item[0]), list(item[1]), item[2]) for item in association_rules]

    return association_rules


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))


def frequent_itemset_support(frequent_itemsets, itemset):
    for set_item, support in frequent_itemsets:
        if set(itemset) == set(set_item):
            return support
    return 0


if __name__ == '__main__':
    # lấy ra các tập phổ biến
    frequent_itemsets = apriori_from_scratch(sp=0.01)

    # tính toán các luật kết hợp
    min_confidence = 0.6
    rules = generate_association_rules(frequent_itemsets, min_confidence)
    print(len(rules))

    # ghi ra file
    with open('../association_rules.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Antecedents', 'Consequents', 'Confidence'])
        for row in rules:
            writer.writerow([','.join(row[0]), ','.join(row[1]), row[2]])

    # in ra
    for rule in rules:
        print(rule)
        print(rule[0], '-->', rule[1], 'confidence:', rule[2])


