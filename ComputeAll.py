import os
from optparse import OptionParser

def main(nb):
	
	GPAs = [['H2020-EU.3'], ['H2020-EU.1.3.1'], ['H2020-EU.3.1'], ['H2020-EU.3.2'],  ['H2020-EU.3.3'],  ['H2020-EU.3.4'], ['H2020-EU.3.5'], ['H2020-EU.3.6'], ['H2020-EU.3.7']]

	for gpa in GPAs:
		os.system("echo 'using gpa = "+gpa[0]+ " and "+ str(nb) +" countries' >> Results/"+ gpa[0]+"_"+str(nb)+".txt")
		os.system("python3 DatabaseFiller.py " + gpa[0] + " "+str(nb) + " >> Results/"+ gpa[0]+"_"+str(nb)+".txt")
		os.system("python3 Shapley.py >> Results/"+ gpa[0]+"_"+str(nb)+".txt")


if __name__ == "__main__":
	parser = OptionParser("Usage: Python3 ComputeAllParallel.py <nb of countries>")
	(options, args) = parser.parse_args()

	if len(args) == 1 :	

		try :
			main(int(args[0]))
		except ValueError:
			print("You must use integers.")

	else:
		print("Usage: Python3 ComputeAll.py <nb of countries>")
