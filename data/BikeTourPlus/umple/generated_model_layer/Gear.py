# %% NEW FILE Gear BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8091.03bcab5b3 modeling language!
# line 61 "model.ump"
# line 136 "model.ump"
from .BookableItem import BookableItem
import os

class Gear(BookableItem):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Gear Attributes
    #Gear Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aPricePerWeek, aBikeTourPlus):
        self._comboItems = None
        self._bikeTourPlus = None
        self._pricePerWeek = None
        super().__init__(aName)
        self._pricePerWeek = aPricePerWeek
        didAddBikeTourPlus = self.setBikeTourPlus(aBikeTourPlus)
        if not didAddBikeTourPlus :
            raise RuntimeError ("Unable to create gear due to bikeTourPlus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._comboItems = []

    #------------------------
    # INTERFACE
    #------------------------
    def setPricePerWeek(self, aPricePerWeek):
        wasSet = False
        self._pricePerWeek = aPricePerWeek
        wasSet = True
        return wasSet

    def getPricePerWeek(self):
        return self._pricePerWeek

    # Code from template association_GetOne
    def getBikeTourPlus(self):
        return self._bikeTourPlus

    # Code from template association_GetMany
    def getComboItem(self, index):
        aComboItem = self._comboItems[index]
        return aComboItem

    def getComboItems(self):
        newComboItems = tuple(self._comboItems)
        return newComboItems

    def numberOfComboItems(self):
        number = len(self._comboItems)
        return number

    def hasComboItems(self):
        has = len(self._comboItems) > 0
        return has

    def indexOfComboItem(self, aComboItem):
        index = (-1 if not aComboItem in self._comboItems else self._comboItems.index(aComboItem))
        return index

    # Code from template association_SetOneToMany
    def setBikeTourPlus(self, aBikeTourPlus):
        wasSet = False
        if aBikeTourPlus is None :
            return wasSet
        existingBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = aBikeTourPlus
        if not (existingBikeTourPlus is None) and not existingBikeTourPlus == aBikeTourPlus :
            existingBikeTourPlus.removeGear(self)
        self._bikeTourPlus.addGear(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfComboItems():
        return 0

    # Code from template association_AddManyToOne
    def addComboItem1(self, aQuantity, aBikeTourPlus, aCombo):
        from .ComboItem import ComboItem
        return ComboItem(aQuantity, aBikeTourPlus, aCombo, self)

    def addComboItem2(self, aComboItem):
        wasAdded = False
        if (aComboItem) in self._comboItems :
            return False
        existingGear = aComboItem.getGear()
        isNewGear = not (existingGear is None) and not self == existingGear
        if isNewGear :
            aComboItem.setGear(self)
        else :
            self._comboItems.append(aComboItem)
        wasAdded = True
        return wasAdded

    def removeComboItem(self, aComboItem):
        wasRemoved = False
        #Unable to remove aComboItem, as it must always have a gear
        if not self == aComboItem.getGear() :
            self._comboItems.remove(aComboItem)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addComboItemAt(self, aComboItem, index):
        wasAdded = False
        if self.addComboItem(aComboItem) :
            if index < 0 :
                index = 0
            if index > self.numberOfComboItems() :
                index = self.numberOfComboItems() - 1
            self._comboItems.remove(aComboItem)
            self._comboItems.insert(index, aComboItem)
            wasAdded = True
        return wasAdded

    def addOrMoveComboItemAt(self, aComboItem, index):
        wasAdded = False
        if (aComboItem) in self._comboItems :
            if index < 0 :
                index = 0
            if index > self.numberOfComboItems() :
                index = self.numberOfComboItems() - 1
            self._comboItems.remove(aComboItem)
            self._comboItems.insert(index, aComboItem)
            wasAdded = True
        else :
            wasAdded = self.addComboItemAt(aComboItem, index)
        return wasAdded

    def delete(self):
        placeholderBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = None
        if not (placeholderBikeTourPlus is None) :
            placeholderBikeTourPlus.removeGear(self)
        i = len(self._comboItems)
        while i > 0 :
            aComboItem = self._comboItems[i - 1]
            aComboItem.delete()
            i -= 1

        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "pricePerWeek" + ":" + str(self.getPricePerWeek()) + "]" + str(os.linesep) + "  " + "bikeTourPlus = " + ((format(id(self.getBikeTourPlus()), "x")) if not (self.getBikeTourPlus() is None) else "null")

    def addComboItem(self, *argv):
        from .ComboItem import ComboItem
        from .BikeTourPlus import BikeTourPlus
        from .Combo import Combo
        if len(argv) == 3 and isinstance(argv[0], int) and isinstance(argv[1], BikeTourPlus) and isinstance(argv[2], Combo) :
            return self.addComboItem1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], ComboItem) :
            return self.addComboItem2(argv[0])
        raise TypeError("No method matches provided parameters")
