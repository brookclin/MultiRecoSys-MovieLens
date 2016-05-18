#!/usr/bin/python
import pandas as pd
import numpy as np
import StringIO
import sys
import matplotlib.pyplot as plt
import os
from time import gmtime, strftime


def now():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

outfile = open("outfile", "w")
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
    # print ltype, precision, recall, user_coverage


resultK = pd.DataFrame(columns=['Type', 'Precision', 'Recall', 'User Coverage'])
resultAlpha = pd.DataFrame(columns=['Alpha', 'Precision', 'Recall', 'User Coverage'])
resultR = pd.DataFrame(columns=['Alpha', 'Precision', 'Recall', 'User Coverage'])

# Phase 1: compute results on 80-10 train set
numlist = len(sys.argv) - 1
eva = pd.read_csv('./ratings_train_eval.dat', sep=' ', header=None, names=['u', 'v', 'w'])
deva = {k: g["v"].tolist() for k, g in eva.groupby("u")}
target_user = pd.read_csv('./train_target_users.dat', sep=' ', header=None)
target_user = target_user[0]
for i in np.arange(numlist):
    listpath = sys.argv[i + 1]
    reclist = pd.read_csv(listpath, delimiter=' ', names=['u', 'v', 'w'])
    drec = {k: g["v"].tolist() for k, g in reclist.groupby("u")}
    compare(listpath, drec, deva, target_user, i, resultK)
print >> outfile, resultK.sort_values('Precision', ascending=False)
print now(), "Phase 1 on 80-10 train set done."
# Phase 2
bestSet = resultK.sort_values('Precision', ascending=False).iloc[0:2, :]['Type'] # Names of the best Reco systems
resultBestSet = pd.DataFrame(columns=['Type', 'Precision', 'Recall', 'User Coverage'])

eva = pd.read_csv('./ratings_test_eval.dat', sep=' ', header=None, names=['u', 'v', 'w'])
deva = {k: g["v"].tolist() for k, g in eva.groupby("u")}
target_user = pd.read_csv('./target_users.dat', sep=' ', header=None)
target_user = target_user[0]
users = target_user.unique()

