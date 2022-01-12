# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 13:41:54 2021

@author: Fajia Sun
"""
import Levenshtein

indexseq=['GTTCT', 'CGTTC', 'CTCTT', 'TGTTC', 'TCTTC', 'TCGTT', 'CGTTG', 'GCGTT', 'TTCTC', 'TCGTC', 'GTTCG', 'TTCTT', 'CTCGT', 'CGTCT', 'TTTCT', 'GCGTC', 'TGTTG', 'GGCGT', 'GGTTC', 'TGGTT', 'GTCTT', 'GTTGG', 'GTGTT', 'CTCTG', 'CTGGT', 'TCTTT', 'CCTCT', 'CTGTT', 'GCGTG', 'TCTCT', 'GTTGT', 'GTCGT', 'GTGGT', 'TTCGT', 'TTCTG', 'GTTTG', 'TGGTG', 'TCTGC', 'TGGTC', 'CGTCG', 'TGCTG', 'TTGTC', 'TCTGG', 'GTCTG', 'GTTTC', 'TGGCG', 'TTGTT', 'TCGTG', 'GGTTG', 'TCTTG', 'GTGTC', 'GCTGG', 'CGTTT', 'GCTCT', 'TGCGT', 'CTGTC', 'CGCGT', 'TCTGT', 'GGCTG', 'TGTCT', 'CCTCG', 'CGTGT', 'GCTGT', 'GGTGG', 'CGTGG', 'CCGTT', 'TCTCG', 'CTTCT', 'GGTCG', 'GTTGC', 'GGTCT', 'TGGGC', 'CGTGC', 'TGCTC', 'TGGGT', 'GTGCG', 'CGCTC', 'GGTGT', 'CTGCT', 'CCTGT', 'TCCTC', 'CTGGC', 'GTGGC', 'GCTGC', 'CGGTC', 'GTCTC', 'GGTGC', 'TTTCG', 'GTTCC', 'CGCTG', 'TGTTT', 'TGTCG', 'CTGCG', 'TGCCG', 'CCGTC', 'GCCTC', 'CGGTT', 'GTGCT', 'CTCTC', 'CGGTG', 'GCGGT', 'CTTCG', 'TCCGT', 'CTTTC', 'GGGCG', 'GTGGG', 'CCTGG', 'TTTGC', 'CGGCG', 'CCTGC', 'TTTGG', 'TTCGC', 'CCTTC', 'CTCCT', 'CTCGC', 'GCCTG', 'GGCTC', 'GTGCC', 'GCTCG', 'TTTGT', 'CCCTC', 'GGCGG', 'GGCGC', 'TTGGT', 'TGCCT', 'CCGTG', 'TGGCT', 'TCGGT', 'TTGCG', 'GGGTT', 'CGCCG', 'TTCCT', 'TTGCT', 'CGCCT', 'TCTCC', 'CTGGG', 'TGCGG', 'GCGCT', 'CGTCC', 'TGCGC', 'GTCCT', 'CTTTG', 'GTCGC', 'GGGTC', 'TCGCT', 'CTGCC', 'TGTGC', 'CCGGC', 'TTTTC', 'TTGGC', 'TCCTG', 'TTCGG', 'TCGCG', 'GGTTT', 'TGTGG', 'GTGTG', 'GCGCC', 'TCGCC', 'GTCGG', 'CTGTG', 'CCGCC', 'CGGCT', 'CTTGT', 'CCGGT', 'GGCCT', 'GCTTC', 'TTCCG', 'TTGCC', 'CTCCG', 'GGGCT', 'CCCGT', 'TTGTG', 'TCGGC', 'GCCGT', 'CTCGG', 'CCGCG', 'GCGCG', 'TCCTT', 'GTCCG', 'CCGCT', 'TGTCC', 'GCGGC', 'TCCGC', 'TTTCC', 'CGGGC', 'GGGTG', 'CTTCC', 'TGTGT', 'CCCTG', 'CTTGC', 'TTTTG', 'TCCGG', 'TGGCC', 'GCCTT', 'CGCGC', 'GCCGG', 'GCCCT', 'CGGGT', 'CGCGG', 'GCCGC', 'GCTCC', 'CCTTT', 'TTGGG', 'CCTCC', 'TGCTT', 'CCTTG', 'GCTTT', 'GGTCC', 'GGGCC', 'GCCCG', 'TGCCC', 'CGCTT', 'TTCCC', 'GGGGC', 'GTTTT', 'GTCCC', 'GCGGG', 'CGCCC', 'TCGGG', 'CCCTT', 'CCCGC', 'GGCTT', 'TCCCT', 'CCGGG', 'CCCGG', 'CTTGG', 'GGGGT', 'TGGGG', 'GGCCC', 'CCCCT', 'GCTTG', 'TCCCG', 'CTTTT', 'CTCCC', 'CCCCG', 'GCCCC', 'TCCCC', 'CGGGG', 'TTTTT', 'CGGCC', 'GGCCG', 'CCCCC', 'GGGGG']

def splitall(seq):
    lseq=list(seq)
    lseq2=list(seq)
    seqlist=[]
    for i in range(19):
        empty="GGATGTGGACGTTCTA"
        ldouble=[]
        for j in range(1310,1350): #1330
            compare=''.join(lseq[j:j+16])
            sim=Levenshtein.editops(empty,compare)
            ldouble.append([j,len(sim)])
        #sort=sorted(ldouble,key=(lambda x:[x[1],x[0]]))
        sort=sorted(ldouble,key=(lambda x:x[1]))
        #print(sort)
        position=sort[0][0]
        splitseq=lseq[:position]
        #print(len(splitseq))
        ldouble2=[]
        for j in range(16):
            fenge=splitseq[j:j+16]
            xulie=''.join(fenge)
            zhengque="GGATGTGGACGTTCTA"
            simtou=Levenshtein.editops(xulie,zhengque)
            ldouble2.append([j,len(simtou)])
        sort2=sorted(ldouble2,key=(lambda x:x[1]))
        position2=sort2[0][0]
        #print(sort2)
        splitseq2=splitseq[position2+10:]
        #print(len(splitseq2))
        seqlist.append(''.join(splitseq2))
        lseq=lseq[position:]
        #print(sort[0])
        #print(len(splitseq))
        #print(len(lseq))
    #seqlist.append(''.join(lseq))
    seqlist2=[]
    for i in range(19):
        empty="GGATGTGGACGTTCTA"
        ldouble=[]
        for j in range(1310,1350): #1330
            compare=''.join(lseq2[(len(lseq2)-j):(len(lseq2)-j+16)])
            sim=Levenshtein.editops(empty,compare)
            ldouble.append([j,len(sim)])
        #sort=sorted(ldouble,key=(lambda x:[x[1],x[0]]))
        sort=sorted(ldouble,key=(lambda x:x[1]))
        #print(sort)
        position=sort[0][0]
        splitseq=lseq2[(len(lseq2)-position):]
        #print(len(splitseq))
        ldouble2=[]
        for j in range(16):
            fenge=splitseq[j:j+16]
            xulie=''.join(fenge)
            zhengque="GGATGTGGACGTTCTA"
            simtou=Levenshtein.editops(xulie,zhengque)
            ldouble2.append([j,len(simtou)])
        sort2=sorted(ldouble2,key=(lambda x:x[1]))
        position2=sort2[0][0]
        splitseq2=splitseq[position2+10:]
        #print(len(splitseq2))
        seqlist2.append(''.join(splitseq2))
        #print(len(splitseq2))
        lseq2=lseq2[:(len(lseq2)-position)]
    seqlist2.reverse()
    return seqlist+seqlist2