cimport allsat
import time
from cpython.mem cimport PyMem_Free

cdef solve (char * dim, int nvar):
    start=time.time()
    cdef allsat.list* sol=allsat.main(dim)
    end=time.time()
    #print ("time allsat: "+str(end-start))
    nsol = 0
    matrix=[]
    while sol.next:    
        sol=sol.next
        matrix.append([])
        for i in range(0,nvar):
            matrix[nsol].append(sol.value[i])
        PyMem_Free(sol.value)
        nsol+=1
    matrix.pop(-1)
    return matrix

def solver (dimacs,nvar):
    return solve (dimacs, nvar)

