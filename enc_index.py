# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 18:17:11 2020

@author: Fajia Sun
"""

import re

#additional operations are required here
#due to inconsistency in base conversion during encoding
def basecon(txt):
    split=re.findall(r'.{2}', txt)
    basecode=''
    n=0
    for i in split:
        if i == '00':
            i='A'
        if i == '01':
            i='C'
        if i == '10':
            i='G'
        if i == '11':
            i='T'
        basecode=(basecode+i)
        n=n+1
    return basecode

def transcon(txt):
    b=list(txt)
    for j in range(4):
        if b[j] == 'A':
            b[j]=0
        if b[j] == 'T':
            b[j]=1
        if b[j] == 'C':
            b[j]=2
        if b[j] == 'G':
            b[j]=3
    n=pow(4,0)*b[-1]+pow(4,1)*b[-2]+pow(4,2)*b[-3]+pow(4,3)*b[-4]
    return n

def enc(lenc): #len(lenc)=160
    #number to base
    transbase=[]
    for j in lenc:
        a=str(bin(j))
        b=list(a)
        c=b[2:]
        while len(c) < 8:
            c.insert(0,'0')
        d=''.join(c)
        transbase.append(basecon(d))
    #base to number
    repsymreal=[]
    for i in transbase:
        repsymreal.append(transcon(i))
    return repsymreal
    
#index
def index(li): #len(li)=16
    lindex=[]
    for i in li:
        for j in range(10):
            lindex.append((i-1)*10+j+1)
    return lindex

def main():
    #convert encoding symbols
    with open('encsym.txt','r') as f:
        lt=f.readlines()
        for i in range(len(lt)):
            lt[i]=lt[i].split(' ')
            lt[i].remove('\n')
            for j in range(len(lt[i])):
                lt[i][j]=eval(lt[i][j])
                
        lrepsym=[]
        for i in range(len(lt)):
            lrepsym.append(enc(lt[i]))
    
    '''with open('encsymreal.txt','w') as f2:
        for i in range(len(lt)):
            le=enc(lt[i])
            for j in range(len(le)):
                f2.write(str(le[j]))
                f2.write(' ')
            f2.write('\n')'''
            
    #convert indices
    with open('index.txt','r') as f3:
        li=f3.readlines()
        for i in range(len(li)):
            li[i]=li[i].split(' ')
            li[i].remove('\n')
            for j in range(len(li[i])):
                li[i][j]=eval(li[i][j])
                
        lindex=[]
        for i in range(len(li)):
            lindex.append(index(li[i]))
    
    '''with open('indexreal.txt','w') as f4:
        for i in range(len(li)):
            ld=index(li[i])
            for j in range(len(ld)):
                f4.write(str(ld[j]))
                f4.write(' ')
            f4.write('\n')'''
    
    #the first DNA symbol in each encoding group        
    lreserve=['149', '119', '191', '130', '152', '139', '242', '77', '39', '197', '60', '60', '67', '94', '62', '176', '42', '216', '218', '72', '202', '244', '30', '157', '188', '68', '120', '168', '47', '230', '205', '151', '128', '4', '105', '217', '107', '178']
    
    with open('rqdec.txt','w') as fn:
        for i in range(len(lindex)):
            if min(lindex[i]) > 160:
                #ReceivedSymbols
                fn.write(str(lreserve[i]))
                fn.write('\n')
                #lossidxK
                for p in range(2,161):
                    fn.write(str(p))
                    fn.write(' ')
                fn.write('\n')
                #RepairSymbolsReal
                for q in lrepsym[i]:
                    fn.write(str(q))
                    fn.write(' ')
                fn.write('\n')       
                #repairIdx
                for m in lindex[i]:
                    fn.write(str(m))
                    fn.write(' ')
                fn.write('\n')       
            if min(lindex[i]) <= 160:
                #ReceivedSymbols
                l160=[0]*160
                for j in range(len(lindex[i])): 
                    if lindex[i][j] <= 160:
                        l160[lindex[i][j]-1]=lrepsym[i][j]
                for q in l160:         
                    fn.write(str(q))
                    fn.write(' ')
                fn.write('\n')
                #lossidxK
                for j in range(1,161):
                    if j not in lindex[i]:
                        fn.write(str(j))
                        fn.write(' ')
                fn.write('\n')
                #RepairSymbolsReal
                for j in range(len(lindex[i])):
                    if lindex[i][j] > 160:
                        fn.write(str(lrepsym[i][j]))
                        fn.write(' ')
                fn.write('\n')
                #repairIdx
                for j in range(len(lindex[i])):
                    if lindex[i][j] > 160:
                        fn.write(str(lindex[i][j]))
                        fn.write(' ')
                fn.write('\n') 
            
main()