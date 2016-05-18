#!/usr/bin/python
import pandas as pd
import numpy as np
import StringIO
import sys
import matplotlib.pyplot as plt


def compare(ltype, drec, deva, target_user, count, calcResult):
    recall = 0
    precision = 0
    rec_user = drec.keys()
    for i in rec_user:
        t = set(deva[i])
        r = set(drec[i])
        k = len(r)
        c_num = len(t.intersection(r))
        recall += c_num * 1.0 / len(t)
        precision += c_num * 1.0 / k
    recall /= len(rec_user)
    precision /= len(rec_user)
    user_coverage = len(rec_user) * 1.0 / len(target_user)
    calcResult.loc[count] = [ltype, precision, recall, user_coverage]
    print ltype, precision, recall, user_coverage


resultK = pd.DataFrame(columns=['Type', 'Precision', 'Recall', 'User Coverage'])

numlist = len(sys.argv) - 1
eva = pd.read_csv('./ratings_train_eval.dat', sep=' ', header=None, names=['u', 'v', 'w'])
deva = {k: g["v"].tolist() for k, g in eva.groupby("u")}
target_user = pd.read_csv('./train_target_users.dat', sep=' ', header=None)
target_user = target_user[0]
print 'list_type', 'precision', 'recall', 'user_coverage'
for i in np.arange(numlist):
    listpath = sys.argv[i + 1]
    reclist = pd.read_csv(listpath, delimiter=' ', names=['u', 'v', 'w'])
    drec = {k: g["v"].tolist() for k, g in reclist.groupby("u")}
    compare(listpath, drec, deva, target_user, i, resultK)