# Generate new recommended lists on 90-10 split, top 5 methods with best precision
finalSets = list()
for i in np.arange(2):
    methodNames = bestSet.iloc[i]
    print methodNames
    methodName = methodNames.split('_')  # eg.: recavg_ib_cos
    name_test = methodName[1] + "_" + methodName[2] + "_test"
    if methodName[1] == 'ub':
        degreearg = "python ../complete_degrees_ML.py ub ./similarity_" + name_test
        sfarg = "../socialfiltering -u 6041 -i 3953 -r ratings_train.dat -t target_users.dat -l ratings_test_input.dat -g similarity_" + name_test + "_complete -k 10 -a weighted_" + name_test + " > ./avg_" + name_test
        if methodName[2] == 'cos':
            simarg = "../sim-cosine -u 6041 -i 3953 -r ratings_train.dat -t ratings_test_input.dat > ./similarity_" + name_test
        elif methodName[2] == 'jaccard':
            simarg = "../sim-jaccard -u 6041 -i 3953 -r ratings_train.dat -t ratings_test_input.dat > ./similarity_" + name_test
        elif methodName[2] == 'q1a0':
            simarg = "../sim-cosine -u 6041 -i 3953 -r ratings_train.dat -t ratings_test_input.dat -q 1 -a 0 > ./similarity_" + name_test
        elif methodName[2] == 'q1a0.5':
            simarg = "../sim-cosine -u 6041 -i 3953 -r ratings_train.dat -t ratings_test_input.dat -q 1 -a 0.5 > ./similarity_" + name_test
        elif methodName[2] == 'q5a0':
            simarg = "../sim-cosine -u 6041 -i 3953 -r ratings_train.dat -t ratings_test_input.dat -q 5 -a 0 > ./similarity_" + name_test
        elif methodName[2] == 'q5a0.5':
            simarg = "../sim-cosine -u 6041 -i 3953 -r ratings_train.dat -t ratings_test_input.dat -q 5 -a 0.5 > ./similarity_" + name_test
    elif methodName[1] == 'ib':
        degreearg = "python ../complete_degrees_ML.py ib ./similarity_" + name_test
        sfarg = "../socialfiltering -u 6041 -i 3953 -r ratings_train.dat -t target_users.dat -l ratings_test_input.dat -g similarity_" + name_test + "_complete -k 10 -b 1 -a weighted_" + name_test + " > ./avg_" + name_test
        if methodName[2] == 'cos':
            simarg = "../sim-cosine -i 6041 -u 3953 -r ratings_train_iuv.dat -t ratings_train_iuv.dat > ./similarity_" + name_test
        elif methodName[2] == 'jaccard':
            simarg = "../sim-jaccard -i 6041 -u 3953 -r ratings_train_iuv.dat -t ratings_train_iuv.dat > ./similarity_" + name_test
        elif methodName[2] == 'q1a0':
            simarg = "../sim-cosine -i 6041 -u 3953 -r ratings_train_iuv.dat -t ratings_train_iuv.dat -q 1 -a 0 > ./similarity_" + name_test
        elif methodName[2] == 'q1a0.5':
            simarg = "../sim-cosine -i 6041 -u 3953 -r ratings_train_iuv.dat -t ratings_train_iuv.dat -q 1 -a 0.5 > ./similarity_" + name_test
        elif methodName[2] == 'q5a0':
            simarg = "../sim-cosine -i 6041 -u 3953 -r ratings_train_iuv.dat -t ratings_train_iuv.dat -q 5 -a 0 > ./similarity_" + name_test
        elif methodName[2] == 'q5a0.5':
            simarg = "../sim-cosine -i 6041 -u 3953 -r ratings_train_iuv.dat -t ratings_train_iuv.dat -q 5 -a 0.5 > ./similarity_" + name_test
        elif methodName[2] == 'arule':
            os.system("../apriori-simple.py ratings_train.dat")
            simarg = "sed '/-/d;/inf/d;/^$/d' sim_arule > ./similarity_" + name_test
    os.system(simarg)
    os.system(degreearg)
    os.system(sfarg)
    if methodName[0] == 'recavg':
        filepath = "./avg_" + name_test
    elif methodName[0] == 'recweighted':
        filepath = "./weighted_" + name_test
    applist = pd.read_csv(filepath, delimiter=' ', names=['user', 'item', 'score'])
    drec = {k: g["item"].tolist() for k, g in applist.groupby("user")}
    compare(methodNames, drec, deva, target_user, i, resultBestSet)
    # Normalization
    applist['score'] = (applist['score'] - applist['score'].min()) / (applist['score'].max() - applist['score'].min())
    finalSets.append(applist)
print >> outfile, resultBestSet
print now(), "Phase 2 - run 5 best RS's on test set done."
# Merge the best 2 RS's with Power Means
set1 = bestSet.iloc[0]
set2 = bestSet.iloc[1]
set1List = finalSets[0]
set2List = finalSets[1]

for K in np.arange(21):
    alpha = K / 20.0
    f = StringIO.StringIO()
    r = StringIO.StringIO()
    resultSet = dict()
    resultSetR = dict()
    for user in target_user:
        resultSet[user] = dict()
        resultSetR[user] = dict()
        itemlist1 = set1List[set1List['user'] == user]
        itemlist2 = set2List[set2List['user'] == user]
        for item in itemlist1['item']:
            resultSet[user][item] = alpha * itemlist1[itemlist1['item'] == item]['score'].iloc[0]
            resultSetR[user][item] = alpha * pow(itemlist1[itemlist1['item'] == item]['score'].iloc[0], 5)
        for item in itemlist2['item']:
            if resultSet[user].has_key(item):
                resultSet[user][item] += (1 - alpha) * itemlist2[itemlist2['item'] == item]['score'].iloc[0]
                resultSetR[user][item] += (1 - alpha) * pow(itemlist2[itemlist2['item'] == item]['score'].iloc[0], 5)
            else:
                resultSet[user][item] = (1 - alpha) * itemlist2[itemlist2['item'] == item]['score'].iloc[0]
                resultSetR[user][item] = (1 - alpha) * pow(itemlist2[itemlist2['item'] == item]['score'].iloc[0], 5)
        for item in resultSetR[user]:
            resultSetR[user][item] = pow(resultSetR[user][item], 0.2)
        resultSet[user] = sorted(resultSet[user].iteritems(), key=lambda d: d[1], reverse=True)
        resultSetR[user] = sorted(resultSetR[user].iteritems(), key=lambda d: d[1], reverse=True)
        if len(resultSet[user]) >= 10:
            range_count = 10
        else:
            range_count = len(resultSet[user])
        for i in np.arange(range_count):
            (item, count) = resultSet[user][i]
            print >> f, str(user) + ' ' + str(item) + ' ' + str(count)
            (item, count) = resultSetR[user][i]
            print >> r, str(user) + ' ' + str(item) + ' ' + str(count)
    f.seek(0)
    r.seek(0)
    rec = pd.read_csv(f, sep=' ', header=None, names=['u', 'v', 'w'])
    recR = pd.read_csv(r, sep=' ', header=None, names=['u', 'v', 'w'])
    drec = {k: g["v"].tolist() for k, g in rec.groupby("u")}
    drecR = {k: g["v"].tolist() for k, g in recR.groupby("u")}
    compare(alpha, drec, deva, target_user, K, resultAlpha)
    compare(alpha, drecR, deva, target_user, K, resultR)
    f.close()
    r.close()
