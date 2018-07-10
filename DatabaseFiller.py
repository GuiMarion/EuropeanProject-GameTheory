from Project import *
import pickle
import os 
import xml.etree.ElementTree as ET
from tqdm import tqdm
from optparse import OptionParser
from sys import stdout



DataBaseName = "DataBase"


def to_int(s):

	if s.find('.') != -1:
		s = s[:s.find('.')]

	s = s.replace(" ", "")

	return int(s)



def look_for_countries(node):
	L = []
	for child in node:
		#print(node.tag)
		if child.tag == "{http://cordis.europa.eu}name":

			return [child.text.replace(" ","")]
		else: 
			L = list(set(L + look_for_countries(child)))
	return L

def look_for_pga(node):
	for child in node:
		if child.tag == "{http://cordis.europa.eu}pga":

			return child.text.replace(" ","")
		else: 
			ret = look_for_pga(child)
			if ret is not None:
				return ret

def Fill_from_xmlfile(filename):

	tree = ET.parse(filename)
	doc = tree.getroot()
	NAME = None
	BUGET = None
	PGA = None
	Countries = []

	for child in doc:

		if child.tag == "{http://cordis.europa.eu}acronym":
			NAME = child.text

		if child.tag == "{http://cordis.europa.eu}ecMaxContribution":
			BUGET = child.text
		
	Countries = (look_for_countries(doc))

	PGA = look_for_pga(doc)

	if NAME is None:
		raise ValueError("The file", filename, "doest have a name of project.")

	if BUGET is None:
		raise ValueError("The file", filename, "doest have a buget.")

	if Countries == []:
		raise ValueError("The file", filename, "doest have any country.")

	if PGA == None:
		return None

	return Project(NAME, to_int(BUGET), Countries, PGA)

def printBase(DataBase):
	for elem in DataBase:
		print(elem)
		print()

def keep_only_certain_countries(DataBase, tokeep):
	OUT = []
	for project in DataBase:
		keep = True
		for country in project.countries:
			if country not in tokeep:
				keep = False
				break
		if keep:
			OUT.append(project)

	return OUT

def keep_only_certain_gpa(DataBase, keep_gpa_with):
	OUT = []
	for project in DataBase:
		keep = False
		for gpa in keep_gpa_with:
			if gpa in project.thematic:
				keep = True
				break
		if keep:
			OUT.append(project)

	return OUT


def Fill_from_directory(dirname, tokeep=None, keep_gpa_with=None):

	print("We are converting your xml databse, wait for a few time please.")
	DataBase = []
	with tqdm(total=len(os.listdir(dirname))) as progress: 	
		for file in os.listdir(dirname):
			if file.endswith(".xml"):
				Proj = Fill_from_xmlfile(dirname + '/' + file)
				if Proj is not None:
					DataBase.append(Proj)
			progress.update(1)

	if tokeep == []:
		tokeep = None

	if keep_gpa_with == []:
		keep_gpa_with = None

	if tokeep:
		DataBase = keep_only_certain_countries(DataBase, tokeep)

	if keep_gpa_with:
		DataBase = keep_only_certain_gpa(DataBase, keep_gpa_with)

	printBase(DataBase)
	print("There is", len(DataBase), "projects in your database.")
	pickle.dump( DataBase, open(DataBaseName, "wb" ) )
	print("The database has been saved in the file", DataBaseName)

def getDatabase(keep_gpa_with, N):

	dirname = "Base"
	
	DataBase = []

	C = 0
	with tqdm(total=len(os.listdir(dirname))) as progress: 	
		for file in os.listdir(dirname):
			if file.endswith(".xml"):
				Proj = Fill_from_xmlfile(dirname + '/' + file)
				if Proj is not None:
					DataBase.append(Proj)
			progress.update(1)

					#stdout.flush()

	if keep_gpa_with == []:
		keep_gpa_with = None		

	if keep_gpa_with:
		DataBase = keep_only_certain_gpa(DataBase, keep_gpa_with)

	Countries = {}

	for project in DataBase:
		for country in project.countries:
			if country in Countries:
				Countries[country] += 1
			else :
				Countries[country] = 1

	sorted_by_value = sorted(Countries.items(), reverse=True,  key=lambda kv: kv[1])

	tokeep = []

	# Keeps only the N most occurent contries
	for i in range(N):
		tokeep.append(sorted_by_value[i][0])


	DataBase = keep_only_certain_countries(DataBase, tokeep)

	return (DataBase, sorted_by_value)



