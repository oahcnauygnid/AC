from utils import *
from WM import *
from SPTM import *
from CWM import *

import time
import math
import numpy as np
import os

methords_num = 6
test_dir = "./file/test_nums/"
result_dir = "./file/result/"
if(not os.path.exists(result_dir)):
    os.mkdir(result_dir)


WM_k = 10
WM_with_AS_k = 20
SPTM_m = 63
CWM_k = WM_k
CWM_s = 10
CWM_with_AS_k = WM_with_AS_k
CWM_with_AS_s = 20

#test1
bound = 100
test1_print_step = 100
#test2
num = 50
BITS = [160,384,512,1024,2048,4096]
P = [0.1,0.2,0.4,0.5,0.6,0.8,0.9]
test2_print_step = 100   
#test4

def test1(bound=None,filename=None):
    if(filename is None):
        filename = test_dir+"test1/"+"l(e)≤22.txt"
    with open(filename,encoding="utf-8") as f:
        if(bound is not None):
            lines = list(f)[2:]
            lines = lines[:bound]
            print("test for %d of l(e)≤22 with l,BM,WM,SPTM,CWM"%bound)
        else:
            lines = list(f)[2:]
            print("test for all of l(e)≤22 with l,BM,WM,SPTM,CWM")
    
    total_num = len(lines)        
    length = [[]]*total_num
    chain = [[]]*total_num
    dict = [[0]*methords_num for _ in range(MAXL)]
    t = time.perf_counter()
    i0 = 0
    for i in range(total_num):
        a,b = lines[i].split()[:2]
        e = int(a)
        le = int(b)
        
        length[i],chain[i] = test_num(e,le)
        for j in range(methords_num):
            dict[length[i][j+2]-length[i][1]][j] += 1
        
        if((i+1)%test1_print_step==0 or i+1==total_num):    
            print(f'time:{time.perf_counter() - t:.8f}s') 
            print("%d/%d=%.2f%%"%(i+1,total_num,((i+1)/total_num)*100)) 
            t = time.perf_counter()
            myFileWriter(length[i0:i+1], result_dir+"test1_length.txt", chain[i0:i+1], result_dir+"test1_chain.txt",option="l(e)")
            i0 = i + 1
    
            with open(result_dir+"test1_length.txt","a+",encoding="utf-8") as f:
                x_title = "%5s %18s %18s %18s %18s %18s %18s\n"%("","BM ","WM ","WM(AS)","SPTM ","CWM ","CWM(AS)")
                f.write(x_title)
                x_title = "%10s"%("-l(e)") + "%8s %10s"%("num","weight")*methords_num + "\n"
                f.write(x_title)
                f.write("%s\n"%("-"*len(x_title)))
                for i1 in range(MAXL):
                    if(sum(dict[i1])==0):
                        break
                    else:
                        f.write("%9d "%i1)
                        for j1 in range(methords_num):
                            f.write("%8d %10.6f"%(dict[i1][j1],dict[i1][j1]/total_num))
                        f.write("\n")
                f.write("%s\n"%("="*200))
        
    myFileWriter(length, result_dir+"test1_length.txt", chain, result_dir+"test1_chain.txt",option="l(e)")
    
    print("test done")


def test2(filename=None):
    
    def test_nums(filename):
        with open(filename) as f:
            lines = list(f)
        lines_num = len(lines)
        length = [[]]*lines_num
        chain = [[]]*lines_num
        for i in range(lines_num):
            es = lines[i].split()[0]
            e = int(es)
            
            length[i],chain[i] = test_num(e)
                
            
        myFileWriter(length, result_dir+"test2_length.txt", chain, result_dir+"test2_chain.txt")
    
        return
    
    total_num = len(BITS)*len(P)
    if(filename is None):
        i = 0
        for bits in BITS:
            for p in P:
                t = time.perf_counter() 
                filename = "%s%s%dbits_with_prob=%.2f.txt"%(test_dir,"test2/",bits,p)
                print("test %s"%(filename))
                test_nums(filename)  
                print(f'time:{time.perf_counter() - t:.8f}s') 
                print("%d/%d=%.2f%%"%(i+1,total_num,((i+1)/total_num)*100)) 
                i += 1  
    else:
        print("test %s"%(filename))
        test_nums(filename)
        
    print("test done")     

