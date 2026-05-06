# %% NEW FILE SemiDetached BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8183.32a6408a9 modeling language!
# line 18 "model.ump"
# line 91 "model.ump"
from abc import ABC, abstractmethod
from .House import House

class SemiDetached(ABC, House):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #SemiDetached Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aAddress, aBuildingMaterial, aGarden, aWindows):
        self._Windows = None
        self._Garden = None
        super().__init__(aAddress, aBuildingMaterial)
        self._Garden = aGarden
        self._Windows = aWindows

    #------------------------
    # INTERFACE
    #------------------------
    def setGarden(self, aGarden):
        wasSet = False
        self._Garden = aGarden
        wasSet = True
        return wasSet

    def setWindows(self, aWindows):
        wasSet = False
        self._Windows = aWindows
        wasSet = True
        return wasSet

    def getGarden(self):
        return self._Garden

    def getWindows(self):
        return self._Windows

    # Code from template attribute_IsBoolean 
    def isGarden(self):
        return self._Garden

    def delete(self):
        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "Garden" + ":" + str(self.getGarden()) + "," + "Windows" + ":" + str(self.getWindows()) + "]"
