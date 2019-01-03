import sys
import argparse

parser = argparse.ArgumentParser(description='Use -w or --write to generate a diff file.')
parser.add_argument("-w","--write", help="Enable write to file. Default is false", default=False)
args = vars(parser.parse_args())
write2file = args["write"] == "True"

fvt = open("mult_out.csv", "r")
fref = open("mult_ref.csv", "r")
if write2file : 
	fdiff = open("diff.txt", 'w')

lvt = fvt.readlines()
lref = fref.readlines()
error = 0
errorContent = []

if fvt == None or fref == None:
	print("FATA: ERROR: No require files are in the directory.")
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
	fdiff.write("Total Number of mismatches: " + str(error) + '\n')
for e in errorContent:
	print(e)
	if write2file:
		fdiff.write(e)

fvt.close()
fref.close()
if write2file:
	fdiff.close()


