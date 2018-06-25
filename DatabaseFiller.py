from Project import *
import pickle 


DataBaseName = "DataBase"


def printBase(DataBase):
	for elem in DataBase:
		print(elem)


DataBase = []

"""
This part is used to fill the database. 
Add a line for evey project. 

"""
# Project(nom, buget, counties, thematic)
DataBase.append(Project("nom", 1000, ["France", "Italy"], "Mathematics"))

DataBase.append(Project("nom2", 999, ["France", "Italy"], "Mathematics"))

DataBase.append(Project("nom2", 10, ["Moldova", "Russia"], "Mathematics"))


printBase(DataBase)

pickle.dump( DataBase, open(DataBaseName, "wb" ) )

print("The database has been saved in the file", DataBaseName)