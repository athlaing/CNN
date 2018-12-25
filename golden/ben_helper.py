#Python program for bfloat16, a truncated mantissa version of IEEE 754 float32
#

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
				#if positive
				if a[0] == '0':
					if int(self.man,2) == 0:
						self.value = '+inf'
					else:
						self.value = '+NaN'
				#else negative
				else: 
					if int(self.man, 2) == 0:
						self.value = '-inf'
					else:
						self.value = '-NaN'

			if int(a,2) == 0:
				self.value = "zero"
	#end __init___
	
	def bin_parsed(self):
		return self.sign, self.exp, self.man
	#end bin_seperate
	
	def bin(self):
		return self.sign + self.exp + self.man
	#end bin

	def mag(self):
		pass #work in progress
	#end mag
#end class				
			

#----------------------------------------------------------------------------------------------
#add_bin: compressor adder the multiplier's partial sums
#	inputs: (a, b) unsigned binary strings with same lengths
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

	#A ripple carry adder; a and b should be the same lengths.
	for i in range(len(a)-1, -1, -1): 
		#a1, b1 to make the code look cleaner
		a1 = int(a[i])					
		b1 = int(b[i])
		#Full-adder expressions. The Cout from previous stage becomes Cin of the new stage.
		add_sum = str(a1^ b1 ^ Cin) + add_sum
		Cin = (a1 & b1) ^ (Cin & (a1 ^ b1))

	#returns the the sum and the carry-out
	return str(Cin) + add_sum


#----------------------------------------------------------------------------------------------

#mult_bfloat16:
#	input: (a, b) two 16bit binary string in Bfloat16 format, where a[0], b[0] are the MSBs
#	output: (mult_out) 16bit binary string in Bfloat16 format, where mult_out[0] is the
def mult_bfloat16(a, b):
	#
	#Edge cases: +-Inf, +-NaN, Zero
	#
	
	o_sign = int(a.sign) ^ int(b.sign)
	o_sign = bin(o_sign)[2:]
	o_exp = (int(a.exp,2) - 127)  + (int(b.exp,2) - 127)

	#Add the implicit 1 in front of mantissa. See Bfloat16 format.
	a_man = ('1' + a.man)			
	b_man=  ('1' + b.man)

	#Calculate the partial sum of the mantissa
	o_man = ''
	for i in range(len(b_man) - 1, -1, -1):
		if(b_man[i] ==  '1'):
			o_man = add_bin(o_man, bin( int(a_man,2) << (7 - i))[2:])
	
	#alternatively, 
	#o_man = int(a_man,2) * int(b_man,2)
		
	#Normalize output mantissa, adding the extra exponents, and add the bias
	o_exp += len(o_man) - (14) - (1)
	o_exp += 127
	o_exp = bin(o_exp)[2:].rjust(8, '0')

	#Truncate partial sum
	o_man = o_man[1:8].ljust(7, '0')

	#concentate sign,exponent,mantissa into one string
	mult_out = bfloat(o_sign + o_exp + o_man)
	return mult_out

#---------------------------------------------------------------------------------------------


a = bfloat('0100000000100011')
b = bfloat('1100000101110110')
#result should be 11000010011100
print(mult_bfloat16(a , b).bin_parsed())

