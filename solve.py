import time
import subprocess
import sys
import numpy
import os
import allsat

'''
find if there is the keyword And
'''
def findAnd(c,i):
    if (c[i+1]=='n'or c[i+1]=='N') and (c[i+2]=='d' or c[i+2]=='D'):
        return 1
    else:
        return -1


'''
find if there is the keyword Or
'''
def findOr(c,i):
    if c[i+1]=='r' or c[i+1]=='R':
        return 1
    else:
        return -1


'''
find if there is the keyword Not
'''
def findNot(c,i):
    if (c[i+1]=='o'or c[i+1]=='O') and (c[i+2]=='t'or c[i+1]=='T'):
        return 1
    else:
        return -1

'''
add variable to the dimacs formula
'''
def addvariable (lVal):
    if len(lVal[1])!=0:         
#       if lVal[1][0]=='-':
#           lVal[1]=lVal[1][1:len(lVal[1])]
#           lVal[5]=1    
        if lVal[1] not in lVal[3]:
            lVal[3].update({lVal[1]:lVal[2]})
            lVal[4].update({lVal[2]:lVal[1]})
            lVal[1]=str(lVal[2])
            lVal[6]+=1
            lVal[2]+=1                        
        else:
            lVal[1]=str(lVal[3][lVal[1]])
#           if lVal[5] ==1:
#               lVal[1]='-'+lVal[1]    
#               lVal[5]-=1
        if lVal[5] > 0:
            if lVal[5] % 2 == 1:
                lVal[1]='-'+lVal[1]
                lVal[5]=0
    
        lVal[0]+=(lVal[1]+' ')
        lVal[1]=''
    return (lVal)


'''
////////////////////////////////////////////////////////////////////////////
what is done in  addvariable with variables

if len(variable)!=0:         
#                    if variable[0]=='-':
#                        variable=variable[1:len(variable)]
#                        minus=1    
                        if variable not in variables:
                            variables.update({variable:indexvariable})
                            inv_variables.update({indexvariable:variable})
                            variable=str(indexvariable)
                            nVar+=1
                            indexvariable+=1                        
                        else:
                            variable=str(variables[variable])
#                       if minus ==1:
#                            variable='-'+variable    
#                            minus-=1
                        if minus > 0:
                            if minus % 2 == 1:
                                variable='-'+variable
                            minus=0
    
                        cnfstring+=(variable+' ')
                        variable=''

////////////////////////////////////////////////////////////////////////////////
'''


'''
build the dimacs formula from a And(OR(....)) one
'''
def buildDimacsString(c):
    cnfstring='';
    variables={}
    inv_variables={}
    nVar=0
    nRow=0 #number of clauses
    buff=[]; #for buffering the letter of the variables
    i=0 #iterator of the formula
    #i2=0
    j=-1 #to chek if i found a key word
    leng=len(c)
    operations=[] #operation's stack
    variable='';
    indexvariable=1 #index for variables
    minus=0 #when writing variabile if is negated
    popped_and=0 #if i justo sow ) and poped And out of the stack, if i see "," and there is And as head of the stack i have not to write dow anything
    operationpar=0 #too see if i'm a variable name or is operation parentesys
    varparentesys=0 #same as above
    lVal=[cnfstring,variable,indexvariable,variables,inv_variables,minus,nVar]
    
    while i<leng:
        operations
        j=-1
        if c[i]=='A':
            j=findAnd(c,i)
            if j!=-1 :
                operations.append('And')   #put the operations in the stack 
                operationpar=1
                i=i+2        
        elif c[i] == 'O':
            j=findOr(c,i)
            if j!=-1:
                operations.append('Or')      
                operationpar=1
                i=i+2             
        elif c[i] == 'N':        
            j= findNot(c,i)
            if j!=-1:
                operations.append('Not')      
                operationpar=1
                i=i+2                
        elif c[i] == ',':      
            if varparentesys==0 :          
                if len(buff) != 0:
                    k=0
                    lengbuff=len(buff)        
                    while k<lengbuff :
                        lVal[1] += buff.pop(0)          #when "," means that if i was reading a variable the variable is finished so i pop it off the buff
                        k+=1
                if operations[-1] == 'Or':               #if "or" i just add the variable
                    lVal=addvariable(lVal)
                    popped_and=0
                elif operations[-1] == 'And':   #"and"means that this clause is finished so i start another one
                    if popped_and==0:
                        lVal=addvariable(lVal)
                        lVal[0]+='0\n'
                        nRow+=1 
                    else:
                        popped_and=0
            else:
                buff.append(c[i])

        elif c[i] == ')':       #when i see ')' means an operation is finished, so after doing the opesations i pop the operations off the stack
            if varparentesys == 0:
                if len(buff) != 0:     #same as the "," for the variables
                    k=0
                    lengbuff=len(buff)
                    while k<lengbuff :
                        lVal[1] += buff.pop(0)
                        k+=1
                if operations[-1] == 'Not' :  #set the controller to 1 for the not
    #                variable='-'+variable
                    lVal[5]+=1
                    popped_and=0
                    operations.pop()
                elif operations[-1] == 'Or' : 
                    lVal=addvariable(lVal)
                    operations.pop()
                    popped_and=0

                elif operations[-1]== 'And' :
                    lVal=addvariable(lVal)
                    lVal[0]+='0\n'
                    nRow+=1
                    popped_and=1                
                    operations.pop() 
            else:
                buff.append(c[i])
                varparentesys=0
        elif c[i]=='(':
            if operationpar==0:
                buff.append(c[i])
                varparentesys=1
        else:
            if j== -1 and c[i]!=' ':              #put the char in the buff for creating the variable name
                buff.append(c[i])
                popped_and=0
                operationpar=0
        i+=1  
    return (lVal[0],lVal[6],nRow,lVal[4],lVal[3])

        