def test3():
    
    def test_nums(filename):
        with open(filename) as f:
            lines = list(f)
        lines_num = len(lines)
        length = [[]]*lines_num
        chain = [[]]*lines_num
        for i in range(lines_num):
            es = lines[i].split()[0]
            e = int(es)
            
            length[i],chain[i] = test_num(e)
        
        myFileWriter(length, result_dir+"test3_length.txt", chain, result_dir+"test3_chain.txt")

        return
            
    total_num = len(BITS)    
    i = 0     
    for bits in BITS:
        t = time.perf_counter()
        filename = "%s%s%dbits_cross.txt"%(test_dir,"test3/",bits)
        print("test %s"%(filename))
        
        test_nums(filename)
        
        print(f'time:{time.perf_counter() - t:.8f}s') 
        print("%d/%d=%.2f%%"%(i+1,total_num,((i+1)/total_num)*100))
        
        i += 1
    
    print("test done")     
    
def test_num(e,option="p"):
    '''
    用各方法测试一个数
    '''
    if(option=="p"):
        P = h(e)/n(e)
    else:
        P = option
    
    l_BM = n(e)+h(e)-2
        
#     t = time.perf_counter()
    l_WM = MAXSIZE
    c_WM = []
    for k in range(1,WM_k+1):
        if(2**k-1>e):
            break
        c = WM(k, e)
        #assert c[-1]==e,"WM wrong,e=%d,k=%d,c=%s"%(e,k,str(c))
        lt = len(c)-1
        if(lt < l_WM):
            l_WM = lt
            c_WM = c
#     print(f'WM:{time.perf_counter() - t:.8f}s')                
#                 
#     t = time.perf_counter()
    l_WM_with_AS = MAXSIZE
    c_WM_with_AS = []
    for k in range(1,WM_with_AS_k+1):
        if(2**k-1>e):
            break
        c = CWM(k,0,e,AS=True)
        #assert c[-1]==e,"M wrong,e=%d,k=%d,c=%s"%(e,k,str(c))
        lt = len(c)-1
        if(lt < l_WM_with_AS):
            l_WM_with_AS = lt
            c_WM_with_AS = c
#     print(f'WM_with_AS:{time.perf_counter() - t:.8f}s')  
#     
#     t = time.perf_counter()
    l_SPTM = MAXSIZE
    c_SPTM = []
    for m in range(1,SPTM_m+1,2):
        if(m>e):
            break
        c = SPTM(m, e)
        #assert c[-1]==e,"SPTM wrong,e=%d,m=%d,c=%s"%(e,m,str(c))
        lt = len(c)-1
        if(lt < l_SPTM):
            l_SPTM = lt
            c_SPTM = c
#     print(f'SPTM:{time.perf_counter() - t:.8f}s') 
#             
#     t = time.perf_counter()
    l_CWM = MAXSIZE
    c_CWM = []
    for k in range(1,CWM_k+1):
        for s in range(0,CWM_s+1):
            if(2**(k+s)-1>e):
                break
            c = CWM(k,s, e)
            #assert c[-1]==e,"M wrong,e=%d,k=%d,s=%d,c=%s"%(e,k,s,str(c))
            lt = len(c)-1
            if(lt < l_CWM):
                l_CWM = lt
                c_CWM = c
#     print(f'CWM:{time.perf_counter() - t:.8f}s') 

#     t = time.perf_counter()
    l_CWM_with_AS = MAXSIZE
    c_CWM_with_AS = []
    for k in range(1,CWM_with_AS_k+1):
        for s in range(0,CWM_with_AS_s+1):
            if(2**(k+s)-1>e):
                break
            c = CWM(k,s,e,AS=True)
            #assert c[-1]==e,"M wrong,e=%d,k=%d,s=%d,c=%s"%(e,k,s,str(c))
            lt = len(c)-1
            if(lt < l_CWM_with_AS):
                l_CWM_with_AS = lt
                c_CWM_with_AS = c
