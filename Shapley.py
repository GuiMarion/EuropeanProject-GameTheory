import pickle 
from Project import *
from optparse import OptionParser
from tqdm import tqdm
import time


DataBaseName = "DataBase"
No0Coalition = True


def printBase(DataBase):
	for elem in DataBase:
		print(elem)

def fact(n):
    """fact(n): calcule la factorielle de n (entier >= 0)"""

    if n < 0:
    	raise ValueError("n must be >= 0", n)
    x=1
    for i in range(2,n+1):
        x*=i
    return x

def load(name):
	 return pickle.load( open( name, "rb" ) )

def listCountries(DataBase):
	countrieslist = []
	for project in DataBase:
		for country in project.countries:
			if country not in countrieslist:
				countrieslist.append(country)
	return countrieslist

def partiesliste(seq):
	# retuns all subsets possibles from seq

    i, imax = 0, 2**len(seq)-1
    LEN = 2**(len(seq))
    p = [None] * LEN
    indice = 0
    with tqdm(total=LEN) as progress:    
        while i <= imax:
            s = []
            j, jmax = 0, len(seq)-1
            while j <= jmax:
                if (i>>j)&1 == 1:
                    s.append(seq[j])
                j += 1
            p[indice] = s
            indice += 1
            progress.update(1)
            i += 1 
    del p[0]
    return p

def partieslisteWithoutPrint(seq):
	# retuns all subsets possibles from seq

    p = []
    i, imax = 0, 2**len(seq)-1
    while i <= imax:
        s = []
        j, jmax = 0, len(seq)-1
        while j <= jmax:
            if (i>>j)&1 == 1:
                s.append(seq[j])
            j += 1
        p.append(s)
        i += 1 
    del p[0]
    return p


def subsetof(A, B):
	# returns if A is a subset of B
	for elem in A:
		if elem not in B:
			return False
	return True

def Fill(DataBase): # Fille each countries with the mean of the buget of the projects involved in
	
	parties = partiesliste(listCountries(DataBase))

	dico = {str(c) : 0 for c in parties}

	with tqdm(total=len(parties)) as progress: 	
		for coalition in parties:
			for project in DataBase:
				if len(coalition) == len(project.countries) and subsetof(coalition, project.countries):
					dico[str(coalition)] += project.buget
					
			if len(coalition) > 1 :
				for country in coalition:
					try:
						dico[str(coalition)] += dico[str([country])]
					except KeyError:
						print(country)
						print(dico)
						raise KeyError("Ordering parties problem")

			progress.update(1)
	return dico

def FillWithoutPrint(DataBase): # Fille each countries with the mean of the buget of the projects involved in

	parties = partieslisteWithoutPrint(listCountries(DataBase))

	dico = {str(c) : 0 for c in parties}

	for coalition in parties:
		dico[str(coalition)] = 0
		for project in DataBase:
			if len(coalition) == len(project.countries) and subsetof(coalition, project.countries):
				dico[str(coalition)] += project.buget
				
		if len(coalition) > 1 :
			for country in coalition:
				try:
					dico[str(coalition)] += dico[str([country])]
				except KeyError:
					print(country)
					print(dico)
					raise KeyError("Ordering parties problem")
	return dico

def S(n, Z):
	# Return the first term of shapley value
	return (fact(n - len(Z)) * fact(len(Z) -1))/fact(n)

def depof(L, e):
	# return the set L deprived of e
	L2 = []
	for elem in L:
		if elem != e:
			L2.append(elem)
	return L2

def toList(L):
	# retun L given str(L)

	L = L.replace("[", "")
	L = L.replace("]", "")
	L = L.replace(" ", "")
	L = L.replace("'", "")

	L = L.split(",")

	return L


def Shapley(DataBase):

	# Fill the shapley value for every country
	shapley = {}
	v = Fill(DataBase)
	countries = listCountries(DataBase)
	n = len(countries)

	with tqdm(total=len(countries)) as progress: 	
		for country in countries:
			temp = 0
			for Z in v:
				if country in toList(Z) and len(toList(Z)) > 1:
					if No0Coalition == False:
						temp += S(n, toList(Z)) * (v[Z] - v[str(depof(toList(Z), country))])
					elif v[Z] > 0:
						temp += S(n, toList(Z)) * (v[Z] - v[str(depof(toList(Z), country))])

			shapley[country] = temp
			progress.update(1)

	return shapley


def ShapleyWithoutPrint(DataBase):

	# Fill the shapley value for every country
	shapley = {}
	v = FillWithoutPrint(DataBase)
	countries = listCountries(DataBase)
	n = len(countries)

	for country in countries:
		temp = 0
		for Z in v:
			if country in toList(Z) and len(toList(Z)) > 1:
				if No0Coalition == False:
					temp += S(n, toList(Z)) * (v[Z] - v[str(depof(toList(Z), country))])
				elif v[Z] > 0:
					temp += S(n, toList(Z)) * (v[Z] - v[str(depof(toList(Z), country))])
		shapley[country] = temp

	return shapley


def ShapleyTest():
	# Test with an example from the french wikipedia page for shapley value
	# should be 20, 20, 80, so it works ! 
	shapley = {}
	v = {"['1', '2', '3']" : 120, "['1', '2']" : 0, "['1', '3']" : 120, "['2', '3']" : 120, "['1']" : 0, "['2']" : 0, "['3']" : 0}
	countries = ['1','2','3']
	n = len(countries)

	for country in countries:
		temp = 0
		for Z in v:
			if country in toList(Z) and len(toList(Z)) > 1:
				if No0Coalition == False:
					temp += S(n, toList(Z)) * (v[Z] - v[str(depof(toList(Z), country))])
				elif v[Z] > 0:
					temp += S(n, toList(Z)) * (v[Z] - v[str(depof(toList(Z), country))])
		shapley[country] = temp

	return shapley

def set0coalitionFalse():
	global No0Coalition
	No0Coalition = False

def main():

	DataBase = load(DataBaseName)
	#printBase(DataBase)
	#print("Database succefully loaded.")
	#print(ShapleyTest())
	print(Shapley(DataBase))




if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-a", "--allow0", action="store_true", dest="allow", help="Allow coalitions with value 0", metavar="allow0coalittion")
	(options, args) = parser.parse_args()

	if options.allow is not None:
		set0coalitionFalse()
	if len(args) == 0 :	


		print("				Shapley Value")	
		print()
		deb = time.clock()
		main()
		print("Computation Time :", abs(time.clock() - deb), "seconds")

	else:
		print("Usage: Python3 Shapley.py (-a to take account of coalition with value of 0)")


