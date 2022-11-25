from utils import *
import math

def WM(k,e):

    if(e==1):
        return [1]
    pre_all = 2**(k-1)+1
    a = [0]*MAXSIZE
    e = binary(e)
    ns = len(e)

    a[0] = 1
    a[1] = 2
#     pre_bound = 2**k - 1
#     for t in range(3,pre_bound+1,2):
#         a[i] = t
#         i = i+1
    pre = WM_k_chain[k-1]
    i = pre_all
    #assert i==2**(k-1)+1,"i!=2**(k-1)+1"

    j=0
    while(j<ns):

        if(j+k>=ns):
            k=ns-j
        m=e[j:j+k]

        for r in range(k-1,-1,-1):
            if(m[r]=="1"):
                t=r
                break
        

        if(j==0):
            a[i]=decimal(m[0:t+1])
            i=i+1
        else:
            for _ in range(t+1):
                a[i]=a[i-1]<<1
                i=i+1
            a[i]=a[i-1]+decimal(m[0:t+1])
            i=i+1
        for _ in range(t+1,k):
            a[i]=a[i-1]<<1
            i=i+1

        j=j+k
        while(j<ns and e[j]=="0"):
            a[i]=a[i-1]<<1
            i=i+1
            j=j+1
            
    a = pre + a[pre_all+1:i]
    
    a = list(dict.fromkeys(a))
    return a

if __name__ == "__main__":
    a = WM(3,95)
    print(a)