def printCountries(dirname, tokeep = None, keep_gpa_with=None):

	print("We are converting your xml databse, wait for a few time please.")
	DataBase = []
	with tqdm(total=len(os.listdir(dirname))) as progress: 	
		for file in os.listdir(dirname):
			if file.endswith(".xml"):
				Proj = Fill_from_xmlfile(dirname + '/' + file)
				if Proj is not None:
					DataBase.append(Proj)
			progress.update(1)

	if keep_gpa_with == []:
		keep_gpa_with = None

	if tokeep == []:
		tokeep = None

	if tokeep:
		DataBase = keep_only_certain_countries(DataBase, tokeep)

	if keep_gpa_with:
		DataBase = keep_only_certain_gpa(DataBase, keep_gpa_with)

	print("There is", len(DataBase), "projects in your database.")

	Countries = {}

	for project in DataBase:
		for country in project.countries:
			if country in Countries:
				Countries[country] += 1
			else :
				Countries[country] = 1

	sorted_by_value = sorted(Countries.items(), reverse=True,  key=lambda kv: kv[1])

	for i in range(len(sorted_by_value)):
		print(i+1, ":", sorted_by_value[i][0], "->", sorted_by_value[i][1])

def Fill_manually():

	DataBase = []


	"""
	This part is used to fill the database. 
	Add a line for evey project. 

	"""
	# Project(nom, buget, counties, thematic)
	DataBase.append(Project("nom", 1000, ["France", "Italy"], "Mathematics"))

	DataBase.append(Project("nom2", 999, ["France", "Italy"], "Mathematics"))

	DataBase.append(Project("nom2", 10, ["Moldova", "France"], "Mathematics"))

	printBase(DataBase)

	pickle.dump( DataBase, open(DataBaseName, "wb" ) )

	print("The database has been saved in the file", DataBaseName)


if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-a", "--allow0", action="store_true", dest="allow", help="Print the number of projects by countries", metavar="allow0coalittion")
	(options, args) = parser.parse_args()


	'''
	Fill here the cuntries to keep and the gpas to keep

	'''

	#tokeep = ['Austria', 'Belgium', 'Croatia', 'Cyprus', 'CzechRepublic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Israel', 'Italy', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Serbia', 'Spain', 'Sweden', 'Turkey', 'UnitedKingdom']
	#keep_gpa_with = ['H2020-EU.3']

	tokeep = []
	keep_gpa_with = []



	if options.allow is not None:

		printCountries("Base", tokeep, keep_gpa_with)

	elif len(args) == 0 :

		Fill_from_directory("Base", tokeep, keep_gpa_with)

		#Fill_manually()

	elif len(args) == 1:

		gpa = []
		N = int(args[0])

		(DataBase, Countries) = getDatabase(gpa, N)


		print("				Countries by number of projects involved in")
		print()

		for i in range(N):
			print(i+1, ":", Countries[i][0], "->", Countries[i][1])

		print()
		print("________________________________")
		print()

		pickle.dump( DataBase, open(DataBaseName, "wb" ) )

	elif len(args) == 2 : 

		gpa = []

		gpa.append(args[0])
		N = int(args[1])

		(DataBase, Countries) = getDatabase(gpa, N)

		print("				Countries by number of projects involved in")
		print()

		for i in range(N):
			print(i+1, ":", Countries[i][0], "->", Countries[i][1])

		print()
		print("________________________________")
		print()

		pickle.dump( DataBase, open(DataBaseName, "wb" ) )

	else:
		print("Usage: Python3 Shapley.py (-a to take account of coalition with value of 0)")










