# %% NEW FILE EarthBasement BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8183.32a6408a9 modeling language!
# line 13 "model.ump"
# line 86 "model.ump"
from .Basement import Basement

class EarthBasement(Basement):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #EarthBasement Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aSize, aName, aHouse, aHumidity):
        self._Humidity = None
        super().__init__(aSize, aName, aHouse)
        self._Humidity = aHumidity

    #------------------------
    # INTERFACE
    #------------------------
    def setHumidity(self, aHumidity):
        wasSet = False
        self._Humidity = aHumidity
        wasSet = True
        return wasSet

    def getHumidity(self):
        return self._Humidity

    def delete(self):
        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "Humidity" + ":" + str(self.getHumidity()) + "]"