#Python program for bfloat16, a truncated mantissa version of IEEE 754 float32

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
		return self.sign, self.exp, self.man
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
				return ((-1)**int(self.sign) * 2**(exp_mag - 126) * (man_mag)) 
		elif self.value == 'inf':
			return float('Inf')
		else:
			return ((-1)**int(self.sign) * 2**(exp_mag - 127) * (man_mag + 1))
	#end mag
#end class
#----------------------------------------------------------------------------------------------

#mult_bfloat16:
#   input: (a, b) two 16bit binary string in Bfloat16 format, where a[0], b[0] are the MSBs
#   output: (mult_out) 16bit binary string in Bfloat16 format, where mult_out[0] is the
def bfloat_mult(a, b):

	#output sign
	o_sign = int(a.sign) ^ int(b.sign)
	o_sign = bin(o_sign)[2:]

	#Edge cases for +-Inf, +-NaN, +-Zero
	#Order of precedence: NaN -> Zero -> Inf
	if a.value == 'NaN' or b.value == 'NaN':
		return bfloat(o_sign, '11111111', '0000001')

	if a.value == 'zero' or b.value == 'zero':
		return bfloat(o_sign, '00000000', '0000000')

	if a.value == 'inf' or b.value == 'inf':
		return bfloat(o_sign, '11111111', '0000000')

	#Substrate the bias and add the exponents.
	if int(a.exp,2) > 0:
		o_exp = (int(a.exp,2) - 127)  + (int(b.exp,2) - 127)
	else:
		o_exp = (int(a.exp,2) - 126)  + (int(b.exp,2) - 126)


	#normalize
	a_man = a.man
	b_man = a.man
	if int(a.exp,2) > 0:
	   a_man = ('1' + a.man)
	if int(b.exp,2) > 0:
	   b_man=  ('1' + b.man)

	o_man = int(a_man,2) * int(b_man,2)
	o_man = bin(o_man)[2:]

	#Normalize output mantissa, adding the extra exponents, and add the bias
	o_exp += len(o_man) - (14) - (1)
	o_exp += 127

	if o_exp < 0: 
		o_exp = 0

	if o_exp > 255:  #if o_exp > '1111_1111'
		o_exp = 255

	o_exp = bin(o_exp)[2:].rjust(8, '0')
	o_man = o_man[1:8].ljust(7, '0')
	
	return bfloat(o_sign, o_exp, o_man)
# end mult_bfloat()----------------------------------------------------------------------------

a = bfloat('0', '00000001', '1000100')
print(a.display_dec())

print(mult_bfloat16(a, a).display_dec())
print(a.display_dec() * a.display_dec())

