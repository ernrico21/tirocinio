import buildset as bs
import solve
from numpy import save, load
import numpy
'''
g='Equivalent(F(c, c), Implies(Phi1(c, c),Equivalent(Phi2(h, j),var3(x,y),var(u,l))))'
print bs.buildJustFormula(g)
'''
f_GKB ='GKB.dat'  
f= open(f_GKB, 'rb')
GKB = set(load(f))
formulas=[]
numpy.set_printoptions(threshold=numpy.nan)
for x in GKB:
    print x
    formula=(bs.buildJustFormula(x)) 
    resset=solve.getSolutions(formula)
    print(numpy.matrix(resset[0]))
    print resset[1] 
    print resset[2]   
    print '...............................................................................................................'
f.close()



#'''


