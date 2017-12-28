def p10(ent):
    bits = []
    for i in  [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]:
       bits.append(ent[i-1])  
    return bits

def p8(ent):
    bits = []
    for i in  [6, 3, 7, 4, 8, 5, 10, 9]:
       bits.append(ent[i-1])        
    return bits
           
def shift(ent, cant=1):
    new = ent[:5]
    old = ent[5:]
    for i in range(cant):
        new.insert(5,new.pop(0)) 
        old.insert(5,old.pop(0))
    return new + old
    
def keys(K):
    k1 = p8(shift(p10(K)))
    k2 =  p8(shift(p10(K),3))
    return k1,k2


        
