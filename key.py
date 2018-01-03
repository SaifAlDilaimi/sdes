def p10(input):
    bits = []
    for i in  [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]:
       bits.append(input[i-1])  
    return bits

def p8(input):
    bits = []
    for i in  [6, 3, 7, 4, 8, 5, 10, 9]:
       bits.append(input[i-1])        
    return bits
           
def shift(input, size=1):
    new = input[:5]
    old = input[5:]
    for i in range(size):
        new.insert(5,new.pop(0)) 
        old.insert(5,old.pop(0))
    return new + old
    
def keys(K):
    k1 = p8(shift(p10(K)))
    k2 =  p8(shift(p10(K),3))
    return k1,k2