#fig = plt.figure()
#ax = plt.axes()
#ax.plot(resultAlpha['Alpha'], resultAlpha['Precision'], '-b', label='Precision r=1')
#ax.plot(resultR['Alpha'], resultR['Precision'], '-g', label='Precision r=5')
#ax.legend(loc=2)
#title = 'Power Means on ' + set1 + '/' + set2
#ax.set_title(title)
#ax.set_xlabel('Alpha')
#plt.savefig("figure.png", format='png')
print >> outfile, resultAlpha
print >> outfile, resultR
print now(), "Phase 2 - Merge the best 2 RS's with Power Means done."
# final merging methods
resultMerge = pd.DataFrame(columns=['Method', 'Precision', 'Recall', 'User Coverage'])

methodSet = ['min', 'max', 'sum', 'med', 'anz', 'mnz', 'rlsim', 'pv', 'borda', 'rrf5']
f = dict()
resultSet = dict()
for method in methodSet:
    f.update({method: StringIO.StringIO()})
    resultSet.update({method: dict()})

for user in users:
    for key in resultSet: # initialize each dicts per user
        resultSet[key][user] = dict()
    for result in finalSets:
        templist = result[result['user'] == user]
        items = templist['item']
        bordaScore = len(items)
        rank = 0
        for item in items:
            bordaScore -= 1
            rank += 1
            itemscore = templist[templist['item'] == item]['score'].iloc[0]
            if not resultSet['sum'][user].has_key(item):
                resultSet['pv'][user][item] = 1
                resultSet['sum'][user][item] = itemscore
                resultSet['rlsim'][user][item] = itemscore
                resultSet['max'][user][item] = itemscore
                resultSet['min'][user][item] = itemscore
                resultSet['borda'][user][item] = bordaScore
                resultSet['rrf5'][user][item] = 1.0 / (5 + rank)
            else:
                if itemscore > resultSet['max'][user][item]:
                    resultSet['max'][user][item] = itemscore
                if itemscore < resultSet['min'][user][item]:
                    resultSet['min'][user][item] = itemscore
                resultSet['pv'][user][item] += 1
                resultSet['sum'][user][item] += itemscore
                resultSet['rlsim'][user][item] *= itemscore
                resultSet['borda'][user][item] += bordaScore
                resultSet['rrf5'][user][item] += 1.0 / (5 + rank)
    # CombMED, CombANZ, CombMNZ
    for key, value in resultSet['sum'][user].iteritems():
        resultSet['med'][user][key] = value / numlist
        resultSet['anz'][user][key] = value / resultSet['pv'][user][key]
        resultSet['mnz'][user][key] = value * resultSet['pv'][user][key]
    for key in resultSet:
        resultSet[key][user] = sorted(resultSet[key][user].iteritems(), key=lambda d: d[1], reverse=True)
        if len(resultSet[key][user]) >= 10:
            range_count = 10
        else:
            range_count = len(resultSet[key][user])
        for i in np.arange(range_count):
            (item, count) = resultSet[key][user][i]
            print >> f[key], str(user) + ' ' + str(item) + ' ' + str(count)
count = 0
for key in f:
    f[key].seek(0)
    rec = pd.read_csv(f[key], sep=' ', header=None, names=['u', 'v', 'w'])
    drec = {k: g["v"].tolist() for k, g in rec.groupby("u")}
    compare(key, drec, deva, target_user, count, resultMerge)
    count += 1
    f[key].close()
print >> outfile, resultMerge
print now(), "Phase 2 - Merge methods done."
outfile.close()
