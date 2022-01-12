# -*- coding: utf-8 -*-
"""
Created on Mon May 10 14:40:08 2021

@author: Fajia Sun
"""

with open("infsym.txt",'r') as f:
    l256=[]
    lt=f.readlines()
    for i in range(len(lt)):
        lt[i]=lt[i].split(' ')
        lt[i]=lt[i][:160]
        for p in range(len(lt[i])):
            lt[i][p]=int(lt[i][p])
    for i in range(35):
        l256=l256+lt[i]

n=8
lf=[]
for i in range(len(l256)):
    number=l256[i]
    lr=[0]*n
    for j in range(n):
        lr[j]=str(int(number%2))
        number=number//2
    lr.reverse()
    result=''.join(lr)
    lf.append(result)
    
stream=''.join(lf)[:44506]
with open('binary_real.txt','w') as f2:
    f2.write(stream)

