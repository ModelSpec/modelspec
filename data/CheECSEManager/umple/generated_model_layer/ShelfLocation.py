#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 44 "../model.ump"
# line 184 "../model.ump"
import os

class ShelfLocation():
    nextId = 1
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #ShelfLocation Attributes
    #Autounique Attributes
    #ShelfLocation Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aColumn, aRow, aShelf):
        self._cheeseWheel = None
        self._shelf = None
        self._id = None
        self._row = None
        self._column = None
        self._column = aColumn
        self._row = aRow
        self._id, ShelfLocation.nextId = ShelfLocation.nextId, ShelfLocation.nextId + 1
        didAddShelf = self.setShelf(aShelf)
        if not didAddShelf :
            raise RuntimeError ("Unable to create location due to shelf. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setColumn(self, aColumn):
        wasSet = False
        self._column = aColumn
        wasSet = True
        return wasSet

    def setRow(self, aRow):
        wasSet = False
        self._row = aRow
        wasSet = True
        return wasSet

    def getColumn(self):
        return self._column

    def getRow(self):
        return self._row

    def getId(self):
        return self._id

    # Code from template association_GetOne 
    def getShelf(self):
        return self._shelf

    # Code from template association_GetOne 
    def getCheeseWheel(self):
        return self._cheeseWheel

    def hasCheeseWheel(self):
        has = not (self._cheeseWheel is None)
        return has

    # Code from template association_SetOneToMany 
    def setShelf(self, aShelf):
        wasSet = False
        if aShelf is None :
            return wasSet
        existingShelf = self._shelf
        self._shelf = aShelf
        if not (existingShelf is None) and not existingShelf == aShelf :
            existingShelf.removeLocation(self)
        self._shelf.addLocation(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToOptionalOne 
    def setCheeseWheel(self, aNewCheeseWheel):
        wasSet = False
        if aNewCheeseWheel is None :
            existingCheeseWheel = self._cheeseWheel
            self._cheeseWheel = None
            if not (existingCheeseWheel is None) and not (existingCheeseWheel.getLocation() is None) :
                existingCheeseWheel.setLocation(None)
            wasSet = True
            return wasSet
        currentCheeseWheel = self.getCheeseWheel()
        if not (currentCheeseWheel is None) and not currentCheeseWheel == aNewCheeseWheel :
            currentCheeseWheel.setLocation(None)
        self._cheeseWheel = aNewCheeseWheel
        existingLocation = aNewCheeseWheel.getLocation()
        if not self == existingLocation :
            aNewCheeseWheel.setLocation(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderShelf = self._shelf
        self._shelf = None
        if not (placeholderShelf is None) :
            placeholderShelf.removeLocation(self)
        if not (self._cheeseWheel is None) :
            self._cheeseWheel.setLocation(None)

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "," + "column" + ":" + str(self.getColumn()) + "," + "row" + ":" + str(self.getRow()) + "]" + str(os.linesep) + "  " + "shelf = " + str(((format(id(self.getShelf()), "x")) if not (self.getShelf() is None) else "null")) + str(os.linesep) + "  " + "cheeseWheel = " + ((format(id(self.getCheeseWheel()), "x")) if not (self.getCheeseWheel() is None) else "null")

