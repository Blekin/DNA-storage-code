# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 13:45:35 2021

@author: Fajia Sun
"""

import Levenshtein
from reedsolo import RSCodec
import finalsplit2
import pickle
import time

indexseq=['GTTCT', 'CGTTC', 'CTCTT', 'TGTTC', 'TCTTC', 'TCGTT', 'CGTTG', 'GCGTT', 'TTCTC', 'TCGTC', 'GTTCG', 'TTCTT', 'CTCGT', 'CGTCT', 'TTTCT', 'GCGTC', 'TGTTG', 'GGCGT', 'GGTTC', 'TGGTT', 'GTCTT', 'GTTGG', 'GTGTT', 'CTCTG', 'CTGGT', 'TCTTT', 'CCTCT', 'CTGTT', 'GCGTG', 'TCTCT', 'GTTGT', 'GTCGT', 'GTGGT', 'TTCGT', 'TTCTG', 'GTTTG', 'TGGTG', 'TCTGC', 'TGGTC', 'CGTCG', 'TGCTG', 'TTGTC', 'TCTGG', 'GTCTG', 'GTTTC', 'TGGCG', 'TTGTT', 'TCGTG', 'GGTTG', 'TCTTG', 'GTGTC', 'GCTGG', 'CGTTT', 'GCTCT', 'TGCGT', 'CTGTC', 'CGCGT', 'TCTGT', 'GGCTG', 'TGTCT', 'CCTCG', 'CGTGT', 'GCTGT', 'GGTGG', 'CGTGG', 'CCGTT', 'TCTCG', 'CTTCT', 'GGTCG', 'GTTGC', 'GGTCT', 'TGGGC', 'CGTGC', 'TGCTC', 'TGGGT', 'GTGCG', 'CGCTC', 'GGTGT', 'CTGCT', 'CCTGT', 'TCCTC', 'CTGGC', 'GTGGC', 'GCTGC', 'CGGTC', 'GTCTC', 'GGTGC', 'TTTCG', 'GTTCC', 'CGCTG', 'TGTTT', 'TGTCG', 'CTGCG', 'TGCCG', 'CCGTC', 'GCCTC', 'CGGTT', 'GTGCT', 'CTCTC', 'CGGTG', 'GCGGT', 'CTTCG', 'TCCGT', 'CTTTC', 'GGGCG', 'GTGGG', 'CCTGG', 'TTTGC', 'CGGCG', 'CCTGC', 'TTTGG', 'TTCGC', 'CCTTC', 'CTCCT', 'CTCGC', 'GCCTG', 'GGCTC', 'GTGCC', 'GCTCG', 'TTTGT', 'CCCTC', 'GGCGG', 'GGCGC', 'TTGGT', 'TGCCT', 'CCGTG', 'TGGCT', 'TCGGT', 'TTGCG', 'GGGTT', 'CGCCG', 'TTCCT', 'TTGCT', 'CGCCT', 'TCTCC', 'CTGGG', 'TGCGG', 'GCGCT', 'CGTCC', 'TGCGC', 'GTCCT', 'CTTTG', 'GTCGC', 'GGGTC', 'TCGCT', 'CTGCC', 'TGTGC', 'CCGGC', 'TTTTC', 'TTGGC', 'TCCTG', 'TTCGG', 'TCGCG', 'GGTTT', 'TGTGG', 'GTGTG', 'GCGCC', 'TCGCC', 'GTCGG', 'CTGTG', 'CCGCC', 'CGGCT', 'CTTGT', 'CCGGT', 'GGCCT', 'GCTTC', 'TTCCG', 'TTGCC', 'CTCCG', 'GGGCT', 'CCCGT', 'TTGTG', 'TCGGC', 'GCCGT', 'CTCGG', 'CCGCG', 'GCGCG', 'TCCTT', 'GTCCG', 'CCGCT', 'TGTCC', 'GCGGC', 'TCCGC', 'TTTCC', 'CGGGC', 'GGGTG', 'CTTCC', 'TGTGT', 'CCCTG', 'CTTGC', 'TTTTG', 'TCCGG', 'TGGCC', 'GCCTT', 'CGCGC', 'GCCGG', 'GCCCT', 'CGGGT', 'CGCGG', 'GCCGC', 'GCTCC', 'CCTTT', 'TTGGG', 'CCTCC', 'TGCTT', 'CCTTG', 'GCTTT', 'GGTCC', 'GGGCC', 'GCCCG', 'TGCCC', 'CGCTT', 'TTCCC', 'GGGGC', 'GTTTT', 'GTCCC', 'GCGGG', 'CGCCC', 'TCGGG', 'CCCTT', 'CCCGC', 'GGCTT', 'TCCCT', 'CCGGG', 'CCCGG', 'CTTGG', 'GGGGT', 'TGGGG', 'GGCCC', 'CCCCT', 'GCTTG', 'TCCCG', 'CTTTT', 'CTCCC', 'CCCCG', 'GCCCC', 'TCCCC', 'CGGGG', 'TTTTT', 'CGGCC', 'GGCCG', 'CCCCC', 'GGGGG']

Ns=24
indexseq=indexseq[:Ns]

lenc=4 #R=4

def splitnew(seq):
    lseq=list(seq)
    lseq2=list(seq)
    seqlist=[]
    for i in range(int(Ns/2)):
        start=indexseq[i]
        end=indexseq[i+1]
        S=10
        empty=[start]+(["A"]+["S"]*4)*S+[end]+(["A"]+["S"]*4)*S
        eseq=''.join(empty)
        ldouble=[]
        #estimated length:5+S*10+5=110
        for j in range(105,116):
            compare=''.join(lseq[:j])
            sim=Levenshtein.editops(eseq,compare)
            diff=[]
            for p in sim:
                if p[0] != 'replace':
                    diff.append(p)
            ldouble.append([j,len(diff)])
        sort=sorted(ldouble,key=(lambda x:x[1]))
        position=sort[0][0]
        splitseq=lseq[:position-55]
        noindex=splitseq[4:]
        seqlist.append(''.join(noindex))
        lseq=lseq[position-55:]

    seqlist2=[]
    for i in range(Ns-int(Ns/2)):
        end=indexseq[-(i+1)]
        start=indexseq[-(i+2)]
        empty=[start]+(["A"]+["S"]*4)*S+[end]+(["A"]+["S"]*4)*S
        eseq=''.join(empty)
        ldouble=[]
        for j in range(105,116):
            compare=''.join(lseq2[(len(lseq2)-j):])
            sim=Levenshtein.editops(eseq,compare)
            diff=[]
            for p in sim:
                if p[0] != 'replace':
                    diff.append(p)
            ldouble.append([j,len(diff)])
        sort=sorted(ldouble,key=(lambda x:[x[1],x[0]]))
        position=sort[0][0]
        splitseq=lseq2[(len(lseq2)-position+55):]
        noindex=splitseq[4:]
        seqlist2.append(''.join(noindex))
        lseq2=lseq2[:(len(lseq2)-position+55)]
    seqlist2.reverse()
    
    return seqlist+seqlist2

def posa(baseseq):
    baseseq=list(baseseq)
    #print(baseseq)
    while len(baseseq) < 2+((1+lenc)*10):
        baseseq.insert(0,'S')
    ret=[]
    posofa=[]
    for i in range(len(baseseq)):
        if baseseq[i] == 'A':
            posofa.append(i)
    
    for j in range(1,lenc+2):
        for i in range(len(posofa)-j):
            if posofa[i+j]-posofa[i] == lenc+1:
                ret.append([posofa[i],baseseq[(posofa[i]+1):(posofa[i]+lenc+1)]])
        if j <= len(posofa):
            ret.append([posofa[-j],baseseq[(posofa[-j]+1):(posofa[-j]+lenc+1)]])

    result=[]
    for i in ret:
        if i not in result:
            result.append(i)

    result2=[]
    for i in range(len(result)):
        for j in range(len(result)):
            if i != j and result[i][0]//(lenc+1) == result[j][0]//(lenc+1):
                bifeni=0
                bifenj=0
                for p in range(1,5):
                    if result[i][0]-(lenc+1)*p in posofa:
                        bifeni+=1
                    if result[i][0]+(lenc+1)*p in posofa:
                        bifeni+=1                
                    if result[j][0]-(lenc+1)*p in posofa:
                        bifenj+=1
                    if result[j][0]+(lenc+1)*p in posofa:
                        bifenj+=1                
                if bifeni > bifenj:
                    result[j]=[-1,'']
                    result2.append(result[i])
                if bifeni <= bifenj:
                    result[i]=[-1,'']
                    result2.append(result[j])
            else:
                result2.append(result[i])
                result2.append(result[j])

    resultq=[]
    for i in result:
        if i[0] != -1:
            resultq.append(i)
    #print(len(resultq))
    results=[]
    for i in resultq:
        if i not in results:
            results.append(i)
    #print(len(results))
    #print(results)
    resultf=[]
    length=0
    for i in range(len(results)):
        resultf.append(results[i])
        length+=1
    
    for i in range(len(results)):
        results[i][0]=results[i][0]//(lenc+1)
    #print(length,end=',')
    for i in range(len(resultf)):
        resultf[i][1]=''.join(resultf[i][1])
        
    resultf2=[]
    for i in resultf:
        if 0<= i[0] <=9 and len(i[1]) == lenc:
            resultf2.append(i)
    return resultf2

def smsdecode(seq1):
    seq24=splitnew(seq1)
    
    ldecode=[]
    #start=time.time()
    for i in range(len(seq24)):
        ldecode.append(posa(seq24[i]))
    #end=time.time()
    #inner_time=end-start
    #print(inner_time,end=',')

    counts=0
    for i in range(16):
        for k in range(len(ldecode[i])):
            b=list(ldecode[i][k][1])
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
            ldecode[i][k][1]=n
            counts+=1     
    
    for i in range(16,24):
        for k in range(len(ldecode[i])):
            b=list(ldecode[i][k][1])
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
            ldecode[i][k][1]=n
            counts+=1
    #print(counts) #number of encoding symbols (may contain errors)
    l256=[]
    for i in range(len(ldecode)):
        for k in range(len(ldecode[i])):
            numorder=i*10+ldecode[i][k][0]
            l256.append([numorder,ldecode[i][k][1]])

    lrs=["X"]*240
    for i in range(len(l256)):
        displace=l256[i][0]
        lrs[displace]=l256[i][1]

    erasure=[]
    for i in range(len(lrs)):
        if lrs[i] == "X":
            erasure.append(i)
            lrs[i]=0

    rsc = RSCodec(80)  # 80 check symbols in each encoding group

    try:
        rmes, rmesecc, errata_pos = rsc.decode(bytearray(lrs),erase_pos=erasure)
    except:
        return False
    else:
        return list(rmes)

def main():
    with open('finalbase.txt','r') as p:
        finalbase=p.read().replace(' ','').replace('\n','')
    #50540bp
    
    lresult=[]
    
    splited=finalsplit2.splitall(finalbase)
    for j in splited:
        decoded=smsdecode(j)
        lresult.append(decoded)
    
    #38×160 DNA symbols
    #save the DNA symbols
    with open('encsym.txt','w') as f:
        for i in range(len(lresult)):
            for j in range(len(lresult[i])):
                f.write(str(lresult[i][j]))
                f.write(' ')
            f.write('\n')

main()