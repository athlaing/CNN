#Python program for bfloat16, a truncated mantissa version of IEEE 754 float32

class bfloat:
	def __init__(self, a):
		if len(a) != 16:
			print("Argument isn't 16bits")
		else:
			self.sign = a[0]
			self.exp = a[1:9]
			self.man  = a[9:]
			self.value = ''

			if self.exp == '11111111':
				if int(self.man,2) == 0:
					self.value = 'inf'
				else:
					self.value = 'NaN'

			if int(a[1:],2) == 0:
				self.value = 'zero'
	#end __init___

	def bin_parsed(self):
		return self.sign, self.exp, self.man
	#end bin_parsed

	def bin(self):
		return self.sign + self.exp + self.man
	#end bin

	def mag(self):
		exp_mag = int(self.exp,2) - 127
		start = -1
		man_mag = 0.0
		for m in self.man:
			man_mag = man_mag + int(m) * 2 ** (start)
			start = start - 1

		if self.value == 'zero':
			return 0.0
		elif self.value == 'inf':
			return float('Inf')
		else:
			return ((-1)**int(self.sign) * 2**exp_mag * (man_mag + 1))
	#end mag
#end class
#----------------------------------------------------------------------------------------------

#add_bin: compressor adder the multiplier's partial sums
#	inputs: (a, b) unsigned binary strings 
#	output: (Cin, add_sum) single binary string
def add_bin(a, b):
	Cin = 0
	add_sum = ''

	#sign extension
	if(len(a) > len(b)):
		#sign extend b
		for i in range(len(a) - len(b)):
			b = '0' + b
	elif(len(b) > len(a)):
		#sign extend a
		for i in range(len(b) - len(a)):
			a = '0' + a

	#A ripple carry adder
	for i in range(len(a)-1, -1, -1):
		a1 = int(a[i])
		b1 = int(b[i])
		add_sum = str(a1^ b1 ^ Cin) + add_sum
		Cin = (a1 & b1) ^ (Cin & (a1 ^ b1))

	return str(Cin) + add_sum
#----------------------------------------------------------------------------------------------

#mult_bfloat16:
#	input: (a, b) two 16bit binary string in Bfloat16 format, where a[0], b[0] are the MSBs
#	output: (mult_out) 16bit binary string in Bfloat16 format, where mult_out[0] is the
def mult_bfloat16(a, b):

	#output sign
	o_sign = int(a.sign) ^ int(b.sign)
	o_sign = bin(o_sign)[2:]

	#Edge cases for +-Inf, +-NaN, +-Zero
	#Order of precedence: NaN -> Zero -> Inf
	if a.value == 'NaN' or b.value == 'NaN':
		return bfloat(o_sign + '111111110000001')

	if a.value == 'zero' or b.value == 'zero':
		return bfloat(o_sign + '000000000000000')

	if a.value == 'inf' or b.value == 'inf':
		return bfloat(o_sign + '111111110000000')

	#Substrate the bias and add the exponents.
	o_exp = (int(a.exp,2) - 127)  + (int(b.exp,2) - 127)

	#Calculate the mantissa
	a_man = ('1' + a.man)
	b_man=  ('1' + b.man)
	o_man = int(a_man,2) * int(b_man,2)
	o_man = bin(o_man)[2:]

	#Normalize output mantissa, adding the extra exponents, and add the bias
	o_exp += len(o_man) - (14) - (1)
	o_exp += 127

	if o_exp < 0: 
		o_exp += 127
	if o_exp > 255:  #if o_exp > '1111_1111'
		o_exp = 255

	o_exp = bin(o_exp)[2:].rjust(8, '0')
	o_man = o_man[1:8].ljust(7, '0')
	
	return bfloat(o_sign + o_exp + o_man)
# end mult_bfloat()----------------------------------------------------------------------------

# a = bfloat('0000000000000001')
# b = bfloat('0000000000000001')

# print(mult_bfloat16(a , b).bin_parsed())


