
# coding: utf-8

# In[215]:


class Bfloat:
    def __init__(self, sign, exp, man):
        self.sign = [int(sign)]
        exp_container = []
        man_container = []
        for e in exp:
            exp_container.append(int(e))
        if len(exp_container) != 8:
            print("Error: len(exp) != 8")
        self.exp = exp_container
        for m in man:
            man_container.append(int(m))
        self.man = man_container
        if len(man_container) != 7:
            print("Error: len(man) != 7")
    def print_bin(self):
        print(self.sign, self.exp, self.man)
    def print(self):
        man_magnitude = 0.0
        exp_magnitude = sum(self.exp[i] * 2**(7-i) for i in range(0,8))
        start = -1
        for m in self.man:
            man_magnitude = man_magnitude + m * 2**(start)
            start = start - 1
        if self.exp == [0, 0, 0, 0, 0, 0, 0, 0]:
            if self.man == [0, 0, 0, 0, 0, 0, 0]:
                print(0.0)
            else:
                
                print((-1)**self.sign[0] * 2**(-126) * man_magnitude)
        elif self.exp == [1, 1, 1, 1, 1, 1, 1, 1]:
            print(float('Inf'))
            
        else:
            print((-1)**self.sign[0] * 2**(exp_magnitude - 127) * (man_magnitude + 1))


# In[216]:


def magnitude(a):
    if(a.exp == [0, 0, 0, 0, 0, 0, 0, 0] or a.exp == [1, 1, 1, 1, 1, 1, 1, 1]):
        man = sum(a.man[i] * 2**(6-i) for i in range(0,7))
        exp = sum(a.exp[i] * 2**(7-i) for i in range(0,8)) - 127
        return exp, man
    else:
        man = sum(a.man[i] * 2**(6-i) for i in range(0,7)) + 128
        exp = sum(a.exp[i] * 2**(7-i) for i in range(0,8)) - 127
        return exp, man


# In[217]:


def bfloat_mult(a, b):
    o_sign = a.sign[0] ^ b.sign[0]
    a_exp, a_man = magnitude(a)
    b_exp, b_man = magnitude(b)
    o_man_mag = a_man * b_man
    o_man = [int(x) for x in bin(o_man_mag)[2:]]
    whole = len(o_man) - 14
    o_exp_mag = a_exp + b_exp + (whole - 1) + 127
    o_exp = [int(x) for x in bin(o_exp_mag)[2:]]
    if len(o_exp) < 8:
        diff = 8 - len(o_expo)
        extra = [int(x)*0 for x in range(0, diff)]
        o_exp = extra + o_exp
    if len(o_man) > 8:
        o_man = o_man[1:8]
    else:
        o_man = o_man[1:]
        diff = 7 - len(o_man)
        extra = [int(x)*0 for x in range(0, diff)]
        o_man = o_man + extra   
    o = Bfloat(o_sign, o_exp, o_man)
    return o


# In[218]:


a = Bfloat("0", "10000000", "0100011")
b = Bfloat("1", "10000010", "1110110")
c = bfloat_mult(a, b)
c.print()
c.print_bin()

