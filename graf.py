import matplotlib.pyplot as plt
import numpy as np
X = []
Y = []
Y2 = []
X2 = []
f=open('all150','r')
split=f.read().split('\n')
i=1
j=0
while i<len(split)-2:
    #print i
    #j+=1
    nv=float(split[i].split()[3])
    i+=1
    ns=float(split[i].split()[3])
    X.append(ns)
    i+=1
    ta=float(split[i].split()[6])
    Y.append(ta)
    i+=1
    tt=float(split[i].split()[2])
    i+=3
    if tt > 0:
        X2.append(ns*nv)
        Y2.append(tt-ta)

plt.vlines(X,[0],Y,label='time')
plt.legend()
plt.ylabel('time')
plt.xlabel('number of solutions')
plt.show()
