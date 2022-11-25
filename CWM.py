from utils import *
import math

def pre_chain(k,s):
    a = [0]*(2**(k-1)+s+2)

    a[0] = 1
    a[1] = 2
    i = 2
    R = math.ceil(k/2)
    L = k - R
    p = 2**R
    for t in range(3,p,2):
        a[i] = t
        i += 1
    a[i] = p
    i += 1
    for _ in range(s):
        a[i] = a[i-1]<<1
        i += 1
    q = a[i-1]
    u = 2**L-1
    v = 0
    for _ in range(u):
        v += q
        for t in range(1,p,2):
            a[i] = v + t
            i += 1
    #assert i==2**(k-1)+s+2,"i!=2**(k-1)+s+2"
     
    if(s==0):
        del a[2**(R-1)+1]
        i -= 1
        R = 0
    
    return a

def CWM(k,s,e,AS=False):

    if(e==1):
        return [1]
    a = [0]*MAXSIZE
    e = binary(e)
    ns = len(e)
#     
 
    R = math.ceil(k/2)
    if(s==0):   
        R = 0
        pre_all = 2**(k-1)+1
    else:
        pre_all = 2**(k-1)+s+2
        
    i = 0

    t = k + s
    op = 0
    ed = 0
    lM = ns + 1
    M = [0]*lM
    while(op<ns):

        if(op+t>ns):
            t = ns - op
        m = e[op:op+t]
        lm = len(m)
        while(m[lm-1]=="0"):
            lm -= 1

        if(lm<=s+R):
            if(lm>R):
                lm = R 
            while(m[lm-1]=="0"):
                lm -= 1
            c = lm
        else:
            c = lm - s - R
            m = m[:c] + "0"*s + m[c+s:]
            e = e[:op+c+s] + "0"*R +e[op+lm:]

        m = m[:lm]
        ed = op + lm
        op += c
        M[ed] = decimal(m)
        

        while(op<ns and e[op]=="0"):
                op += 1 
                

    pre = []
    j = 0
    while(M[j]==0):
        j += 1
    a[i] = M[j]
    pre.append(M[j])
    i += 1
    j += 1
    while(j<lM):
        a[i] = a[i-1]<<1
        i += 1
        if(M[j]!=0):
            a[i] = a[i-1] + M[j]
            pre.append(M[j])
            i += 1
        j += 1
    
    if(AS):
        pre = list(dict.fromkeys(pre))
#         use = len(pre)
#         print("use=%d%s"%(use,str(pre)))
#         print("pre",pre_all,":",a[:pre_all])
        pre = ASA(pre)
        if(pre_all<len(pre)):
#             print("make_seq false,use=%d%s,pre_all=%d%s,AS=%d%s"%(use,str(pre1),pre_all,str(a[:pre_all]),len(pre),str(pre)))
            pre = pre_chain(k, s)
#         print("AS",len(pre),":",pre)
#         print("优化：",pre_all - len(pre))
    else:
        pre = CWM_k_s_chain[k-1][s]
    
    a = pre + a[:i]
    
    a = list(dict.fromkeys(a)) 
    return a


def ASA(a):

    CWM_k = 10
    CWM_s = 10
    a.sort()
    if(a[0]==1 and len(a)==1):
        return a
    if(a[0]!=1):
        a.insert(0, 1)
    if(a[1]!=2):
        a.insert(1, 2)
    j = len(a)-1
    while(j>1):
        #m = kn+r
        m = a[j]
        n = a[j-1]
        B = m // n
        C = m - B*n
        i = j
        t = 0
        u = n
        
        l_CWM = MAXSIZE
        c_CWM = []
        for k in range(1,CWM_k+1):
            for s in range(0,CWM_s+1):
                if(2**(k+s)-1>B):
                    break
                c = CWM(k,s, B)
                #assert c[-1]==e,"M wrong,e=%d,k=%d,s=%d,c=%s"%(e,k,s,str(c))
                lt = len(c)-1
                if(lt < l_CWM):
                    l_CWM = lt
                    c_CWM = c
                    
        if(C==0):
            cB = [i*n for i in c][1:-1]
        else:
            cB = [i*n for i in c][1:]
        a = a[:i]+cB+a[i:]

        if(C not in a and C!=0):
            for r in range(j):
                if(a[r]>=C):
                    a.insert(r,C)
                    j += 1
                    break
            
                       
        j -= 1
    
    #a = list(dict.fromkeys(a))
    return a

    
if __name__ == "__main__":
    a = CWM(3,2,95,AS=True)
    print(a)
