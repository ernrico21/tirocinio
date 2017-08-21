from sympy.logic.boolalg import to_cnf

def changeFormula(s,symbol):
    i=0
    j=0
    add=0
    openb=-1
    leng=len(s)
    res=''
    d={}
    op=0
    while i<leng:
        if s[i:i+3]=='And':
            op=1
            i+=3
        elif s[i:i+2]=='Or':
            op=1
            i+=2
        elif s[i:i+3]=='Not':
            op=1
            i+=3
        if s[i]=='(':
            if op==1:
                op=0
            else:
                openb=i
        if s[i]==')':
            if openb != -1:
                res=res+s[add:openb]+symbol+str(j)
                d.update({symbol+str(j):s[openb:i+1]})
                j+=1
                add=i+1
                openb=-1                
        i+=1
    res=res+s[add:]
    return (res,d,j)

def findSymbol(f):
    newsy='new'
    while 1:
        if newsy not in f:
            break
        newsy=newsy[0:-1]+'ew'
    return newsy
        
def buildSet(Kb,Dt):
    Sym=[]
    j=0
    find=True
    for i in range (0,len(Dt)):
        while find:
            find=False
            for k in range(0,len(Kb)):
                if 'Sym'+str(j) in Kb:
                    find=True
            j+=1
        name='Sym'+str(j)            
        symbol=findSymbol(Dt[i])
        resset = changeFormula(Dt[i],symbol)
        formula='Or(And('+name+','+resset[0]+'),And(Not('+name+'),Not('+resset[0]+')))'
        cnfstr =str(to_cnf(formula))

        for i in range(0,resset[2]):
            cnfstr=str.replace(cnfstr,symbol+str(i),resset[1][symbol+str(i)])

        Sym.append(cnfstr)

    KB_ext=[]
    for i in range (0,len(Kb)):
        symbol=findSymbol(Kb[i])
        resset=changeFormula(Kb[i],symbol)
        cnfstr=str(to_cnf(resset[0]))
        for j in range(0,resset[2]):
            cnfstr=str.replace(cnfstr,symbol+str(j),resset[1][symbol+str(j)])
        Kb[i]=cnfstr
    KB_ext.extend(Kb)
    KB_ext.extend(Sym)
    return KB_ext




f1='Or(And(A(x),B(x)),Not(And(E(x,y),G(k,z))))'
f2='And(A(x),B(x))'
f3='Or(A(x),C(x))'

p1='Or(Not(And(C(x,y),D(x,y))),And(E(x,y),F(x,y)))'
p2='And(C(x),D(x))'
p3='Or(D(x),E(x))'

Kb=[f1,f2,f3]
Dt=[p1,p2,p3]

print (buildSet(Kb,Dt))

