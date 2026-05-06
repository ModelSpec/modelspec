#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 13 "model.ump"
# line 29 "model.ump"

class TOShelf():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #TOShelf Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aShelfID):
        self._monthsAgeds = None
        self._rowNrs = None
        self._columnNrs = None
        self._cheeseWheelIDs = None
        self._shelfID = None
        self._shelfID = aShelfID
        self._cheeseWheelIDs = []
        self._columnNrs = []
        self._rowNrs = []
        self._monthsAgeds = []

    #------------------------
    # INTERFACE
    #------------------------
    def setShelfID(self, aShelfID):
        wasSet = False
        self._shelfID = aShelfID
        wasSet = True
        return wasSet

    # Code from template attribute_SetMany 
    def addCheeseWheelID(self, aCheeseWheelID):
        wasAdded = False
        wasAdded = self._cheeseWheelIDs.append(aCheeseWheelID)
        return wasAdded

    def removeCheeseWheelID(self, aCheeseWheelID):
        wasRemoved = False
        wasRemoved = self._cheeseWheelIDs.remove(aCheeseWheelID)
        return wasRemoved

    # Code from template attribute_SetMany 
    def addColumnNr(self, aColumnNr):
        wasAdded = False
        wasAdded = self._columnNrs.append(aColumnNr)
        return wasAdded

    def removeColumnNr(self, aColumnNr):
        wasRemoved = False
        wasRemoved = self._columnNrs.remove(aColumnNr)
        return wasRemoved

    # Code from template attribute_SetMany 
    def addRowNr(self, aRowNr):
        wasAdded = False
        wasAdded = self._rowNrs.append(aRowNr)
        return wasAdded

    def removeRowNr(self, aRowNr):
        wasRemoved = False
        wasRemoved = self._rowNrs.remove(aRowNr)
        return wasRemoved

    # Code from template attribute_SetMany 
    def addMonthsAged(self, aMonthsAged):
        wasAdded = False
        wasAdded = self._monthsAgeds.append(aMonthsAged)
        return wasAdded

    def removeMonthsAged(self, aMonthsAged):
        wasRemoved = False
        wasRemoved = self._monthsAgeds.remove(aMonthsAged)
        return wasRemoved

    def getShelfID(self):
        return self._shelfID

    # Code from template attribute_GetMany 
    def getCheeseWheelID(self, index):
        aCheeseWheelID = self._cheeseWheelIDs[index]
        return aCheeseWheelID

    def getCheeseWheelIDs(self):
        newCheeseWheelIDs = self._cheeseWheelIDs.copy()
        return newCheeseWheelIDs

    def numberOfCheeseWheelIDs(self):
        number = len(self._cheeseWheelIDs)
        return number

    def hasCheeseWheelIDs(self):
        has = len(self._cheeseWheelIDs) > 0
        return has

    def indexOfCheeseWheelID(self, aCheeseWheelID):
        index = (-1 if not aCheeseWheelID in self._cheeseWheelIDs else self._cheeseWheelIDs.index(aCheeseWheelID))
        return index

    # Code from template attribute_GetMany 
    def getColumnNr(self, index):
        aColumnNr = self._columnNrs[index]
        return aColumnNr

    def getColumnNrs(self):
        newColumnNrs = self._columnNrs.copy()
        return newColumnNrs

    def numberOfColumnNrs(self):
        number = len(self._columnNrs)
        return number

    def hasColumnNrs(self):
        has = len(self._columnNrs) > 0
        return has

    def indexOfColumnNr(self, aColumnNr):
        index = (-1 if not aColumnNr in self._columnNrs else self._columnNrs.index(aColumnNr))
        return index

    # Code from template attribute_GetMany 
    def getRowNr(self, index):
        aRowNr = self._rowNrs[index]
        return aRowNr

    def getRowNrs(self):
        newRowNrs = self._rowNrs.copy()
        return newRowNrs

    def numberOfRowNrs(self):
        number = len(self._rowNrs)
        return number

    def hasRowNrs(self):
        has = len(self._rowNrs) > 0
        return has

    def indexOfRowNr(self, aRowNr):
        index = (-1 if not aRowNr in self._rowNrs else self._rowNrs.index(aRowNr))
        return index

    # Code from template attribute_GetMany 
    def getMonthsAged(self, index):
        aMonthsAged = self._monthsAgeds[index]
        return aMonthsAged

    def getMonthsAgeds(self):
        newMonthsAgeds = self._monthsAgeds.copy()
        return newMonthsAgeds

    def numberOfMonthsAgeds(self):
        number = len(self._monthsAgeds)
        return number

    def hasMonthsAgeds(self):
        has = len(self._monthsAgeds) > 0
        return has

    def indexOfMonthsAged(self, aMonthsAged):
        index = (-1 if not aMonthsAged in self._monthsAgeds else self._monthsAgeds.index(aMonthsAged))
        return index

    def delete(self):
        pass

    def __str__(self):
        return str(super().__str__()) + "[" + "shelfID" + ":" + str(self.getShelfID()) + "]"