#     print(f'CWM:{time.perf_counter() - t:.8f}s')
     
    length = [e,P,l_BM,l_WM,l_WM_with_AS,l_SPTM,l_CWM,l_CWM_with_AS]
    chain = [c_WM,c_WM_with_AS,c_SPTM,c_CWM,c_CWM_with_AS]
    
    return length,chain
        
        
def myFileWriter(length,length_file,chain,chain_file,option="p"):
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    with open(length_file,"a+") as f:
        f.write("%s\n"%("="*200))
        x_title = "%8s %8s %8s  %8s%8s %8s  %8s   %8s\n"%(option,"BM","WM","WM(AS)","SPTM","CWM","CWM(AS)","e")
        f.write("%s\n"%localtime)
        f.write("%s\n"%("--"*len(x_title)))
        f.write(x_title)
        f.write("%s\n"%("--"*len(x_title)))
        for i in range(len(length)):
            if(option=="p"):
                f.write("%8.2f %8d %8d %8d %8d %8d %8d     %8d\n"%(length[i][1],length[i][2],length[i][3],length[i][4],length[i][5],length[i][6],length[i][7],length[i][0]))
            else:
                f.write("%8d %8d %8d %8d %8d %8d %8d     %8d\n"%(length[i][1],length[i][2],length[i][3],length[i][4],length[i][5],length[i][6],length[i][7],length[i][0]))
        f.write("%s\n"%("--"*len(x_title)))
        length_sum = np.sum(length,axis=0)
        if(option=="p"):
            f.write("%8s %8d %8d %8d %8d %8d %8d\n"%("sum",length_sum[2],length_sum[3],length_sum[4],length_sum[5],length_sum[6],length_sum[7]))
            f.write("%s\n"%("="*200))
        else:
            f.write("%8d %8d %8d %8d %8d %8d %8d\n"%(length_sum[1],length_sum[2],length_sum[3],length_sum[4],length_sum[5],length_sum[6],length_sum[7]))
            f.write("%s\n"%("--"*len(x_title)))
        
    with open(chain_file,"a+") as f:
        f.write("%s\n"%("="*200))
        for i in range(len(chain)):
            f.write("%d\n"%(length[i][0]))
            f.write("   WM  :%5d%8s\n WM(AS):%5d%8s\n  SPTM :%5d%8s\n  CWM  :%5d%8s\nCWM(AS):%5d%8s\n"%(length[i][3],str(chain[i][0]),length[i][4],str(chain[i][1]),length[i][5],str(chain[i][2]),length[i][6],str(chain[i][3]),length[i][7],str(chain[i][4])))
            f.write("%s\n"%("="*200))    
    
