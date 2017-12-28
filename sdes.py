import operator
from key import *

def ip(ent):
    bits = []
    for i in  [2, 6, 3, 1, 4, 8, 5, 7]:
       bits.append(ent[i-1]) 
    return bits

def ip_1(ent):
    bits = []
    for i in  [4, 1, 3, 5, 7, 2, 8, 6]:
       bits.append(ent[i-1]) 
    return bits

def ep(ent):    
    bits = []
    for i in [4, 1, 2, 3, 2, 3, 4, 1]:
        bits.append(ent[i-1])        
    return bits

def xor(var1, var2):
    assert(len(var1)==len(var2))
    bits = [operator.xor(var1[i],var2[i]) for i in range(len(var1))]
    return bits
    
def s(ent,tipo):
    assert(len(ent)==4)
    assert(tipo==0 or tipo==1)
    
    if [ent[0],ent[3]]==[0,0]:
        if [ent[1],ent[2]] == [0,0]:
            s = [0,1],[0,0] 
        if [ent[1],ent[2]] == [0,1]:
            s = [0,0],[0,1]
        if [ent[1],ent[2]] == [1,0]:
            s = [1,1],[1,0]
        if [ent[1],ent[2]] == [1,1]:
            s = [1,0],[1,1]

    if [ent[0],ent[3]]==[0,1]:
        if [ent[1],ent[2]] == [0,0]:
            s = [1,1],[1,0]
        if [ent[1],ent[2]] == [0,1]:
            s = [1,0],[0,0]
        if [ent[1],ent[2]] == [1,0]:
            s = [0,1],[0,1]
        if [ent[1],ent[2]] == [1,1]:
            s = [0,0],[1,1]

    if [ent[0],ent[3]]==[1,0]:
        if [ent[1],ent[2]] == [0,0]:
            s = [0,0],[1,1]
        if [ent[1],ent[2]] == [0,1]:
            s = [1,0],[0,0]
        if [ent[1],ent[2]] == [1,0]:
            s = [0,1],[0,1]
        if [ent[1],ent[2]] == [1,1]:
            s = [1,1],[0,0]        

    if [ent[0],ent[3]]==[1,1]:
        if [ent[1],ent[2]] == [0,0]:
            s = [1,1],[1,0]
        if [ent[1],ent[2]] == [0,1]:
            s = [0,1],[0,1]
        if [ent[1],ent[2]] == [1,0]:
            s = [1,1],[0,0]
        if [ent[1],ent[2]] == [1,1]:
            s = [1,0],[1,1]
    return s[tipo]

def p4(ent):
    bits = []
    for i in  [2, 4, 3, 1]:
       bits.append(ent[i-1])
    return bits

def sw(ent):
    return ent[4:] + ent[:4]
    
def fk(ent, k):
    L = ent[:4]
    R = ent[4:]
    parcial = ep(R)
    parcial = xor(parcial,k)
    parcial = s(parcial[:4],0) + s(parcial[4:],1)
    parcial = p4(parcial)
    parcial = xor(L, parcial)
    return parcial + R
    
def sdes(M,K,sentido='cod'):
    if sentido == 'cod':
    	k1, k2 = keys(K)
    elif sentido == 'dec':
	    k2, k1 = keys(K)
    sdes = ip(M) 
    sdes = fk(sdes,k1)
    sdes = sw(sdes)
    sdes = fk(sdes,k2)
    sdes = ip_1(sdes)
    return sdes 

def cbc_mode(M, K, IV, mode="cod"):
    y = []
    for i, m in enumerate(M):
        if i == 0:
            y_i1 = IV
        xor_res = xor(m, y_i1)
        y_i1 = sdes(xor_res, K, 'cod')
        y.append(y_i1)
    return y
       
if __name__ == '__main__':	
    M = [[0, 1, 0, 0, 0, 0, 1, 1], [0, 1, 1, 1, 0, 0, 1, 0], [0, 1, 1, 1, 1, 0, 0, 1], 
        [0, 1, 1, 1, 0, 0, 0, 0], [0, 1, 1, 1, 0, 1, 0, 0], [0, 1, 1, 0, 1, 1, 1, 1]]
    M_error = [[0, 1, 0, 0, 0, 0, 1, 1], [1, 1, 1, 1, 0, 0, 1, 0], [0, 1, 1, 1, 1, 0, 0, 1], 
        [0, 1, 1, 1, 0, 0, 0, 0], [0, 1, 1, 1, 0, 1, 0, 0], [0, 1, 1, 0, 1, 1, 1, 1]]
    K = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
    IV = [1, 0, 0, 0, 1 , 0, 1, 1]
    cbc_y = cbc_mode(M, K, IV, 'cod')
    cbc_error_y = cbc_mode(M_error, K, IV, 'cod')
    for i in range(len(cbc_y)):
        print("Output R: ", cbc_y[i])
        print("Output E: ", cbc_error_y[i])