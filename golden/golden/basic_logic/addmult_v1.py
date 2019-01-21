
# coding: utf-8

# In[215]:


class bfloat:
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

    def display_bin(self):
         retlist = (''.join([str(x) for x in self.sign]),
                    ''.join([str(x) for x in self.exp]),
                    ''.join([str(x) for x in self.man]))
         return retlist

    def display_dec(self):
        man_magnitude = 0.0
        exp_magnitude = sum(self.exp[i] * 2**(7-i) for i in range(0,8))
        start = -1
        for m in self.man:
            man_magnitude = man_magnitude + m * 2**(start)
            start = start - 1
        if self.exp == [0, 0, 0, 0, 0, 0, 0, 0]:
            if self.man == [0, 0, 0, 0, 0, 0, 0]:
                return 0.0
            else:
                return (-1)**self.sign[0] * 2**(-126) * man_magnitude
        elif self.exp == [1, 1, 1, 1, 1, 1, 1, 1]:
            return float('Inf')

        else:
            return (-1)**self.sign[0] * 2**(exp_magnitude - 127) * (man_magnitude + 1)


# In[216]:


def magnitude(a):
    if(a.exp == [0, 0, 0, 0, 0, 0, 0, 0] or a.exp == [1, 1, 1, 1, 1, 1, 1, 1]):
        man = sum(a.man[i] * 2**(6-i) for i in range(0,7)) + 128
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
    if o_exp_mag < 0:
        o_exp_mag = o_exp_mag + 127
    o_exp = [int(x) for x in bin(o_exp_mag)[2:]]
    if len(o_exp) < 8:
        diff = 8 - len(o_exp)
        extra = [int(x)*0 for x in range(0, diff)]
        o_exp = extra + o_exp
    elif len(o_exp) > 8:
        o_exp = [int(x)*0 for x in range (0, 8)]
    if len(o_man) > 8:
        o_man = o_man[1:8]
    else:
        o_man = o_man[1:]
        diff = 7 - len(o_man)
        extra = [int(x)*0 for x in range(0, diff)]
        o_man = o_man + extra
    o = bfloat(o_sign, o_exp, o_man)
    return o


# In[218]:
def bfloat_add(a, b):
    if a.exp == "11111111":
        return a
    elif b.exp == "11111111":
        return b
    elif (a.exp == "00000000" and a.man == "0000000") and (b.exp == "00000000" and b.man == "0000000"):
        return bfloat("0","00000000", "0000000")
    elif (a.exp == "00000000" and a.man == "0000000") and not(b.exp == "00000000" and b.man == "0000000"):
        return b
    elif not(a.exp == "00000000" and a.man == "0000000") and (b.exp == "00000000" and b.man == "0000000"):
        return a
    if(a.exp == "00000000" and a.man != "0000000"):
        a_man = "0" + a.man
        a_exp = -126
    else:
        a_man = "1" + a.man
        a_exp = int(a.exp, 2) -127
    if(b.exp == "00000000" and b.man != "0000000"):
        b_man = "0" + b.man
        b_exp = -126
    else:
        b_man = "1" + b.man
        b_exp = int(b.exp, 2) - 127
    diff = int(a.exp, 2) - int(b.exp, 2)
    print(diff)
    if(diff > 0):
        b_man = int(b_man, 2) >> diff
        a_man = int(a_man, 2)
        b_exp = a_exp
    elif(diff < 0):
        a_man = int(a_man, 2) >> (-diff)
        print(a_man)
        b_man = int(b_man, 2)
        a_exp = b_exp
    if(a.sign == b.sign): 
        out_man = a_man + b_man
    elif(a.sign == "1" and b.sign == "0"):
        out_man = b_man - a_man
    elif(a.sign == "0" and b.sign == "1"):
        out_man = a_man - b_man
    print(out_man)
    if len(bin(out_man)[2:]) > 8:
        shift_amt = len(bin(out_man)[2:]) - 8
        out_man = out_man >> shift_amt
        out_exp = a_exp + shift_amt + 127
    elif len(bin(out_man)[2:]) < 8:
        shift_amt = 8 - len(bin(out_man)[2:])
        out_man = out_man << shift_amt
        out_exp = a_exp - shift_amt + 127
    else:
        out_exp = a_exp + 127
    out_exp = bin(out_exp)[2:]
    if len(out_exp) < 8:
        exp_fill = 8 - len(out_exp)
        for i in range(0, exp_fill):
            out_exp = "0" + out_exp
    if(out_man < 0):
        out_sign = "1"
        out_man = (-1)*out_man
    else:
        out_sign = "0"
    print(bin(out_man))
    return bfloat(out_sign, out_exp, bin(out_man)[3:])



# a = bfloat("0", "10000000", "0100011")
# b = bfloat("1", "10000010", "1110110")
# c = bfloat_mult(a, b)
# c.print()
# c.print_bin()
