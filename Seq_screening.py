# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 17:20:10 2020

@author: Fajia Sun
"""

import numpy as np
import re
import screener

def basecon(txt):
    split=re.findall(r'.{2}', txt)
    basecode=''
    n=0
    for i in split:
        if i == '00':
            i='A'
        if i == '01':
            i='T'
        if i == '10':
            i='C'
        if i == '11':
            i='G'
        basecode=(basecode+i)
        n=n+1
    return basecode

def infcon(infsym):
    #n DNA symbols were put in 1 encoding set
    n=10
    while len(infsym)%n != 0:
        infsym.append(100)
    numofg=int(len(infsym)/n)
    codeseq=[]
    infindex=0
    for i in range(numofg):
        infindex += 1
        binary=[]
        issplit=infsym[(i*n):((i+1)*n)]
        for j in issplit:
            a=str(bin(j))
            b=list(a)
            c=b[2:]
            while len(c) < 8:
                c.insert(0,'0')
            #add leading base ('00'=='A')
            c.insert(0,'0')
            c.insert(0,'0')
            d=''.join(c)
            binary.append(d)
        seq2=''.join(binary)
        baseseq=basecon(seq2)
        if screener.screening5(baseseq):
            codeseq.append([baseseq,infindex])
    return codeseq

def repcon(repsym):
    #n shoule be identical to the above setting
    n=10
    while len(repsym)%n != 0:
        repsym.append(100)
    numofr=int(len(repsym)/n)
    recseq=[]
    repindex=0
    for i in range(numofr):
        repindex += 1
        binary=[]
        repsplit=repsym[(i*10):((i+1)*10)]
        for j in repsplit:
            a=str(bin(j))
            b=list(a)
            c=b[2:]
            while len(c) < 8:
                c.insert(0,'0')
           #add leading base ('00'=='A')
            c.insert(0,'0')
            c.insert(0,'0')
            d=''.join(c)
            binary.append(d)
        seq2=''.join(binary)
        baseseq=basecon(seq2)
        #print(screening(baseseq))
        if screener.screening5(baseseq):
            recseq.append([baseseq,repindex])
    return recseq

def main():
    #screening secondary repair symbols
    linfbase=[]
    
    with open('inf_pri.txt','r') as p:
        lp=p.read().split('\n')
        lp=lp[:38]
        for i in range(len(lp)):
            lp[i]=lp[i].split(' ')
            lp[i]=lp[i][:160]
        
    for p in range(len(lp)):
        for q in range(len(lp[p])):
            lp[p][q]=eval(lp[p][q])
        
    for i in range(len(lp)):
        numbers=lp[i]
        bases=infcon(numbers)
        linfbase.append(bases)
    
    lrepbase=[]
        
    with open('sRepSym.txt','r') as f:
        lt=f.readlines()
        lt=lt[:38]
        
    for i in range(len(lt)):
        numbers=str(lt[i]).split(' ')
        numbers=numbers[:63840]
        for j in range(len(numbers)):
            numbers[j]=eval(numbers[j])
        bases=repcon(numbers)
        lrepbase.append(bases)
    
    #record the screened bases
    final=open('screenedbase.txt','w')
    
    for i in range(len(linfbase)):
        final.write(linfbase[i])
        final.write('\n')
        final.write(lrepbase[i])
        final.write('\n')
    #note that an extra \n was added at the end of the file
    
    final.close()
    
main()