def get_kbits(bits,p,num,mode=2): 
    if(mode==2):
        with open("%s%s%dbits_with_prob=%.2f.txt"%(test_dir,"test2/",bits,p),"w") as f:
            for _ in range(num):
                s = "1"
                for _ in range(bits-1):
                    if(flip(p)):
                        s+="1"
                    else:
                        s+="0"
                f.write("%d %s\n"%(int(s,2),s))
    elif(mode==3):
        with open("%s%s%dbits_cross.txt"%(test_dir,"test3/",bits),"w") as f:
            for _ in range(num):
                k = random.randint(4,6)
                R = n(k)
                s = random.randint(40,60) 
                t = "1" + "0"*s + binary(k)
                lt = len(t)
                v = min(R+1,bits//lt)
                t = int(t,2)
                t0 = t
                M = [0]*(bits+1)
                op = []
                ed = []
                for _ in range(v):
                    while(1):
                        j = random.randint(0,bits)
                        flag = 1
                        for j0 in op:
                            if(j0==(j-lt) or j0==j):
                                flag = 0
                                break
                        for j0 in ed:
                            if((j0-j<R and j0-j>(-R)) or (j0-(j-lt)<R and j0-(j-lt)>(-R))):
                                flag = 0
                                break
                        if(flag==1):
                            ed.append(j)
                            op.append(j-lt)
                            break
                    M[j] = t
                j = 0
                while(M[j]==0):
                    j += 1
                t = M[j]
                j += 1
                while(j<=bits):
                    t <<= 1
                    if(M[j]!=0):
                        t += M[j]
                    j += 1
                t = int(binary(t),2)
                shift_bits = bits - n(t)
                if(shift_bits>0):
                    t = (t<<shift_bits) + t0
                else:
                    t = (t>>(-shift_bits)) + t0
                assert n(t)==bits
                f.write("%d %s\n"%(t,binary(t)))


                    
    elif(mode==4):
        with open("%s%s%dbits_cross.txt"%(test_dir,"test4/",bits),"w") as f:
            for _ in range(num):
                if(bits<500):
                    k = random.randint(5,10)
                elif(bits<1000):
                    k = random.randint(10,15)
                else:
                    k = random.randint(15,20)
                s = random.randint(6,10) 
                R = math.ceil(k/2)
                t = "1"*k
                t = t[:-R] + "0"*s + t[-R:]
                t = int(t,2)
                M = [0]*(bits+1)
                op = []
                ed = []
                for _ in range(k):
                    while(1):
                        j = random.randint(0,bits)
                        flag = 1
                        for j0 in op:
                            if((j0-(j-R-s)<R and j0-(j-R-s)>(-R)) or (j0-j<R and j0-j>(-R))):
                                flag = 0
                                break
                        for j0 in ed:
                            if((j0-(j-R-s)<R and j0-(j-R-s)>(-R)) or (j0-j<R and j0-j>(-R))):
                                flag = 0
                                break
                        if(flag==1):
                            ed.append(j)
                            op.append(j-R-s)
                            break
                    M[j] = t
                j = 0
                while(M[j]==0):
                    j += 1
                t = M[j]
                j += 1
                while(j<=bits):
                    t <<= 1
                    if(M[j]!=0):
                        t += M[j]
                    j += 1
                t = int(binary(t).strip("0"),2)
                f.write("%d %s\n"%(t,binary(t)))
            '''
            for _ in range(num):
                k = random.randint(2,10) 
                kk = 2**k - 1
                s = random.randint(10,20) 
                R = math.ceil(k/2)
                v = math.floor(bits/k)
                M = [0]*(bits+1)
                for _ in range(v):
                    t = random.randint(0,kk)
                    if(n(s)>R):
                        t = binary(s)
                        t = t[:-R] + "0"*s + t[-R:]
                        t= int(t,2)
                    j = random.randint(0,bits)
                    M[j] = t
                j = 0
                while(M[j]==0):
                    j += 1
                t = M[j]
                j += 1
                while(j<=bits):
                    t <<= 1
                    if(M[j]!=0):
                        t += M[j]
                    j += 1
                t = int(binary(t).strip("0"),2)
                f.write("%d %s\n"%(t,binary(t)))
            '''
    #print("get %d of %d bits with prob.=%.2f done"%(num,k,p))
    
def get_test_nums(mode=2):
    if(mode==2):
        for bits in BITS:
            for p in P:
                get_kbits(bits, p, num, mode=mode)
    elif(mode==3):
        for bits in BITS:
            get_kbits(bits, 0,num, mode=mode)
    elif(mode==4):
        for bits in BITS:
            get_kbits(bits, 0,num, mode=mode)
    elif(mode==5):#mode=2，仅用于p=0.95
        for bits in BITS:
            get_kbits(bits, 0.95,num, mode=2)
            
    print("get_test_nums done")

def test_result_parse(filename=None,option="sum"):
    if(filename==None):
        filenames=[result_dir+"test1_length.txt",result_dir+"test2_length.txt",result_dir+"test3_length.txt"]
    else:
        filenames=[filename]
    for filename in filenames:
        with open(filename,"r") as f:
            lines = list(f)
            with open(filename,"a+") as fw:
                fw.write("%s\n"%("="*200))
                fw.write("Sum list\n")
                for line in lines:
                    if(option in line):
                        fw.write(line.replace(option,""))
            
                fw.write("%s\n"%("="*200))
    print("test_result_parse done")
    
if __name__ == "__main__":

    test1()
    # get_test_nums(mode=2)
    # test2()
    # get_test_nums(mode=3)
    # test3()

    # test_result_parse()
    
