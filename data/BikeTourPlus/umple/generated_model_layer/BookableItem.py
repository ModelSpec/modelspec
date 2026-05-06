# %% NEW FILE BookableItem BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8091.03bcab5b3 modeling language!
# line 56 "model.ump"
# line 131 "model.ump"
from abc import ABC, abstractmethod

class BookableItem(ABC):
    bookableitemsByName = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #BookableItem Attributes
    #BookableItem Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName):
        self._bookedItems = None
        self._name = None
        if not self.setName(aName) :
            raise RuntimeError ("Cannot create due to duplicate name. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        self._bookedItems = []

    #------------------------
    # INTERFACE
    #------------------------
    def setName(self, aName):
        wasSet = False
        anOldName = self.getName()
        if not (anOldName is None) and anOldName == aName :
            return True
        if BookableItem.hasWithName(aName) :
            return wasSet
        self._name = aName
        wasSet = True
        if not (anOldName is None) :
            BookableItem.bookableitemsByName.pop(anOldName, None)
        BookableItem.bookableitemsByName[aName] = self
        return wasSet

    def getName(self):
        return self._name

    # Code from template attribute_GetUnique
    @staticmethod
    def getWithName(aName):
        return BookableItem.bookableitemsByName.get(aName)

    # Code from template attribute_HasUnique
    @staticmethod
    def hasWithName(aName):
        return not (BookableItem.getWithName(aName) is None)

    # Code from template association_GetMany
    def getBookedItem(self, index):
        aBookedItem = self._bookedItems[index]
        return aBookedItem

    def getBookedItems(self):
        newBookedItems = tuple(self._bookedItems)
        return newBookedItems

    def numberOfBookedItems(self):
        number = len(self._bookedItems)
        return number

    def hasBookedItems(self):
        has = len(self._bookedItems) > 0
        return has

    def indexOfBookedItem(self, aBookedItem):
        index = (-1 if not aBookedItem in self._bookedItems else self._bookedItems.index(aBookedItem))
        return index

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfBookedItems():
        return 0

    # Code from template association_AddManyToOne
    def addBookedItem1(self, aQuantity, aBikeTourPlus, aParticipant):
        from .BookedItem import BookedItem
        return BookedItem(aQuantity, aBikeTourPlus, aParticipant, self)

    def addBookedItem2(self, aBookedItem):
        wasAdded = False
        if (aBookedItem) in self._bookedItems :
            return False
        existingItem = aBookedItem.getItem()
        isNewItem = not (existingItem is None) and not self == existingItem
        if isNewItem :
            aBookedItem.setItem(self)
        else :
            self._bookedItems.append(aBookedItem)
        wasAdded = True
        return wasAdded

    def removeBookedItem(self, aBookedItem):
        wasRemoved = False
        #Unable to remove aBookedItem, as it must always have a item
        if not self == aBookedItem.getItem() :
            self._bookedItems.remove(aBookedItem)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addBookedItemAt(self, aBookedItem, index):
        wasAdded = False
        if self.addBookedItem(aBookedItem) :
            if index < 0 :
                index = 0
            if index > self.numberOfBookedItems() :
                index = self.numberOfBookedItems() - 1
            self._bookedItems.remove(aBookedItem)
            self._bookedItems.insert(index, aBookedItem)
            wasAdded = True
        return wasAdded

    def addOrMoveBookedItemAt(self, aBookedItem, index):
        wasAdded = False
        if (aBookedItem) in self._bookedItems :
            if index < 0 :
                index = 0
            if index > self.numberOfBookedItems() :
                index = self.numberOfBookedItems() - 1
            self._bookedItems.remove(aBookedItem)
            self._bookedItems.insert(index, aBookedItem)
            wasAdded = True
        else :
            wasAdded = self.addBookedItemAt(aBookedItem, index)
        return wasAdded

    def delete(self):
        BookableItem.bookableitemsByName.pop(self.getName(), None)
        i = len(self._bookedItems)
        while i > 0 :
            aBookedItem = self._bookedItems[i - 1]
            aBookedItem.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "name" + ":" + str(self.getName()) + "]"

    def addBookedItem(self, *argv):
        from .BookedItem import BookedItem
        from .BikeTourPlus import BikeTourPlus
        from .Participant import Participant
        if len(argv) == 3 and isinstance(argv[0], int) and isinstance(argv[1], BikeTourPlus) and isinstance(argv[2], Participant) :
            return self.addBookedItem1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], BookedItem) :
            return self.addBookedItem2(argv[0])
        raise TypeError("No method matches provided parameters")
