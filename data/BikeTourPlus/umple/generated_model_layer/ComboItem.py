# %% NEW FILE ComboItem BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8091.03bcab5b3 modeling language!
# line 71 "model.ump"
# line 146 "model.ump"
import os

class ComboItem():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #ComboItem Attributes
    #ComboItem Associations
    #Helper Variables
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aQuantity, aBikeTourPlus, aCombo, aGear):
        self._canSetGear = None
        self._canSetCombo = None
        self._cachedHashCode = None
        self._gear = None
        self._combo = None
        self._bikeTourPlus = None
        self._quantity = None
        self._cachedHashCode = -1
        self._canSetCombo = True
        self._canSetGear = True
        self._quantity = aQuantity
        didAddBikeTourPlus = self.setBikeTourPlus(aBikeTourPlus)
        if not didAddBikeTourPlus :
            raise RuntimeError ("Unable to create comboItem due to bikeTourPlus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddCombo = self.setCombo(aCombo)
        if not didAddCombo :
            raise RuntimeError ("Unable to create comboItem due to combo. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddGear = self.setGear(aGear)
        if not didAddGear :
            raise RuntimeError ("Unable to create comboItem due to gear. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setQuantity(self, aQuantity):
        wasSet = False
        self._quantity = aQuantity
        wasSet = True
        return wasSet

    def getQuantity(self):
        return self._quantity

    # Code from template association_GetOne
    def getBikeTourPlus(self):
        return self._bikeTourPlus

    # Code from template association_GetOne
    def getCombo(self):
        return self._combo

    # Code from template association_GetOne
    def getGear(self):
        return self._gear

    # Code from template association_SetOneToManyAssociationClass
    def setBikeTourPlus(self, aBikeTourPlus):
        wasSet = False
        if aBikeTourPlus is None :
            return wasSet
        existingBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = aBikeTourPlus
        if not (existingBikeTourPlus is None) and not existingBikeTourPlus == aBikeTourPlus :
            existingBikeTourPlus.removeComboItem(self)
        if not self._bikeTourPlus.addComboItem(self) :
            self._bikeTourPlus = existingBikeTourPlus
            wasSet = False
        else :
            wasSet = True
        return wasSet

    # Code from template association_SetOneToMandatoryMany
    def setCombo(self, aCombo):
        from .Combo import Combo
        wasSet = False
        if not self._canSetCombo :
            return False
        #Must provide combo to comboItem
        if aCombo is None :
            return wasSet
        if not (self._combo is None) and self._combo.numberOfComboItems() <= Combo.minimumNumberOfComboItems() :
            return wasSet
        existingCombo = self._combo
        self._combo = aCombo
        if not (existingCombo is None) and not existingCombo == aCombo :
            didRemove = existingCombo.removeComboItem(self)
            if not didRemove :
                self._combo = existingCombo
                return wasSet
        self._combo.addComboItem(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToManyAssociationClass
    def setGear(self, aGear):
        wasSet = False
        if not self._canSetGear :
            return False
        if aGear is None :
            return wasSet
        existingGear = self._gear
        self._gear = aGear
        if not (existingGear is None) and not existingGear == aGear :
            existingGear.removeComboItem(self)
        if not self._gear.addComboItem(self) :
            self._gear = existingGear
            wasSet = False
        else :
            wasSet = True
        return wasSet

    def equals(self, obj):
        if obj is None :
            return False
        if not type(self) is type(obj) :
            return False
        compareTo = obj
        if self.getCombo() is None and not (compareTo.getCombo() is None) :
            return False
        elif not (self.getCombo() is None) and not self.getCombo() == compareTo.getCombo() :
            return False
        if self.getGear() is None and not (compareTo.getGear() is None) :
            return False
        elif not (self.getGear() is None) and not self.getGear() == compareTo.getGear() :
            return False
        return True

    def __hash__(self):
        if self._cachedHashCode != -1 :
            return self._cachedHashCode
        self._cachedHashCode = 17
        if not (self.getCombo() is None) :
            self._cachedHashCode = self._cachedHashCode * 23 + self.getCombo().__hash__()
        else :
            self._cachedHashCode = self._cachedHashCode * 23
        if not (self.getGear() is None) :
            self._cachedHashCode = self._cachedHashCode * 23 + self.getGear().__hash__()
        else :
            self._cachedHashCode = self._cachedHashCode * 23
        self._canSetCombo = False
        self._canSetGear = False
        return self._cachedHashCode

    def delete(self):
        placeholderBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = None
        if not (placeholderBikeTourPlus is None) :
            placeholderBikeTourPlus.removeComboItem(self)
        placeholderCombo = self._combo
        self._combo = None
        if not (placeholderCombo is None) :
            placeholderCombo.removeComboItem(self)
        placeholderGear = self._gear
        self._gear = None
        if not (placeholderGear is None) :
            placeholderGear.removeComboItem(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "quantity" + ":" + str(self.getQuantity()) + "]" + str(os.linesep) + "  " + "bikeTourPlus = " + str(((format(id(self.getBikeTourPlus()), "x")) if not (self.getBikeTourPlus() is None) else "null")) + str(os.linesep) + "  " + "combo = " + str(((format(id(self.getCombo()), "x")) if not (self.getCombo() is None) else "null")) + str(os.linesep) + "  " + "gear = " + ((format(id(self.getGear()), "x")) if not (self.getGear() is None) else "null")
