# %% NEW FILE SemiDetachedWithCarport BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8183.32a6408a9 modeling language!
# line 38 "model.ump"
# line 106 "model.ump"
from .SemiDetached import SemiDetached

class SemiDetachedWithCarport(SemiDetached):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #SemiDetachedWithCarport Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aAddress, aBuildingMaterial, aGarden, aWindows):
        self._carports = None
        super().__init__(aAddress, aBuildingMaterial, aGarden, aWindows)
        self._carports = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany 
    def getCarport(self, index):
        aCarport = self._carports[index]
        return aCarport

    def getCarports(self):
        newCarports = tuple(self._carports)
        return newCarports

    def numberOfCarports(self):
        number = len(self._carports)
        return number

    def hasCarports(self):
        has = len(self._carports) > 0
        return has

    def indexOfCarport(self, aCarport):
        index = (-1 if not aCarport in self._carports else self._carports.index(aCarport))
        return index

    # Code from template association_IsNumberOfValidMethod 
    def isNumberOfCarportsValid(self):
        isValid = self.numberOfCarports() >= SemiDetachedWithCarport.minimumNumberOfCarports() and self.numberOfCarports() <= SemiDetachedWithCarport.maximumNumberOfCarports()
        return isValid

    # Code from template association_RequiredNumberOfMethod 
    @staticmethod
    def requiredNumberOfCarports():
        return 2

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfCarports():
        return 2

    # Code from template association_MaximumNumberOfMethod 
    @staticmethod
    def maximumNumberOfCarports():
        return 2

    # Code from template association_AddMNToOnlyOne 
    def addCarport1(self, aDoublePort, aFlatRoof):
        from .Carport import Carport
        if self.numberOfCarports() >= SemiDetachedWithCarport.maximumNumberOfCarports() :
            return None
        else :
            return Carport(aDoublePort, aFlatRoof, self)

    def addCarport2(self, aCarport):
        wasAdded = False
        if (aCarport) in self._carports :
            return False
        if self.numberOfCarports() >= SemiDetachedWithCarport.maximumNumberOfCarports() :
            return wasAdded
        existingSemiDetachedWithCarport = aCarport.getSemiDetachedWithCarport()
        isNewSemiDetachedWithCarport = not (existingSemiDetachedWithCarport is None) and not self == existingSemiDetachedWithCarport
        if isNewSemiDetachedWithCarport and existingSemiDetachedWithCarport.numberOfCarports() <= SemiDetachedWithCarport.minimumNumberOfCarports() :
            return wasAdded
        if isNewSemiDetachedWithCarport :
            aCarport.setSemiDetachedWithCarport(self)
        else :
            self._carports.append(aCarport)
        wasAdded = True
        return wasAdded

    def removeCarport(self, aCarport):
        wasRemoved = False
        #Unable to remove aCarport, as it must always have a semiDetachedWithCarport
        if self == aCarport.getSemiDetachedWithCarport() :
            return wasRemoved
        #semiDetachedWithCarport already at minimum (2)
        if self.numberOfCarports() <= SemiDetachedWithCarport.minimumNumberOfCarports() :
            return wasRemoved
        self._carports.remove(aCarport)
        wasRemoved = True
        return wasRemoved

    def delete(self):
        i = len(self._carports)
        while i > 0 :
            aCarport = self._carports[i - 1]
            aCarport.delete()
            i -= 1

        super().delete()

    def addCarport(self, *argv):
        from .Carport import Carport
        if len(argv) == 2 and isinstance(argv[0], bool) and isinstance(argv[1], bool) :
            return self.addCarport1(argv[0], argv[1])
        if len(argv) == 1 and isinstance(argv[0], Carport) :
            return self.addCarport2(argv[0])
        raise TypeError("No method matches provided parameters")
