import buildset as bs
from numpy import save, load  
'''
g='Equivalent(F(c, c), Implies(Phi1(c, c),Equivalent(Phi2(h, j),var3(x,y),var(u,l))))'
print bs.buildJustFormula(g)
'''
f_GKB ='GKB.dat'  
f= open(f_GKB, 'rb')
GKB = set(load(f))
formulas=[]
for x in GKB:
    formulas.append(bs.buildJustFormula(x))    
f.close()
for s in formulas:
    print s


#'''


