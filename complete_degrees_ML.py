#!/bin/python
import pandas as pd
import sys

recType = sys.argv[1]
simPath = sys.argv[2]
outFile = simPath + '_complete'
sim = pd.read_csv(simPath, delimiter=" ", names=['user1', 'user2', 'similarity'])
# max_user1 = sim['user1'].max()
# max_user2 = sim['user2'].max()
# max_num_user = max_user1 if max_user1 > max_user2 else max_user2
# total = max_num_user + 1
if recType == 'ub':
    total = 6041
elif recType == 'ib':
    total = 3953
else:
    exit()
degrees = sim['user1'].value_counts().sort_index(0)
dict_degrees = degrees.to_dict()
for i in xrange(total):
    if not dict_degrees.has_key(i):
        dict_degrees[i] = 0
f = open(outFile, "w")
sim_input = open(simPath)
print >> f, total
for key, value in dict_degrees.iteritems():
    print >> f, str(key) + ' ' + str(value)
print >> f, (sim_input.read()).strip()
f.close()
sim_input.close()
