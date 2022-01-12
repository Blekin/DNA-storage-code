# -*- coding: utf-8 -*-
"""
Created on Mon May 10 13:29:16 2021

@author: Fajia Sun
"""
import sys

def haffuman_decode(data,code):
    newcode=dict(zip(code.values(), code.keys()))
    i=0
    res=""
    while i < len(data):
        j=i+1
        while j < len(data):
            if data[i:j] in newcode.keys():
                break
            j+=1
        res=res+str(newcode.get(data[i:j]))
        i=j
    return res

#seq=input("Please enter the binary sequence:")
def main():
    name=input("Please enter the name of file containing binary sequence:")
    with open(name,'r') as f:
        seq=f.read()
    
    #dictionary=eval(input("Please enter the decoding dictionary:"))
    name2=input("Please enter the name of file containing decoding dictionary:")
    with open(name2,'r') as f2:
        dictionary=eval(f2.read())
        
        
    try:
        text=haffuman_decode(seq,dictionary)
        print('The decoding result is:')
        print(text)
        #save the decoding result to a text file
        with open('decoding.txt','w') as f3:
            f3.write(text)
        
    except:
        print('Error! Please check if the DNA sequence and decoding dictionary are correct!')
        
main()