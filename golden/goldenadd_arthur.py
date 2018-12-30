
# coding: utf-8

# In[77]:


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


# In[15]:


class bfloat:
	def __init__(self, s, e, m):
		if len(s) + len(e) + len(m) != 16:
			print("Argument isn't 16bits")
		else:
			self.sign = s
			self.exp = e
			self.man  = m
			self.value = ''

			if self.exp == '11111111':
				if int(self.man,2) == 0:
					self.value = 'inf'
				else:
					self.value = 'NaN'

			if int(e,2) + int(m,2) == 0:
				self.value = 'zero'
	#end __init___

	def display_bin(self):
		return (self.sign, self.exp, self.man)
	#end bin_parsed

	def display_dec(self):
		exp_mag = int(self.exp,2)
		start = -1
		man_mag = 0.0
		for m in self.man:
			man_mag = man_mag + int(m) * 2 ** (start)
			start = start - 1

		if self.exp == '00000000':
			if self.man == '0000000':
				return 0.0
			else: 
				out = ((-1)**int(self.sign) * 2**(exp_mag - 126) * (man_mag)) 
				return (out)
		elif self.value == 'inf':
			return float('Inf')
		else:
			out = ((-1)**int(self.sign) * 2**(exp_mag - 127) * (man_mag + 1))
			return (out)


# In[52]:


a = bfloat("0", "01111100", "0010100")
print(a.display_dec())
b = bfloat("0", "01111110", "0001000")
print(b.display_dec())


# In[53]:


c = bfloat_add(a,b)
print(c.display_dec())


# In[55]:


a = bfloat("0", "10000010", "0101010")
print(a.display_dec())
b = bfloat("0", "10000100", "0000001")
print(b.display_dec())


# In[78]:


c = bfloat_add(a,b)
print(c.display_dec())

