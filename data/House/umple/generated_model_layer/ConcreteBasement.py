# %% NEW FILE ConcreteBasement BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8183.32a6408a9 modeling language!
# line 2 "model.ump"
# line 76 "model.ump"
from .Basement import Basement

class ConcreteBasement(Basement):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #ConcreteBasement Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aSize, aName, aHouse, aQuality):
        self._Quality = None
        super().__init__(aSize, aName, aHouse)
        self._Quality = aQuality

    #------------------------
    # INTERFACE
    #------------------------
    def setQuality(self, aQuality):
        wasSet = False
        self._Quality = aQuality
        wasSet = True
        return wasSet

    def getQuality(self):
        return self._Quality

    def delete(self):
        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "Quality" + ":" + str(self.getQuality()) + "]"
