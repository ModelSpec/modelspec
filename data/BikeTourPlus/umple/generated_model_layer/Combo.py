# %% NEW FILE Combo BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8091.03bcab5b3 modeling language!
# line 66 "model.ump"
# line 141 "model.ump"
from .BookableItem import BookableItem
import os

class Combo(BookableItem):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Combo Attributes
    #Combo Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aDiscount, aBikeTourPlus):
        self._comboItems = None
        self._bikeTourPlus = None
        self._discount = None
        super().__init__(aName)
        self._discount = aDiscount
        didAddBikeTourPlus = self.setBikeTourPlus(aBikeTourPlus)
        if not didAddBikeTourPlus :
            raise RuntimeError ("Unable to create combo due to bikeTourPlus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._comboItems = []

    #------------------------
    # INTERFACE
    #------------------------
    def setDiscount(self, aDiscount):
        wasSet = False
        self._discount = aDiscount
        wasSet = True
        return wasSet

    def getDiscount(self):
        return self._discount

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
            existingBikeTourPlus.removeCombo(self)
        self._bikeTourPlus.addCombo(self)
        wasSet = True
        return wasSet

    # Code from template association_IsNumberOfValidMethod
    def isNumberOfComboItemsValid(self):
        isValid = self.numberOfComboItems() >= Combo.minimumNumberOfComboItems()
        return isValid

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfComboItems():
        return 2

    # Code from template association_AddMandatoryManyToOne
    def addComboItem1(self, aQuantity, aBikeTourPlus, aGear):
        from .ComboItem import ComboItem
        aNewComboItem = ComboItem(aQuantity, aBikeTourPlus, self, aGear)
        return aNewComboItem

    def addComboItem2(self, aComboItem):
        wasAdded = False
        if (aComboItem) in self._comboItems :
            return False
        existingCombo = aComboItem.getCombo()
        isNewCombo = not (existingCombo is None) and not self == existingCombo
        if isNewCombo and existingCombo.numberOfComboItems() <= Combo.minimumNumberOfComboItems() :
            return wasAdded
        if isNewCombo :
            aComboItem.setCombo(self)
        else :
            self._comboItems.append(aComboItem)
        wasAdded = True
        return wasAdded

    def removeComboItem(self, aComboItem):
        wasRemoved = False
        #Unable to remove aComboItem, as it must always have a combo
        if self == aComboItem.getCombo() :
            return wasRemoved
        #combo already at minimum (2)
        if self.numberOfComboItems() <= Combo.minimumNumberOfComboItems() :
            return wasRemoved
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
            placeholderBikeTourPlus.removeCombo(self)
        i = len(self._comboItems)
        while i > 0 :
            aComboItem = self._comboItems[i - 1]
            aComboItem.delete()
            i -= 1

        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "discount" + ":" + str(self.getDiscount()) + "]" + str(os.linesep) + "  " + "bikeTourPlus = " + ((format(id(self.getBikeTourPlus()), "x")) if not (self.getBikeTourPlus() is None) else "null")

    def addComboItem(self, *argv):
        from .ComboItem import ComboItem
        from .BikeTourPlus import BikeTourPlus
        from .Gear import Gear
        if len(argv) == 3 and isinstance(argv[0], int) and isinstance(argv[1], BikeTourPlus) and isinstance(argv[2], Gear) :
            return self.addComboItem1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], ComboItem) :
            return self.addComboItem2(argv[0])
        raise TypeError("No method matches provided parameters")
