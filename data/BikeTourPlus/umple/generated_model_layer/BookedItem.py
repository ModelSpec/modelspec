# %% NEW FILE BookedItem BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8091.03bcab5b3 modeling language!
# line 50 "model.ump"
# line 126 "model.ump"
import os

class BookedItem():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #BookedItem Attributes
    #BookedItem Associations
    #Helper Variables
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aQuantity, aBikeTourPlus, aParticipant, aItem):
        self._canSetItem = None
        self._canSetParticipant = None
        self._cachedHashCode = None
        self._item = None
        self._participant = None
        self._bikeTourPlus = None
        self._quantity = None
        self._cachedHashCode = -1
        self._canSetParticipant = True
        self._canSetItem = True
        self._quantity = aQuantity
        didAddBikeTourPlus = self.setBikeTourPlus(aBikeTourPlus)
        if not didAddBikeTourPlus :
            raise RuntimeError ("Unable to create bookedItem due to bikeTourPlus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddParticipant = self.setParticipant(aParticipant)
        if not didAddParticipant :
            raise RuntimeError ("Unable to create bookedItem due to participant. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddItem = self.setItem(aItem)
        if not didAddItem :
            raise RuntimeError ("Unable to create bookedItem due to item. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

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
    def getParticipant(self):
        return self._participant

    # Code from template association_GetOne
    def getItem(self):
        return self._item

    # Code from template association_SetOneToManyAssociationClass
    def setBikeTourPlus(self, aBikeTourPlus):
        wasSet = False
        if aBikeTourPlus is None :
            return wasSet
        existingBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = aBikeTourPlus
        if not (existingBikeTourPlus is None) and not existingBikeTourPlus == aBikeTourPlus :
            existingBikeTourPlus.removeBookedItem(self)
        if not self._bikeTourPlus.addBookedItem(self) :
            self._bikeTourPlus = existingBikeTourPlus
            wasSet = False
        else :
            wasSet = True
        return wasSet

    # Code from template association_SetOneToManyAssociationClass
    def setParticipant(self, aParticipant):
        wasSet = False
        if not self._canSetParticipant :
            return False
        if aParticipant is None :
            return wasSet
        existingParticipant = self._participant
        self._participant = aParticipant
        if not (existingParticipant is None) and not existingParticipant == aParticipant :
            existingParticipant.removeBookedItem(self)
        if not self._participant.addBookedItem(self) :
            self._participant = existingParticipant
            wasSet = False
        else :
            wasSet = True
        return wasSet

    # Code from template association_SetOneToManyAssociationClass
    def setItem(self, aItem):
        wasSet = False
        if not self._canSetItem :
            return False
        if aItem is None :
            return wasSet
        existingItem = self._item
        self._item = aItem
        if not (existingItem is None) and not existingItem == aItem :
            existingItem.removeBookedItem(self)
        if not self._item.addBookedItem(self) :
            self._item = existingItem
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
        if self.getParticipant() is None and not (compareTo.getParticipant() is None) :
            return False
        elif not (self.getParticipant() is None) and not self.getParticipant() == compareTo.getParticipant() :
            return False
        if self.getItem() is None and not (compareTo.getItem() is None) :
            return False
        elif not (self.getItem() is None) and not self.getItem() == compareTo.getItem() :
            return False
        return True

    def __hash__(self):
        if self._cachedHashCode != -1 :
            return self._cachedHashCode
        self._cachedHashCode = 17
        if not (self.getParticipant() is None) :
            self._cachedHashCode = self._cachedHashCode * 23 + self.getParticipant().__hash__()
        else :
            self._cachedHashCode = self._cachedHashCode * 23
        if not (self.getItem() is None) :
            self._cachedHashCode = self._cachedHashCode * 23 + self.getItem().__hash__()
        else :
            self._cachedHashCode = self._cachedHashCode * 23
        self._canSetParticipant = False
        self._canSetItem = False
        return self._cachedHashCode

    def delete(self):
        placeholderBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = None
        if not (placeholderBikeTourPlus is None) :
            placeholderBikeTourPlus.removeBookedItem(self)
        placeholderParticipant = self._participant
        self._participant = None
        if not (placeholderParticipant is None) :
            placeholderParticipant.removeBookedItem(self)
        placeholderItem = self._item
        self._item = None
        if not (placeholderItem is None) :
            placeholderItem.removeBookedItem(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "quantity" + ":" + str(self.getQuantity()) + "]" + str(os.linesep) + "  " + "bikeTourPlus = " + str(((format(id(self.getBikeTourPlus()), "x")) if not (self.getBikeTourPlus() is None) else "null")) + str(os.linesep) + "  " + "participant = " + str(((format(id(self.getParticipant()), "x")) if not (self.getParticipant() is None) else "null")) + str(os.linesep) + "  " + "item = " + ((format(id(self.getItem()), "x")) if not (self.getItem() is None) else "null")