'''
metod for getting the And(Or(..)) formula from a dimacs
'''
def buildFormula(s):
    rs=s[0].split()
    nvar=int(rs[2])
    nclause=int(rs[3])
    res='And('
    i=1
    k=1
    while k< (nclause+1):
        ri=s[i].split()
        if ri[0]!='0':
            temp="Or("
            for j in range (0,len(ri)):
                if(int(ri[j])<0):
                    temp=temp+'Not('+str(abs(int(ri[j])))+'),'
                elif ri[j]!='0':
                    temp=temp+ri[j]+','
            temp=temp[0:-1]+'),'
            res=res+temp
            k+=1
        i+=1
    res=res[0:-1]+')'
    return res



'''
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
Return the result matrix and the dictionary that give the index if a variable
Printing the matrix with numpy call getSolutions with 2nd parameter =1
Printing time stats in fie 3rd parameter =1 if 4th parameter not specified filename=outputfile
Printing time stats in shell 3rd parameter =2
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
'''


def getSolutions(s,smatrix=0,stat=0,name="outputfile"):
    print name
    start=time.time()
    res=()
    res = buildDimacsString(s)  
    #getting results from bdd_allsat
    start=time.time()
    matrix=allsat.solver('p cnf '+str(res[1])+' '+str(res[2])+'\n'+res[0],res[1])
    end=time.time()
    if smatrix==1:
        numpy.set_printoptions(threshold=numpy.nan)
        print(numpy.matrix(matrix))
    if stat==1:
        f2=open('all100b','a')
        f2.write(name+"\n")
        f2.write("number of variables: "+str(res[1])+"\n")
        f2.write("number of solutions: "+str(len(matrix))+"\n")
        f2.write("time allsat to find the solutions: "+str(end-start)+"\n")
        f2.write("total time: "+str(end-start)+"\n\n")    
        f2.close()
    elif stat ==2:
        print("number of variables: "+str(res[1]))
        print("number of solutions: "+str(len(matrix)))
        print("time: "+str(end-start))  
    matrix= None
    res= None    
    return (matrix,res[3]) 
#'''
s1='And(Or(Not(var1(x,y)), var2(x,y), Not(Not(Not(var3(x,y)))), Not(Not(var4(x,y)))), Or(Not(var2(x,y)), var1(x,y), var3(x,y),var5(x,y)))And(Or(var1(x,y), var2(x,y), var4(x,y)))'
s2='And(Or(Not(var1), var2, Not(Not(Not(var3))), Not(Not(var4))), Or(Not(var2), var1, var3,var5), Or(var1, var2, var4))'
s3='And(And(Or(Not(var1),Or(var2,Or(Not(Not(Not(var3))), Not(Not(var4))))),Or(Not(var2),Or(var1,Or(var3,var5)))),Or(var1, Or(var2, var4)))'
s3='And(And(And(Or(1,Not(2)),3),4),5)'

dims1=buildDimacsString(s1)
print dims1
print buildDimacsString(s2)
#dims3=buildDimacsString(s3)

#print dims1[0]
#print dims2[0]
#print dims3[0]
'''
da=901
cwd = os.getcwd()
direc=cwd+'/cnf100/'
for j in range (da,da+100):
    if j != 6 and j != 70 and j != 136 and j != 342 and j != 516 and j != 704 and j != 717 and j != 766 and j != 776 and j != 793 and j != 834 and j != 836 and j != 837 and j != 936:
        namefile="uf100-0"+str(j)+".cnf"
        f=open(direc+namefile,"r")
        sf=f.readlines()
        i=0
        while i>=0:
            if sf[0][0]=='c':
                sf.pop(0)
                i=1
            else:
                i=-1
        s=buildFormula(sf)
        getSolutions(s,0,1,namefile)
'''

 
