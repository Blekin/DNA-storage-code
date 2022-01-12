# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 18:17:11 2020

@author: Fajia Sun
"""
import re

#len=160

l00=[23, 181, 94, 27, 38, 38, 236, 59, 4, 30, 246, 16, 26, 41, 89, 44, 163, 253, 222, 111, 219, 246, 93, 237, 217, 158, 57, 100, 14, 240, 188, 206, 24, 90, 81, 144, 218, 67, 107, 116, 62, 119, 108, 49, 28, 205, 153, 105, 244, 101, 186, 6, 62, 91, 35, 217, 46, 234, 209, 4, 74, 82, 28, 161, 239, 93, 25, 255, 161, 13, 164, 119, 95, 232, 55, 65, 121, 133, 202, 194, 155, 93, 227, 5, 169, 58, 58, 62, 17, 39, 251, 36, 118, 79, 253, 222, 221, 29, 102, 157, 164, 226, 237, 109, 251, 97, 182, 237, 104, 83, 83, 89, 230, 77, 79, 215, 215, 235, 230, 37, 112, 101, 228, 166, 71, 253, 7, 108, 217, 13, 18, 79, 237, 39, 182, 117, 140, 191, 116, 102, 19, 4, 77, 154, 102, 23, 125, 190, 187, 217, 19, 230, 83, 117, 65, 171, 231, 90, 125, 62]

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

transbase=[]
for j in l00:
    a=str(bin(j))
    b=list(a)
    c=b[2:]
    while len(c) < 8:
        c.insert(0,'0')
    d=''.join(c)
    transbase.append(basecon(d))
    
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

def main():
    repsymreal=[]
    for i in transbase:
        repsymreal.append(transcon(i))
    
    for i in repsymreal:
        print(i,end=' ')
    
    print('---')
    
    #len=16
    
    lll=[60, 252, 488, 736, 2368, 2430, 2940, 3364, 3600, 3786, 3835, 4055, 5233, 5491, 5813, 6162]
    
    lindex=[]
    for i in lll:
        for j in range(10):
            lindex.append((i-1)*10+j+1)
            
    for i in lindex:
        print(i,end=' ')

main()