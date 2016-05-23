#!/bin/python
import pandas as pd
import numpy as np
from time import gmtime, strftime


def now():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())


print now(), 'start clean'
ratings = pd.read_csv('../../MLens-ratings_no_timestamp.dat', header=None, sep=' ', names=['u', 'i', 'r'])
users = (ratings['u'].unique())
users = np.random.permutation(users)
k = int(users.shape[0] * 0.9)
train_user = users[:k]
test_user = users[k:]
print now(), 'spliting train-test'
ratings_train = ratings[ratings['u'].isin(train_user)].copy()
ratings_test = ratings[ratings['u'].isin(test_user)].copy()
ratings_train.to_csv('./ratings_train.dat', header=False, sep=' ', index=False)
ratings_train_iuv = ratings_train[['i', 'u', 'r']]
ratings_train_iuv.to_csv('./ratings_train_iuv.dat', header=False, sep=' ', index=False)


k = int((8 / 9.0) * train_user.shape[0])
train_user_80 = train_user[:k]
test_user_10 = train_user[k:]
ratings_train_80 = ratings[ratings['u'].isin(train_user_80)].copy()
ratings_test_10 = ratings[ratings['u'].isin(test_user_10)].copy()
ratings_train_80.to_csv('./ratings_train_80.dat', header=False, sep=' ', index=False)
ratings_train_80_iuv = ratings_train_80[['i', 'u', 'r']]
ratings_train_80_iuv.to_csv('./ratings_train_80_iuv.dat', header=False, sep=' ', index=False)

test_input = pd.DataFrame()
test_eval = pd.DataFrame()

test_input_10 = pd.DataFrame()
test_eval_10 = pd.DataFrame()

print now(), 'spliting test data'
for u in test_user:
    transactions = ratings_test[ratings_test['u'] == u]
    n = transactions.shape[0]
    k = int(n / 2)
    test_input = test_input.append(transactions.iloc[:k, :])
    test_eval = test_eval.append(transactions.iloc[k:, :])

for u in test_user_10:
    transactions = ratings_test_10[ratings_test_10['u'] == u]
    n = transactions.shape[0]
    k = int(n / 2)
    test_input_10 = test_input_10.append(transactions.iloc[:k, :])
    test_eval_10 = test_eval_10.append(transactions.iloc[k:, :])

# for i in xrange(k):
#        test_input = test_input.append(transactions.iloc[i,:])
#    for j in xrange(k,n):
#        test_eval = test_eval.append(transactions.iloc[j,:])
test_input = test_input[['u', 'i', 'r']].astype(int)
test_eval = test_eval[['u', 'i', 'r']].astype(int)

test_input_10 = test_input_10[['u', 'i', 'r']].astype(int)
test_eval_10 = test_eval_10[['u', 'i', 'r']].astype(int)

test_input.to_csv('./ratings_test_input.dat', header=False, sep=' ', index=False)
test_eval.to_csv('./ratings_test_eval.dat', header=False, sep=' ', index=False)

test_input_10.to_csv('./ratings_train_input.dat', header=False, sep=' ', index=False)
test_eval_10.to_csv('./ratings_train_eval.dat', header=False, sep=' ', index=False)

pd.DataFrame(test_input['u'].unique()).to_csv('./target_users.dat', header=False, sep=' ', index=False)
pd.DataFrame(test_input_10['u'].unique()).to_csv('./train_target_users.dat', header=False, sep=' ', index=False)
print now(), 'done'
