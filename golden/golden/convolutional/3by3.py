import sys
sys.path.append("../../")

from golden.basic_logic import addmult_v2 as alu

class kernel:
    def __init__(self, weights):
        
        self.weights = weights
        self.mult = alu.bfloat_mult
        self.add  = alu.bfloat_add
        self.pp   = []
        self.out  = [0,0,0,0,0,0,0]
    
    def dot(self, img):
        
        for i in range(9):
            self.pp.append(self.mult(self.weights[i],img[i]))
        self.out[0] = self.add(self.pp[0], self.pp[1])
        self.out[1] = self.add(self.pp[2], self.pp[3])
        self.out[2] = self.add(self.pp[4], self.pp[5])
        self.out[3] = self.add(self.pp[6], self.pp[7])
        self.out[4] = self.add(self.out[0], self.out[1])
        self.out[5] = self.add(self.out[2], self.out[3])
        self.out[6] = self.add(self.out[5], self.pp[8])
        
        return self.out[6]
    
    def display_tree(self, form="dec"):
        
        if (form == "bin"):
            elements = [x.display_bin() for x in self.out]
        elif (form == "dec"):
            elements = [x.display_dec() for x in self.out]
        else:
            print("ERROR: choose <bin> or <dec>")
            
        print ("="*15+" Add tree "+"="*15)            
        print (elements)
        print (elements[0],elements[1],elements[2],elements[3])
        print (elements[4],elements[5])
        print (elements[6])        
        print ("="*40)
        
#============================== DEBUG TEST ====================================
import random
import itertools
from datetime import datetime
random.seed(datetime.now())

a_list = list(itertools.product([0,1], repeat=16))
b_list = list(itertools.product([0,1], repeat=16))

random.shuffle(a_list)
random.shuffle(b_list)

weights = [''.join([str(x) for x in a]) for a in a_list[0:9]]
weights = [alu.bfloat(str(a[0]),str(a[1:9]),str(a[9:])) for a in weights]
img     = [''.join([str(x) for x in b]) for b in b_list[0:9]]
img     = [alu.bfloat(str(b[0]),str(b[1:9]),str(b[9:])) for b in img]

test_kernel = kernel(weights)
test_kernel.dot(img)
test_kernel.display_tree()
#========================== END DEBUG TEST ====================================