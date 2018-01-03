import operator
from key import *
import itertools
import numpy as np

def ip(input):
    bits = []
    for i in  [2, 6, 3, 1, 4, 8, 5, 7]:
       bits.append(input[i-1]) 
    return bits

def ip_1(input):
    bits = []
    for i in  [4, 1, 3, 5, 7, 2, 8, 6]:
       bits.append(input[i-1]) 
    return bits

def ep(input):    
    bits = []
    for i in [4, 1, 2, 3, 2, 3, 4, 1]:
        bits.append(input[i-1])        
    return bits

def xor(var1, var2):
    assert(len(var1)==len(var2))
    bits = [operator.xor(var1[i],var2[i]) for i in range(len(var1))]
    return bits
    
def s(input, input_index):
    assert(len(input)==4)
    assert(input_index==0 or input_index==1)
    
    if [input[0],input[3]]==[0,0]:
        if [input[1],input[2]] == [0,0]:
            s = [0,1],[0,0] 
        if [input[1],input[2]] == [0,1]:
            s = [0,0],[0,1]
        if [input[1],input[2]] == [1,0]:
            s = [1,1],[1,0]
        if [input[1],input[2]] == [1,1]:
            s = [1,0],[1,1]

    if [input[0],input[3]]==[0,1]:
        if [input[1],input[2]] == [0,0]:
            s = [1,1],[1,0]
        if [input[1],input[2]] == [0,1]:
            s = [1,0],[0,0]
        if [input[1],input[2]] == [1,0]:
            s = [0,1],[0,1]
        if [input[1],input[2]] == [1,1]:
            s = [0,0],[1,1]

    if [input[0],input[3]]==[1,0]:
        if [input[1],input[2]] == [0,0]:
            s = [0,0],[1,1]
        if [input[1],input[2]] == [0,1]:
            s = [1,0],[0,0]
        if [input[1],input[2]] == [1,0]:
            s = [0,1],[0,1]
        if [input[1],input[2]] == [1,1]:
            s = [1,1],[0,0]        

    if [input[0],input[3]]==[1,1]:
        if [input[1],input[2]] == [0,0]:
            s = [1,1],[1,0]
        if [input[1],input[2]] == [0,1]:
            s = [0,1],[0,1]
        if [input[1],input[2]] == [1,0]:
            s = [1,1],[0,0]
        if [input[1],input[2]] == [1,1]:
            s = [1,0],[1,1]
    return s[input_index]

def p4(input):
    bits = []
    for i in  [2, 4, 3, 1]:
       bits.append(input[i-1])
    return bits

def sw(input):
    return input[4:] + input[:4]
    
def fk(input, k):
    L = input[:4]
    R = input[4:]
    sub_result = ep(R)
    sub_result = xor(sub_result,k)
    sub_result = s(sub_result[:4],0) + s(sub_result[4:],1)
    sub_result = p4(sub_result)
    sub_result = xor(L, sub_result)
    return sub_result + R
    
def sdes(M, K, s_input='cod'):
    if s_input == 'cod':
    	k1, k2 = keys(K)
    elif s_input == 'dec':
	    k2, k1 = keys(K)
    sdes = ip(M) 
    sdes = fk(sdes,k1)
    sdes = sw(sdes)
    sdes = fk(sdes,k2)
    sdes = ip_1(sdes)
    return sdes 

def cbc_mode_enc(M, K, IV):
    y = []
    for i, m in enumerate(M):
        if i == 0:
            y_i1 = IV
        xor_res = xor(m, y_i1)
        y_i1 = sdes(xor_res, K, 'cod')
        y.append(y_i1)
    return y

def cbc_mode_dec(Y, K, IV):
    x = []
    for i, y in enumerate(Y):
        if i == 0:
            y_i1 = IV
        dk = sdes(y, K, 'dec')
        xi = xor(dk, y_i1)
        x.append(xi)
        y_i1 = y
    return x
       
def cbc():
    Y = [[0, 1, 0, 0, 0, 0, 1, 1], [0, 1, 1, 1, 0, 0, 1, 0], [0, 1, 1, 1, 1, 0, 0, 1], 
        [0, 1, 1, 1, 0, 0, 0, 0], [0, 1, 1, 1, 0, 1, 0, 0], [0, 1, 1, 0, 1, 1, 1, 1]]
    Y_error = [[0, 1, 0, 0, 0, 0, 1, 1], [1, 1, 1, 1, 0, 0, 1, 0], [0, 1, 1, 1, 1, 0, 0, 1], 
        [0, 1, 1, 1, 0, 0, 0, 0], [0, 1, 1, 1, 0, 1, 0, 0], [0, 1, 1, 0, 1, 1, 1, 1]]
    K = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
    IV = [1, 0, 0, 0, 1 , 0, 1, 1]
    cbc_y = cbc_mode_dec(Y, K, IV)
    cbc_error_y = cbc_mode_dec(Y_error, K, IV)
    for i in range(len(cbc_y)):
        if cbc_y[i] != cbc_error_y[i]:
            print("Error at i = ", i+1)
            print("Output R: ", cbc_y[i])
            print("Output E: ", cbc_error_y[i])

def k1_to_k(K1):
    return [K1[0], "a2", K1[5], K1[3], "a1", K1[7], K1[1], K1[4], K1[2], K1[6]]

def k2_to_k(K2):
    return [K2[7], K2[3], K2[1], "a2", K2[5], K2[2], "a1", K2[0], K2[6], K2[4]]

def k_testing():
    S0_1 = [[0,1,0,0], [0,0,0,1], [1,1,1,0], [1,0,0,1]]
    S1_1 = [[0,1,1,0], [0,1,1,1], [1,0,0,0], [1,1,1,1]]
    R0 = [1,1,1,0,1,0,1,1]
    K1 = [prod for prod in itertools.product(S0_1, S1_1)]
    K1 = [x+y for (x,y) in K1]

    S0_2 = [[0,0,0,0], [0,1,0,1], [1,1,0,0], [1,0,1,1]]
    S1_2 = [[0,1,1,0], [0,1,1,1], [1,0,0,0], [1,1,1,1]]
    R1 = [0,1,0,1,0,1,0,1]
    K2 = [prod for prod in itertools.product(S0_2, S1_2)]
    K2 = [x+y for (x,y) in K2]

    print(K1)
    print()
    print("k1 to k: ")
    print(k1_to_k(K1))
    print()
    print(K2)
    print()
    print("k2 to k: ")
    print(k2_to_k(K2))

def brute_force():
    x = [1, 0, 0, 1, 0, 1, 1, 1]
    y = [1, 0, 1, 1, 1, 0, 0, 0]
    keys = [[int(c) for c in "".join(seq)] for seq in itertools.product("01", repeat=10)]
    K = []
    for key in keys:
        y_test = sdes(x, key, 'cod')
        if y == y_test:
            print("Found key: ", key)
            K = key
            break
    print("Finished!")
    

if __name__ == '__main__':	
    #cbc()
    #brute_force()
    k_testing()