# %% NEW FILE Guide BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8091.03bcab5b3 modeling language!
# line 34 "model.ump"
# line 116 "model.ump"
from .NamedUser import NamedUser

class Guide(NamedUser):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Guide Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEmail, aPassword, aName, aEmergencyContact, aBikeTourPlus):
        self._bikeTours = None
        self._bikeTourPlus = None
        super().__init__(aEmail, aPassword, aName, aEmergencyContact)
        didAddBikeTourPlus = self.setBikeTourPlus(aBikeTourPlus)
        if not didAddBikeTourPlus :
            raise RuntimeError ("Unable to create guide due to bikeTourPlus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._bikeTours = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne
    def getBikeTourPlus(self):
        return self._bikeTourPlus

    # Code from template association_GetMany
    def getBikeTour(self, index):
        aBikeTour = self._bikeTours[index]
        return aBikeTour

    def getBikeTours(self):
        newBikeTours = tuple(self._bikeTours)
        return newBikeTours

    def numberOfBikeTours(self):
        number = len(self._bikeTours)
        return number

    def hasBikeTours(self):
        has = len(self._bikeTours) > 0
        return has

    def indexOfBikeTour(self, aBikeTour):
        index = (-1 if not aBikeTour in self._bikeTours else self._bikeTours.index(aBikeTour))
        return index

    # Code from template association_SetOneToMany
    def setBikeTourPlus(self, aBikeTourPlus):
        wasSet = False
        if aBikeTourPlus is None :
            return wasSet
        existingBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = aBikeTourPlus
        if not (existingBikeTourPlus is None) and not existingBikeTourPlus == aBikeTourPlus :
            existingBikeTourPlus.removeGuide(self)
        self._bikeTourPlus.addGuide(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfBikeTours():
        return 0

    # Code from template association_AddManyToOne
    def addBikeTour1(self, aId, aStartWeek, aEndWeek, aBikeTourPlus):
        from .BikeTour import BikeTour
        return BikeTour(aId, aStartWeek, aEndWeek, self, aBikeTourPlus)

    def addBikeTour2(self, aBikeTour):
        wasAdded = False
        if (aBikeTour) in self._bikeTours :
            return False
        existingGuide = aBikeTour.getGuide()
        isNewGuide = not (existingGuide is None) and not self == existingGuide
        if isNewGuide :
            aBikeTour.setGuide(self)
        else :
            self._bikeTours.append(aBikeTour)
        wasAdded = True
        return wasAdded

    def removeBikeTour(self, aBikeTour):
        wasRemoved = False
        #Unable to remove aBikeTour, as it must always have a guide
        if not self == aBikeTour.getGuide() :
            self._bikeTours.remove(aBikeTour)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addBikeTourAt(self, aBikeTour, index):
        wasAdded = False
        if self.addBikeTour(aBikeTour) :
            if index < 0 :
                index = 0
            if index > self.numberOfBikeTours() :
                index = self.numberOfBikeTours() - 1
            self._bikeTours.remove(aBikeTour)
            self._bikeTours.insert(index, aBikeTour)
            wasAdded = True
        return wasAdded

    def addOrMoveBikeTourAt(self, aBikeTour, index):
        wasAdded = False
        if (aBikeTour) in self._bikeTours :
            if index < 0 :
                index = 0
            if index > self.numberOfBikeTours() :
                index = self.numberOfBikeTours() - 1
            self._bikeTours.remove(aBikeTour)
            self._bikeTours.insert(index, aBikeTour)
            wasAdded = True
        else :
            wasAdded = self.addBikeTourAt(aBikeTour, index)
        return wasAdded

    def delete(self):
        placeholderBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = None
        if not (placeholderBikeTourPlus is None) :
            placeholderBikeTourPlus.removeGuide(self)
        i = len(self._bikeTours)
        while i > 0 :
            aBikeTour = self._bikeTours[i - 1]
            aBikeTour.delete()
            i -= 1

        super().delete()

    def addBikeTour(self, *argv):
        from .BikeTour import BikeTour
        from .BikeTourPlus import BikeTourPlus
        if len(argv) == 4 and isinstance(argv[0], int) and isinstance(argv[1], int) and isinstance(argv[2], int) and isinstance(argv[3], BikeTourPlus) :
            return self.addBikeTour1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], BikeTour) :
            return self.addBikeTour2(argv[0])
        raise TypeError("No method matches provided parameters")
