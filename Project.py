class Project:

    def __init__(self, name):
        self.name = None
        self.buget = None
        self.countries = []
        self.thematic = None


    def __init__(self, name, buget, countries, thematic):
        self.name = name # Name of the project
        self.buget = buget # Buget of the project
        self.countries = countries # Coutries working for the project
        self.thematic = thematic # Thematic of the project

    def __str__(self):

        return(str(self.name) + " " +  str(self.buget) + " "+ str(self.countries) + " " + str(self.thematic))