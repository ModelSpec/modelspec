#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 121 "../model.ump"
# line 149 "../model.ump"
import os

class TOCheeseWheel():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #TOCheeseWheel Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aId, aMonthsAged, aIsSpoiled, aPurchaseDate, aShelfID, aColumn, aRow, aIsOrdered):
        self._isOrdered = None
        self._row = None
        self._column = None
        self._shelfID = None
        self._purchaseDate = None
        self._isSpoiled = None
        self._monthsAged = None
        self._id = None
        self._id = aId
        self._monthsAged = aMonthsAged
        self._isSpoiled = aIsSpoiled
        self._purchaseDate = aPurchaseDate
        self._shelfID = aShelfID
        self._column = aColumn
        self._row = aRow
        self._isOrdered = aIsOrdered

    #------------------------
    # INTERFACE
    #------------------------
    def setId(self, aId):
        wasSet = False
        self._id = aId
        wasSet = True
        return wasSet

    def setMonthsAged(self, aMonthsAged):
        wasSet = False
        self._monthsAged = aMonthsAged
        wasSet = True
        return wasSet

    def setIsSpoiled(self, aIsSpoiled):
        wasSet = False
        self._isSpoiled = aIsSpoiled
        wasSet = True
        return wasSet

    def setPurchaseDate(self, aPurchaseDate):
        wasSet = False
        self._purchaseDate = aPurchaseDate
        wasSet = True
        return wasSet

    def setShelfID(self, aShelfID):
        wasSet = False
        self._shelfID = aShelfID
        wasSet = True
        return wasSet

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

    def setIsOrdered(self, aIsOrdered):
        wasSet = False
        self._isOrdered = aIsOrdered
        wasSet = True
        return wasSet

    def getId(self):
        return self._id

    def getMonthsAged(self):
        return self._monthsAged

    def getIsSpoiled(self):
        return self._isSpoiled

    def getPurchaseDate(self):
        return self._purchaseDate

    def getShelfID(self):
        return self._shelfID

    def getColumn(self):
        return self._column

    def getRow(self):
        return self._row

    def getIsOrdered(self):
        return self._isOrdered

    # Code from template attribute_IsBoolean 
    def isIsSpoiled(self):
        return self._isSpoiled

    # Code from template attribute_IsBoolean 
    def isIsOrdered(self):
        return self._isOrdered

    def delete(self):
        pass

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "," + "monthsAged" + ":" + str(self.getMonthsAged()) + "," + "isSpoiled" + ":" + str(self.getIsSpoiled()) + "," + "shelfID" + ":" + str(self.getShelfID()) + "," + "column" + ":" + str(self.getColumn()) + "," + "row" + ":" + str(self.getRow()) + "," + "isOrdered" + ":" + str(self.getIsOrdered()) + "]" + str(os.linesep) + "  " + "purchaseDate" + "=" + (((self.getPurchaseDate().__str__().replaceAll("  ", "    ")) if not self.getPurchaseDate() == self else "this") if not (self.getPurchaseDate() is None) else "null")

