from utils import *
import math
import copy

def BM(e):
    a = [0]*MAXSIZE
    bs = binary(e)
    ns = len(bs)
    a[0] = 1
    i = 1
    for _ in range(ns-1):
        a[i]=a[i-1]<<1
        i += 1
    for j in range(1,ns):
        if(bs[j]=="1"):
            a[i] = a[i-1] + a[ns-1-j]
            i += 1
    return a[:ns+h(e)-1]
    
def SPTM(m,e):

    a = BM(e)
    la = len(a)
    
    rc = BM(m)#root chain
    lr = len(rc)
    
    t = [0]*MAXSIZE
    for j in range(lr):
        t[j] = rc[j]
    nm = n(m)
    t[lr] = 2**nm
    
    for i in range(nm,n(e)):
        j = lr+1
        for _ in range(nm,i):
            t[j] = t[j-1]<<1
            j += 1
        assert t[j-1]==2**i,"t[j-1]!=2**i"
        t[j] = t[j-1] + m
        while(t[j]<e):
            j += 1
            t[j] = t[j-1]<<1
        lt = search(t,la,e)
        if(lt<la):
            a = copy.deepcopy(t[:lt+1])
            la = lt
    
    a = list(dict.fromkeys(a[:la+1]))
    return a

def search(a,l,e):
    for r in range(l+1):
        if(r>=l):
            return l
        if(a[r]==e):
            return r
        elif(a[r]<e and a[r+1]>e):
            for i in range(r-1,-1,-1):
                if(a[r]+a[i]<=e):
                    r += 1
                    a[r] = a[r-1]+a[i]
                if(a[r]==e):
                    return r


if __name__ == "__main__":
    a = SPTM(3,95)
    print(a)