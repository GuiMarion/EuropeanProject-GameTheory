# EuropeanProject-GameTheory
This project implements the Shapley value computation for country coalition in European projets.


This project compute shapley value by country for European research projects. The database contains projects as following : 

			project(name: string, buget: int, countries: list, thematic: string)

Where project is a class defined in Project.py.

The program will compute the shapley value for every country with the assumption that : 

			v[Z] = buget mean of every project that contain the members of Z

For exemple, if the database is : 

		Project("nom1", 990, ["France", "Italy"], "Mathematics")
		Project("nom2", 10, ["Moldova", "France"], "Mathematics")

The function v will be, 

		v[France, Italy] = 990
		v[France, Moldova] = 10
		v[Italy] = 990
		v[Moldova] = 10
		v[France] = 500

# DataBase 

You can fill the DataBase with DatabaseFiller.py, everything was done in order to be very easy to script, you can also do it by adding lines by hand as done in the script.

Current usage is : 

	Usage: DatabaseFiller.py [options] <gpa to keep> <number of contries to keep>

	Options:
	  -h, --help    show this help message and exit
	  -a, --allow0  Print the number of projects by countries

<gpa to keep> must be a string with the gpa name you want to keep in the database.

As the shapley value exponential in the number of countries (computing the set of all subsets) we want to minimize the number of countries keeping the most projects possibles. So you can specify <number of countries to keep>, this will keep only the N most occurent countries on the final database. This help to have better computing perfomances and good statistical results. 

Base.zip contains all the databse of European Projects, you just have to unzip it: 

						unzip Base.zip

# Usage

To get started (remember to fill the database before): 

			python3 Shapley.py


This will print the shapley values for every country without taking into account of coalition with value of 0. If you want to take them into account please use the -a flag. 

			python3 Shapley.py -a

# Statistics 

You can compute statistics on the database using our scripts.

## ComputeAll.py

You can use ComputeAll.py to compute Shapley values for N countries with all gpas in the database and fill the /Results folder. 

	Usage: Python3 ComputeAll.py <nb of countries>

		Options:
		  -h, --help  show this help message and exit

## ComputeAllParallel.py

You can use ComputeAllParallel.py to compute Shapley values for N countries with all gpas in the database and fill the /Results folder with 3 gpa computations in the same time. Be carefull, with big N you can quickly fill the RAM ! 

	Usage: Python3 ComputeAllParallel.py <nb of countries>

		Options:
		  -h, --help  show this help message and exit





