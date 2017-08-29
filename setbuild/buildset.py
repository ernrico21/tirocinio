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
        elif s[i:i+10]=='Equivalent':
            op=1
            i+=10
        elif s[i:i+7]=='Implies':
            op=1
            i+=7
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
        

def ResolveEqImp(st):
    s=str.replace(st,' ','')
    prova=s
    i=0
    op='N'
    elemntpoint=0
    parentesyscount=0
    elements=[]
    init=0
    par=1;
    while i<len(s):  
        if s[i:i+10]=='Equivalent':
            if op=='N':
                op='E'
                init=i
                elemntpoint=i+11
            i+=10
            parentesyscount+=1
        elif s[i:i+7]=='Implies':
            if op=='N':
                op='I'
                init=i
                elemntpoint=i+8
            i+=7
            parentesyscount+=1
        elif s[i]=='(':
            if op != 'N': 
                parentesyscount+=1
        elif s[i]==',':
            if parentesyscount==1 and op != 'N' :
                elements.append(s[elemntpoint:i])
                elemntpoint=i+1
        elif s[i]==')':
            if op != 'N':                
                parentesyscount-=1
            if parentesyscount==0 and op != 'N':
                tempformula=''
                newstr=''
                elements.append(s[elemntpoint:i])  
                if op== 'E':
                    if len(elements)!=2:
                        j=1                    
                        newelem=''
                        while j < len(elements)-1:
                            newelem=newelem+'Equivalent('+elements[j]+','
                            j+=1
                        newelem=newelem+elements[j]
                        while j>1:
                            newelem+=')'
                            j-=1
                        elements[1]=newelem
                    newstr='And(Or('+elements[0]+',Not('+elements[1]+')),Or(Not('+elements[0]+'),'+elements[1]+'))'
                    if init!=0:
                        tempformula=s[0:init]
                    tempformula+=newstr
                    if i!= len(s)-1:
                        tempformula+=s[i+1:]                    
                    elements=[]
                    s=tempformula
                    op='N'
                    i=init+6
                if op== 'I':
                    if len(elements)!=2:
                        j=1                    
                        newelem=''
                        while j < len(elements)-1:
                            newelem=newelem+'Implies('+elements[j]+','
                            j+=1
                        newelem=newelem+elements[j]
                        while j>1:
                            newelem+=')'
                            j-=1
                        elements[1]=newelem
                    newstr='Or(Not('+elements[0]+'),'+elements[1]+')'
                    if init!=0:
                        tempformula=s[0:init]
                    tempformula+=newstr
                    if i!= len(s)-1:
                        tempformula+=s[i+1:]                    
                    elements=[]
                    s=tempformula
                    op='N'
                    i=init+6
        #print s[0:i+1]
        #print parentesyscount
        i+=1  
    return s


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
        #newformula= ResolveEqImp(resset[0])
        #formula='And(Or('+name+',Not('+newformula+')),Or(Not('+name+'),'+newformula+'))'
        formula='And(Or('+name+',Not('+resset[0]+')),Or(Not('+name+'),'+resset[0]+'))'
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


def buildJustFormula (f):
    symbol=findSymbol(f)
    resset = changeFormula(f,symbol)
    newformula= ResolveEqImp(resset[0])
    cnfstr =str(to_cnf(newformula))
    for i in range(0,resset[2]):
        cnfstr=str.replace(cnfstr,symbol+str(i),resset[1][symbol+str(i)])
    return cnfstr




'''

f1='Or(And(A(x),B(x)),Not(And(E(x,y),G(k,z))))'
f2='And(A(x),B(x))'
f3='Or(A(x),C(x))'

p1='Or(Not(And(C(x,y),D(x,y))),And(E(x,y),F(x,y)))'
p2='And(C(x),D(x))'
p3='Or(D(x),E(x))'

Kb=[f1,f2,f3]
Dt=[p1,p2,p3]
'''
#print (buildSet(Kb,Dt))

