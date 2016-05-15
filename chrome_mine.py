
# coding: utf-8

# In[1]:

import git
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt


# In[2]:

#1. Connect to repo and get files&developers
repo = git.Repo() 
devs, files = defaultdict(int), defaultdict(list)
for commit in repo.iter_commits():
    authorName = commit.author.name
    commitedFiles = commit.stats.files.keys()
    for f in commitedFiles:
        files[f].append(authorName)
    devs[authorName] += 1


# In[3]:

#2. Identify top devs and plot commit blocks
def plotDict(d, plotName):
    plt.bar(range(len(d)), d.values(), align='center')
    plt.xticks(range(len(d)), d.keys())
    plt.savefig(plotName)
    plt.close()
#2.a Plot commit distribution
plotDict(devs, 'all-commit')
#2.b Identify top devs&plot top dev distribution
eightyCommit = sum(devs.itervalues())*0.8 # %80 of total commits
sortedDevs, topDevs = sorted(devs.items(), key=lambda x:x[1], reverse = True), defaultdict(int)
for dev in sortedDevs:
    if dev[1] < eightyCommit:
        topDevs[dev[0]] = dev[1]
        eightyCommit -= dev[1]  
plotDict(topDevs, 'top-commit')        


# In[35]:

#3. Build and save the commit matrix
commitMatrix = np.zeros((len(files), len(devs)), dtype=np.int)
commitM = defaultdict(dict)
i, j = 0, 0
for f in files:
    for dev in devs:
        if dev in files[f]:
            commitMatrix[i][j] = 1
            commitM[f][dev] = 1
        j += 1
    j = 0     
    i += 1 
np.savetxt('commitMatrix.adj', commitMatrix, fmt='%i', delimiter=' ')    


# In[34]:

#4.Build and save top devs commit matrix
topCommitM = defaultdict(dict)
for dev in topDevs:
    for f in commitM:
        for dev2 in commitM[f]:
            if dev2 in topDevs and dev in commitM[f] and dev != dev2:
                topCommitM[dev][dev2] = 1
topCommitMatrix = np.zeros((len(topDevs), len(topDevs)), dtype=np.int)
i, j = 0, 0
for dev in topDevs:
    for dev2 in topDevs:
        if topCommitM.get(dev).get(dev2) is not None:
            topCommitMatrix[i][j] = 1
        else:
            topCommitMatrix[i][j] = 0
        j += 1
    j = 0
    i += 1
np.savetxt('topCommitMatrix.adj', topCommitMatrix, fmt='%i', delimiter=' ')           


# In[ ]:



