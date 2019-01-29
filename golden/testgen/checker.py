import sys
import argparse

parser = argparse.ArgumentParser(description='Checks if the outputs verilog adder/mult matches with reference')
parser.add_argument("-w","--write", help="Enable write to file. Default is false", default=False)
parser.add_argument("-a","--adder", help="Enable adder reference check. Default is True", default=True)
parser.add_argument("-m","--mult", help="Enable mult reference check. Default is True", default=False)

args = vars(parser.parse_args())
write2file = args["write"] == "True"
add = args["adder"] == "True"
mult = args["mult"] == "True"


if(mult):
	fvt_mult = open("mult_out.csv", "r")
	fref_mult = open("mult_ref.csv", "r")
	if write2file : 
		fdiff_mult = open("diff_mult.txt", 'w')

	lvt = fvt_mult.readlines()
	lref = fref_mult.readlines()
	error = 0
	errorContent = []

	if fvt_mult == None or fref_mult == None:
		print("FATAL: ERROR: No require files are in the directory.")
		sys.exit()
	if len(lvt) != len(lref):
		print("ERROR: Mult_out and mult_ref aren't the same length.")
	else:
		for i in range(len(lvt)):
			if lvt[i] != lref[i]:
				error += 1
				errorContent.append("Mismatch at Line " + str(i + 1) + 
					":\n" + "mult_out: " + lvt[i] + "mult_ref: " + lref[i])

	print("Total Number of mismatches: " + str(error))
	if write2file:
		fdiff_mult.write("Total Number of mismatches: " + str(error) + '\n')
	for e in errorContent:
		print(e)
		if write2file:
			fdiff_mult.write(e)

	fvt_mult.close()
	fref_mult.close()
	if write2file:
		fdiff_mult.close()


if(add):
	fvt_add = open("add_out.csv", "r")
	fref_add = open("add_ref.csv", "r")
	if write2file : 
		fdiff_add = open("diff_add.txt", 'w')

	lvt = fvt_add.readlines()
	lref = fref_add.readlines()
	error = 0
	errorContent = []

	if fvt_add == None or fref_add == None:
		print("FATAL: ERROR: No require files are in the directory.")
		sys.exit()
	if len(lvt) != len(lref):
		print("ERROR: Mult_out and mult_ref aren't the same length.")
	else:
		for i in range(len(lvt)):
			if lvt[i] != lref[i]:
				error += 1
				errorContent.append("Mismatch at Line " + str(i + 1) + 
					":\n" + "mult_out: " + lvt[i] + "mult_ref: " + lref[i])

	print("Total Number of mismatches: " + str(error))
	if write2file:
		fdiff_add.write("Total Number of mismatches: " + str(error) + '\n')
	for e in errorContent:
		print(e)
		if write2file:
			fdiff_add.write(e)

	fvt_add.close()
	fref_add.close()
	if write2file:
		fdiff_add.close()


