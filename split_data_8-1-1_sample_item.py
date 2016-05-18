#!/bin/python
import pandas as pd
import numpy as np
from time import gmtime, strftime


def now():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

ratings_train = pd.DataFrame()
ratings_test = pd.DataFrame()
ratings_train_80 = pd.DataFrame()
ratings_test_10 = pd.DataFrame()
test_input = pd.DataFrame()
test_eval = pd.DataFrame()
test_input_10 = pd.DataFrame()
test_eval_10 = pd.DataFrame()

print now(), 'start clean'
ratings = pd.read_csv('../MLens-ratings_no_timestamp.dat', header=None, sep=' ', names=['u', 'i', 'r'])
users = (ratings['u'].unique())
print now(), 'splitting train-test'
for user in users:
    # 90-10
    items = ratings[ratings['u'] == user]['i'].unique()
    items = np.random.permutation(items)
    k = int(round(items.shape[0] * 0.9))
    train_items = items[:k]
    test_items = items[k:]
    ratings_train = ratings_train.append(ratings[(ratings['u'] == user) & (ratings['i'].isin(train_items))])
    test_transactions = ratings[(ratings['u'] == user) & (ratings['i'].isin(test_items))]
    ratings_test = ratings_test.append(test_transactions)
    # splitting test
    n = test_transactions.shape[0]
    k = int(round(n / 2.0))
    test_input = test_input.append(test_transactions.iloc[:k, :])
    test_eval = test_eval.append(test_transactions.iloc[k:, :])
    # 80-10 in 90
    k = int(round((8 / 9.0) * train_items.shape[0]))
    train_items_80 = train_items[:k]
    test_items_10 = train_items[k:]
    ratings_train_80 = ratings_train_80.append(ratings[(ratings['u'] == user) & (ratings['i'].isin(train_items_80))])
    test_transactions = ratings[(ratings['u'] == user) & (ratings['i'].isin(test_items_10))]
    ratings_test_10 = ratings_test_10.append(test_transactions)
    # splitting test
    n = test_transactions.shape[0]
    k = int(round(n / 2.0))
    test_input_10 = test_input_10.append(test_transactions.iloc[:k, :])
    test_eval_10 = test_eval_10.append(test_transactions.iloc[k:, :])

ratings_train.to_csv('./ratings_train.dat', header=False, sep=' ', index=False)
ratings_train_iuv = ratings_train[['i', 'u', 'r']]
ratings_train_iuv.to_csv('./ratings_train_iuv.dat', header=False, sep=' ', index=False)

ratings_train_80.to_csv('./ratings_train_80.dat', header=False, sep=' ', index=False)
ratings_train_80_iuv = ratings_train_80[['i', 'u', 'r']]
ratings_train_80_iuv.to_csv('./ratings_train_80_iuv.dat', header=False, sep=' ', index=False)

test_input = test_input[['u', 'i', 'r']].astype(int)
test_eval = test_eval[['u', 'i', 'r']].astype(int)

test_input_10 = test_input_10[['u', 'i', 'r']].astype(int)
test_eval_10 = test_eval_10[['u', 'i', 'r']].astype(int)

test_input.to_csv('./ratings_test_input.dat', header=False, sep=' ', index=False)
test_eval.to_csv('./ratings_test_eval.dat', header=False, sep=' ', index=False)

test_input_10.to_csv('./ratings_train_input.dat', header=False, sep=' ', index=False)
test_eval_10.to_csv('./ratings_train_eval.dat', header=False, sep=' ', index=False)

pd.DataFrame(test_eval['u'].unique()).to_csv('./target_users.dat', header=False, sep=' ', index=False)
pd.DataFrame(test_eval_10['u'].unique()).to_csv('./train_target_users.dat', header=False, sep=' ', index=False)
print now(), 'done'
