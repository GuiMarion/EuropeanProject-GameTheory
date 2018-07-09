from DatabaseFiller import *
from Shapley import *
from threading import Thread


def writeCountries(DataBase, file):

	Countries = {}

	for project in DataBase:
		for country in project.countries:
			if country in Countries:
				Countries[country] += 1
			else :
				Countries[country] = 1

	sorted_by_value = sorted(Countries.items(), reverse=True,  key=lambda kv: kv[1])

	for i in range(len(sorted_by_value)):
		file.write(str(i+1) + " : " + str(sorted_by_value[i][0]) + " -> " + str(sorted_by_value[i][1]) + "\n")

def compute(gpa, nb):

	print("Start:", str(gpa))

	file = open("Results/"+str(gpa)+".txt",'w')
	DataBase = getDatabase(gpa, nb)
	file.write("				Country List (nb of projects) \n \n")
	writeCountries(DataBase, file)
	file.write("\n \n")
	file.write("				 Shapley Values\n \n")
	Values = Shapley(DataBase)
	sorted_by_value = sorted(Values.items(), reverse=True,  key=lambda kv: kv[1])
	for i in range(len(sorted_by_value)):
		file.write(str(i+1) + " : " + str(sorted_by_value[i][0]) + " -> " + str(sorted_by_value[i][1]) + "\n")


	file.close()

	print("End:", str(gpa))

def main2(nb):
	
	GPAs = [[], ['H2020-EU.3'], ['H2020-EU.1.3.1'], ['H2020-EU.3.1'], ['H2020-EU.3.2'],  ['H2020-EU.3.3'],  ['H2020-EU.3.4'], ['H2020-EU.3.5'], ['H2020-EU.3.6'], ['H2020-EU.3.7']]

	for elem in GPAs:
		compute(elem,nb)

def main(nb):

	GPAs = [[], ['H2020-EU.3'], ['H2020-EU.1.3.1'], ['H2020-EU.3.1'], ['H2020-EU.3.2'],  ['H2020-EU.3.3'],  ['H2020-EU.3.4'], ['H2020-EU.3.5'], ['H2020-EU.3.6'], ['H2020-EU.3.7']]

	for i in range(0, len(GPAs), 3):
		t1 = Thread(target=compute, args=(GPAs[i],nb,))
		t1.start()

		if i +1 < len(GPAs):
			t2 = Thread(target=compute, args=(GPAs[i+1],nb,))
			t2.start()

		if i +2 < len(GPAs):
			t3 = Thread(target=compute, args=(GPAs[i+2],nb,))
			t3.start()

		t1.join()
		t2.join()
		t3.join()
main2(27)


