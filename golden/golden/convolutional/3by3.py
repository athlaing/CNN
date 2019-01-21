import sys
sys.path.append("../../")

from golden.basic_logic import addmult_v2 as alu

class kernel:
    def __init__(self, weights):

        self.weights = weights
        self.mult = alu.bfloat_mult
        self.add  = alu.bfloat_add
        self.pp   = []
        self.out  = [0,0,0,0,0,0,0,0]

    def dot(self, img):
        self.img = img
        for i in range(9):
            self.pp.append(self.mult(self.weights[i],img[i]))

        self.out[0] = self.add(self.pp[0], self.pp[1])
        self.out[1] = self.add(self.pp[2], self.pp[3])
        self.out[2] = self.add(self.pp[4], self.pp[5])
        self.out[3] = self.add(self.pp[6], self.pp[7])
        self.out[4] = self.add(self.out[0], self.out[1])
        self.out[5] = self.add(self.out[2], self.out[3])
        self.out[6] = self.add(self.out[4], self.out[5])
        self.out[7] = self.add(self.out[6], self.pp[8])

        return self.out[6]

    def display_tree(self, form="dec"):

        out = None
        pp = None
        w = None
        i = None

        if (form == "bin"):
            pp  = [x.display_bin() for x in self.pp]
            out = [x.display_bin() for x in self.out]
            w   = [x.display_bin() for x in self.weights]
            i   = [x.display_bin() for x in self.img]
        elif (form == "dec"):
            pp = [x.display_dec() for x in self.pp]
            out = [x.display_dec() for x in self.out]
            w   = [x.display_dec() for x in self.weights]
            i   = [x.display_dec() for x in self.img]
        else:
            print("ERROR: choose <bin> or <dec>")
            
        print ("="*15+" Multiply "+"="*15)
        print (str(w[0]) + ' * ' + str(i[0]) + ' = ' + str(pp[0]))
        print (str(w[1]) + ' * ' + str(i[1]) + ' = ' + str(pp[1]))
        print (str(w[2]) + ' * ' + str(i[2]) + ' = ' + str(pp[2]))
        print (str(w[3]) + ' * ' + str(i[3]) + ' = ' + str(pp[3]))
        print (str(w[4]) + ' * ' + str(i[4]) + ' = ' + str(pp[4]))
        print (str(w[5]) + ' * ' + str(i[5]) + ' = ' + str(pp[5]))
        print (str(w[6]) + ' * ' + str(i[6]) + ' = ' + str(pp[6]))
        print (str(w[7]) + ' * ' + str(i[7]) + ' = ' + str(pp[7]))
        print (str(w[8]) + ' * ' + str(i[8]) + ' = ' + str(pp[8]))
        print ("="*15+" Add tree "+"="*15)
        print (pp)
        print (out[0],out[1],out[2],out[3], pp[8])
        print (out[4],out[5], pp[8])
        print (out[6], pp[8])
        print (out[7])
        print ("="*40)

#============================== DEBUG TEST ====================================
#init
w  = []
w.append(alu.bfloat("0","00010010","1110101"))
w.append(alu.bfloat("0","00101001","1010111"))
w.append(alu.bfloat("0","10110101","1100110"))
w.append(alu.bfloat("1","01001011","0101011"))
w.append(alu.bfloat("0","10101110","1010110"))
w.append(alu.bfloat("1","01011110","1101010"))
w.append(alu.bfloat("0","10101010","1101010"))
w.append(alu.bfloat("1","11010110","1011101"))
w.append(alu.bfloat("0","11101110","1111011"))
i = []
i.append(alu.bfloat("0","10010101","0111100"))
i.append(alu.bfloat("0","11010101","1010101"))
i.append(alu.bfloat("0","10110101","1101011"))
i.append(alu.bfloat("1","11010110","1010110"))
i.append(alu.bfloat("1","01011010","1110101"))
i.append(alu.bfloat("0","01110101","0111011"))
i.append(alu.bfloat("1","10110101","0111101"))
i.append(alu.bfloat("0","00111010","1000101"))
i.append(alu.bfloat("1","00010100","1011101"))

test_kernel = kernel(w)
test_kernel.dot(i)
test_kernel.display_tree(form='bin')
#========================== END DEBUG TEST ====================================
