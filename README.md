# EuropeanProject-GameTheory
This project implements the Shapley value computation for country coalition in European projets.


This project compute shapley value by country for European research projects. The database contains projects as following : 

			project(name: string, buget: int, countries: list, thematic: string)

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

You can fill the DataBase with DatabaseFiller.py, you will have to add elements to the DataBase liste to append project in the database. Everything was done in order to be very easy to script, you can also do it by adding lines by hand as done in the script.

Please don't forget to lauch the script after changing it : 

			python3 DatabaseFiller.py


# Usage

To get started : 

			python3 Shapley.py


This will print the shapley values for every country without taking into account of coalition with value of 0. If you want to take them into account please use the -a flag. 

			python3 Shapley.py -a