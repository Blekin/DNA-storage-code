# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 19:55:51 2020

@author: Fajia Sun
"""

import numpy as np
import os
from reedsolo import RSCodec
import re

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

def main():
    #here 330 RS check symbols were generated based on the whole information,
    #which served as primary repair symbols
    rsc = RSCodec(330, c_exp=12)
    
    #GF(2^12) was used here, which was determined by the amount of data
    
    #enter binary stream
    name=input("Please enter the name of file containing binary sequence:")
    with open(name,'r') as f:
        bi=f.read()
    
    lt=list(bi)
    #length=44506
    
    while len(lt)%12 != 0:
        lt.append('0')
    bi11=''.join(lt)
    #2 '0' was added at the end
    
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
    #print(sym4095[0],sym4095[3700])
    
    #generating RS check symbols
    a=rsc.encode(sym4095)
    
    b=list(a)
    
    print(len(b))
    print(b[0],b[3700])
    
    #check if systematic code
    for i in range(3709):
        if sym4095[i] != b[i]:
            print("No systematic code!")
    #the length of codeword cannot exceed the number of elements in GF
    
    rscode=b[3709:] #the primary redundancy, 330 4096-ray numbers
    
    #convert to binary stream, which was added after the information stream
    #next step is grouping and sent to RaptorQ encoder to generate secondary repair symbols
    lrs=[]
    for i in range(len(rscode)):
        lzancun=[]
        twelve=conver(rscode[i])
        for j in twelve:
            lzancun.append(j)
        while len(lzancun) < 12:
            lzancun.insert(0,'0')
        tzancun=''.join(lzancun)
        lrs.append(tzancun)
    rsbinary=''.join(lrs)
    
    #transform information stream and primary repair symbols to base-256 numbers
    
    nb=8
    
    lti=list(bi)
    while len(lti)%nb != 0:
        lti.append('0')
    
    lr=bito256(lti)
    
    print(len(lr)) #5564
    
    #each encoding group contains 160 symbols
    nofs=160
    nofg_enc=int(np.ceil(len(lr)/nofs))
    
    while len(lr) < nofs*nofg_enc:
        lr.append(100)
    
    
    nofg_pri=3
    lrs256=bito256(rsbinary)
    
    with open('inf_pri.txt','w') as f2:
        #write information symbols
        for p in range(nofg_enc):
            for q in range(nofs):
                f2.write(str(lr[p*160+q]))
                f2.write(' ')
            f2.write('\n')
        for p in range(nofg_pri-1):
            for q in range(nofs):
                f2.write(str(lrs256[p*160+q]))
                f2.write(' ')
            f2.write('\n')       
        for p in range(nofg_pri-1,nofg_pri):
            for q in range(nofs):
                f2.write(str(lrs256[p*160+q]))
                f2.write(' ')

main()