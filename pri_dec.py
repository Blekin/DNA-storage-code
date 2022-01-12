# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 19:55:51 2020

@author: Fajia Sun
"""

import numpy as np
import os
from reedsolo import RSCodec
import re
import sys

def conver(n):
    if n==0 :
        return '' 
    return conver(n//2)+str(n%2)

def reconver(n):
    ls11=[]
    t=str(n)
    for i in t:
        ls11.append(eval(i))
    while len(ls11) < 12:
        ls11.insert(0,0)
    number=0
    for j in range(12):
        number+=pow(2,j)*ls11[-(j+1)]
    return number

def bito256(infor):
    linfor=list(infor)
    while len(linfor)%8 != 0:
        linfor.append('0')
    l256=[]
    rec=int(len(linfor)/8)
    
    for i in range(rec):
        lsplit=linfor[(8*i):(8*i)+8]
        for j in range(len(lsplit)):
            lsplit[j]=eval(lsplit[j])
        n256=1*lsplit[-1]+2*lsplit[-2]+4*lsplit[-3]+8*lsplit[-4]+16*lsplit[-5]+32*lsplit[-6]+64*lsplit[-7]+128*lsplit[-8]
        l256.append(n256)
    return l256

def r256tobi(lt):
    binary=[]
    for j in lt:
        a=str(bin(j))
        b=list(a)
        c=b[2:]
        while len(c) < 8:
            c.insert(0,'0')
        d=''.join(c)
        binary.append(d)
    return ''.join(binary)

#decoding using primary redundancy is dispensable when all the information
#groups were successfully recovered by RaptorQ decoder
def main():
    lossidx=int(input("Please type in the number of unrecovered encoding groups:"))
    
    if lossidx not in [1,2,3]:
        print('The numbers of unrecovered encoding groups must be 1 or 2 or 3!')
        sys.exit(1)
    
    lidx=[]
    for i in range(lossidx):
        lidx.append(int(input("Please type in the order of unrecovered encoding groups (0-37):")))
    
    for i in lidx:
        if i<0 or i>37:
            print('Wrong order of encoding groups!')
            sys.exit(1)    
    
    #enter the recovered encoding groups
    with open("infsym.txt",'r') as f:
        lbi=[]
        lt=f.readlines()
        for i in range(len(lt)):
            lt[i]=lt[i].split(' ')
            lt[i]=lt[i][:160]
            for p in range(len(lt[i])):
                lt[i][p]=int(lt[i][p])
            
        for j in range(35):
            if j not in lidx:
                lbi.append(r256tobi(lt[j]))
            if j in lidx:
                lbi.append('0'*1280)
        
        lpri=[]
        for q in range(35,38):
            lpri.append(r256tobi(lt[q]))
    
    bitxt=list(''.join(lbi))[:44506]
    pritxt=''.join(lpri)
    
    while len(bitxt)%12 != 0:
        bitxt.append('0')
    bi11=''.join(bitxt)
    
    split=re.findall(r'.{12}', bi11)
    #the stream was separated every 12 bits, resulting in 3709 numbers with a length of 12
    
    sym4095=[]
    for i in range(len(split)):
        str11=split[i]
        ls1=list(str11)
        ls11=[]
        for j in ls1:
            ls11.append(eval(j))
        number=1*ls11[-1]+2*ls11[-2]+4*ls11[-3]+8*ls11[-4]+16*ls11[-5]+32*ls11[-6]+64*ls11[-7]+128*ls11[-8]+256*ls11[-9]+512*ls11[-10]+1024*ls11[-11]+2048*ls11[-12]
        sym4095.append(number)
    
    print(len(sym4095)) #3709
    
    split=re.findall(r'.{12}', pritxt)
    
    pri4095=[]
    for i in range(len(split)):
        str11=split[i]
        ls1=list(str11)
        ls11=[]
        for j in ls1:
            ls11.append(eval(j))
        number=1*ls11[-1]+2*ls11[-2]+4*ls11[-3]+8*ls11[-4]+16*ls11[-5]+32*ls11[-6]+64*ls11[-7]+128*ls11[-8]+256*ls11[-9]+512*ls11[-10]+1024*ls11[-11]+2048*ls11[-12]
        pri4095.append(number)
    
    print(len(pri4095)) #320
    
    last10=[2446, 1936, 1705, 2704, 3369, 3679, 2257, 2885, 509, 2989]
    
    decall=sym4095+pri4095+last10
    
    #positions of unrecoverable symbols
    eraloc=[]
    for i in lidx:
        for j in range(107):
            eraloc.append(int(np.ceil(i*160*8/12+j)))
        
    rsc = RSCodec(330, c_exp=12)
    rmes, rmesecc, errata_pos = rsc.decode(decall,erase_pos=eraloc)
    
    infsym_real=list(rmes)
    linfreal=[]
    for i in infsym_real:
        txt12=list(conver(i))
        while len(txt12) < 12:
            txt12.insert(0,'0')
        linfreal.append(''.join(txt12))
    bireal=''.join(linfreal)[:44506]
    #now we get the decoding result, which can be transferred to source decoding
    with open('infsym_real.txt','w') as f2:
        f2.write(bireal)
    
main()