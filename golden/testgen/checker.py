import sys

fvt = open("mult_out.csv", "r")
fref = open("mult_ref.csv", "r")
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
				": " + lvt[i] + ' '*22 + lref[i])

print("Total Number of mismatches: " + str(error))
for e in errorContent:
	print(e)

fvt.close()
fref.close()


