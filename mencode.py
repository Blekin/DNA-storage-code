# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 14:01:24 2021

@author: Fajia Sun
"""

import re
import random
import pickle
from reedsolo import RSCodec

indexseq=['GTTCT', 'CGTTC', 'CTCTT', 'TGTTC', 'TCTTC', 'TCGTT', 'CGTTG', 'GCGTT', 'TTCTC', 'TCGTC', 'GTTCG', 'TTCTT', 'CTCGT', 'CGTCT', 'TTTCT', 'GCGTC', 'TGTTG', 'GGCGT', 'GGTTC', 'TGGTT', 'GTCTT', 'GTTGG', 'GTGTT', 'CTCTG', 'CTGGT', 'TCTTT', 'CCTCT', 'CTGTT', 'GCGTG', 'TCTCT', 'GTTGT', 'GTCGT', 'GTGGT', 'TTCGT', 'TTCTG', 'GTTTG', 'TGGTG', 'TCTGC', 'TGGTC', 'CGTCG', 'TGCTG', 'TTGTC', 'TCTGG', 'GTCTG', 'GTTTC', 'TGGCG', 'TTGTT', 'TCGTG', 'GGTTG', 'TCTTG', 'GTGTC', 'GCTGG', 'CGTTT', 'GCTCT', 'TGCGT', 'CTGTC', 'CGCGT', 'TCTGT', 'GGCTG', 'TGTCT', 'CCTCG', 'CGTGT', 'GCTGT', 'GGTGG', 'CGTGG', 'CCGTT', 'TCTCG', 'CTTCT', 'GGTCG', 'GTTGC', 'GGTCT', 'TGGGC', 'CGTGC', 'TGCTC', 'TGGGT', 'GTGCG', 'CGCTC', 'GGTGT', 'CTGCT', 'CCTGT', 'TCCTC', 'CTGGC', 'GTGGC', 'GCTGC', 'CGGTC', 'GTCTC', 'GGTGC', 'TTTCG', 'GTTCC', 'CGCTG', 'TGTTT', 'TGTCG', 'CTGCG', 'TGCCG', 'CCGTC', 'GCCTC', 'CGGTT', 'GTGCT', 'CTCTC', 'CGGTG', 'GCGGT', 'CTTCG', 'TCCGT', 'CTTTC', 'GGGCG', 'GTGGG', 'CCTGG', 'TTTGC', 'CGGCG', 'CCTGC', 'TTTGG', 'TTCGC', 'CCTTC', 'CTCCT', 'CTCGC', 'GCCTG', 'GGCTC', 'GTGCC', 'GCTCG', 'TTTGT', 'CCCTC', 'GGCGG', 'GGCGC', 'TTGGT', 'TGCCT', 'CCGTG', 'TGGCT', 'TCGGT', 'TTGCG', 'GGGTT', 'CGCCG', 'TTCCT', 'TTGCT', 'CGCCT', 'TCTCC', 'CTGGG', 'TGCGG', 'GCGCT', 'CGTCC', 'TGCGC', 'GTCCT', 'CTTTG', 'GTCGC', 'GGGTC', 'TCGCT', 'CTGCC', 'TGTGC', 'CCGGC', 'TTTTC', 'TTGGC', 'TCCTG', 'TTCGG', 'TCGCG', 'GGTTT', 'TGTGG', 'GTGTG', 'GCGCC', 'TCGCC', 'GTCGG', 'CTGTG', 'CCGCC', 'CGGCT', 'CTTGT', 'CCGGT', 'GGCCT', 'GCTTC', 'TTCCG', 'TTGCC', 'CTCCG', 'GGGCT', 'CCCGT', 'TTGTG', 'TCGGC', 'GCCGT', 'CTCGG', 'CCGCG', 'GCGCG', 'TCCTT', 'GTCCG', 'CCGCT', 'TGTCC', 'GCGGC', 'TCCGC', 'TTTCC', 'CGGGC', 'GGGTG', 'CTTCC', 'TGTGT', 'CCCTG', 'CTTGC', 'TTTTG', 'TCCGG', 'TGGCC', 'GCCTT', 'CGCGC', 'GCCGG', 'GCCCT', 'CGGGT', 'CGCGG', 'GCCGC', 'GCTCC', 'CCTTT', 'TTGGG', 'CCTCC', 'TGCTT', 'CCTTG', 'GCTTT', 'GGTCC', 'GGGCC', 'GCCCG', 'TGCCC', 'CGCTT', 'TTCCC', 'GGGGC', 'GTTTT', 'GTCCC', 'GCGGG', 'CGCCC', 'TCGGG', 'CCCTT', 'CCCGC', 'GGCTT', 'TCCCT', 'CCGGG', 'CCCGG', 'CTTGG', 'GGGGT', 'TGGGG', 'GGCCC', 'CCCCT', 'GCTTG', 'TCCCG', 'CTTTT', 'CTCCC', 'CCCCG', 'GCCCC', 'TCCCC', 'CGGGG', 'TTTTT', 'CGGCC', 'GGCCG', 'CCCCC', 'GGGGG']

def errorless(baseseq):
    ret=[]
    for i in range(10):
        single=baseseq[i*5:(i*5+5)]
        if single[0] == 'A':
            ret.append([i,single[1:]])
    return ret

#convert binary stream to base sequences
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

def smsencode(infbase,repbase):
    rq=[]
    for i in range(len(infbase)):
        rq.append(infbase[i][1])
    for i in range(len(repbase)):
        rq.append(repbase[i][1])
    
    encsym1=[]
    for i in range(len(infbase)):
        encsym1.append(infbase[i][0])
    for i in range(len(repbase)):
        encsym1.append(repbase[i][0])
    
    A=0
    B=len(encsym1)
    numofg=16
    resultList=random.sample(range(A,B-1),numofg)
    encsym2=[]
    rq2=[]
    for i in sorted(resultList):
        encsym2.append(encsym1[i])
        rq2.append(rq[i])
    
    #encsym1=encsym1[:numofg]
    
    lencsym=[]
    for i in range(len(encsym2)):
        lencsym.append(errorless(encsym2[i]))
    allencsym=[]
    for i in range(len(lencsym)):
        for j in range(len(lencsym[i])):
            encsym=lencsym[i][j][1]
            allencsym.append(encsym)
    ln=[]
    for i in range(len(allencsym)):
        b=list(allencsym[i])
        for j in range(4):
            if b[j] == 'A':
                b[j]=0
            if b[j] == 'C':
                b[j]=1
            if b[j] == 'G':
                b[j]=2
            if b[j] == 'T':
                b[j]=3
        n=pow(4,0)*b[-1]+pow(4,1)*b[-2]+pow(4,2)*b[-3]+pow(4,3)*b[-4]
        ln.append(n)
        
    rsc = RSCodec(80)
    s160=ln
    rsa=rsc.encode(s160)
    rsb=list(rsa)
    redundancy=rsb[160:]
    indexrs=indexseq[16:24]
    n=10    
    rsbase=[]
    for i in range(8):
        rs10=redundancy[10*i:10*(i+1)]
        binary=[]
        for j in rs10:
            a=str(bin(j))
            b=list(a)
            c=b[2:]
            while len(c) < 8:
                c.insert(0,'0')
            c.insert(0,'0')
            c.insert(0,'0')
            d=''.join(c)
            binary.append(d)
        seq2=''.join(binary)
        baseseq=basecon(seq2)
        rsbase.append(baseseq)

    encode=[]
    for i in range(len(encsym2)):
        encode.append(indexseq[i]+encsym2[i])
    for i in range(len(rsbase)):
        encode.append(indexrs[i]+rsbase[i])
    resultbase=''.join(encode)
    return resultbase,rq2

#you may define some condition for selecting repair symbols
#since repair symbols are surplus
def select(seq):
    return "the seq you do not want" in seq

def main():
    infbase=[]
    repbase=[]
    f=open('screenedbase.txt','r',encoding='ISO8859_1')
    count=0
    for line in f:
        if count % 2 == 0:
            infbase.append(eval(line))
        else:
            repbase.append(eval(line))
        count+=1
    f.close()
    
    
    
    lbiggroup=[]
    lindex=[]
    for i in range(len(infbase)):
        for j in range(100):
            inter,rq2=smsencode(infbase[i],repbase[i])
            if select(inter) == False:
                lindex.append(rq2)
                lbiggroup.append(inter)
                break
    
    finalcode=[]
    for i in range(len(lbiggroup)):
        finalcode.append("GGATGTGGAC")
        finalcode.append(lbiggroup[i])   
    
    finalbase=''.join(finalcode)
    
    print(len(lindex)) #38 (list)
    print(len(finalbase)) #50540 (str)
    
    #save the index
    with open('index.txt','w') as f:
        for i in range(len(lindex)):
            for j in range(len(lindex[i])):
                f.write(str(lindex[i][j]))
                f.write(' ')
            f.write('\n')
    #save the sequence
    with open('finalbase.txt','w') as f2:
        f2.write(finalbase)
        
main()