#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 2 "model.ump"
# line 24 "model.ump"

class TOFarmer():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #TOFarmer Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEmail, aPassword, aName, aAddress):
        self._isSpoileds = None
        self._monthsAgeds = None
        self._purchaseDates = None
        self._cheeseWheelIDs = None
        self._address = None
        self._name = None
        self._password = None
        self._email = None
        self._email = aEmail
        self._password = aPassword
        self._name = aName
        self._address = aAddress
        self._cheeseWheelIDs = []
        self._purchaseDates = []
        self._monthsAgeds = []
        self._isSpoileds = []

    #------------------------
    # INTERFACE
    #------------------------
    def setEmail(self, aEmail):
        wasSet = False
        self._email = aEmail
        wasSet = True
        return wasSet

    def setPassword(self, aPassword):
        wasSet = False
        self._password = aPassword
        wasSet = True
        return wasSet

    def setName(self, aName):
        wasSet = False
        self._name = aName
        wasSet = True
        return wasSet

    def setAddress(self, aAddress):
        wasSet = False
        self._address = aAddress
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
    def addPurchaseDate(self, aPurchaseDate):
        wasAdded = False
        wasAdded = self._purchaseDates.append(aPurchaseDate)
        return wasAdded

    def removePurchaseDate(self, aPurchaseDate):
        wasRemoved = False
        wasRemoved = self._purchaseDates.remove(aPurchaseDate)
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

    # Code from template attribute_SetMany 
    def addIsSpoiled(self, aIsSpoiled):
        wasAdded = False
        wasAdded = self._isSpoileds.append(aIsSpoiled)
        return wasAdded

    def removeIsSpoiled(self, aIsSpoiled):
        wasRemoved = False
        wasRemoved = self._isSpoileds.remove(aIsSpoiled)
        return wasRemoved

    def getEmail(self):
        return self._email

    def getPassword(self):
        return self._password

    def getName(self):
        return self._name

    def getAddress(self):
        return self._address

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
    def getPurchaseDate(self, index):
        aPurchaseDate = self._purchaseDates[index]
        return aPurchaseDate

    def getPurchaseDates(self):
        newPurchaseDates = self._purchaseDates.copy()
        return newPurchaseDates

    def numberOfPurchaseDates(self):
        number = len(self._purchaseDates)
        return number

    def hasPurchaseDates(self):
        has = len(self._purchaseDates) > 0
        return has

    def indexOfPurchaseDate(self, aPurchaseDate):
        index = (-1 if not aPurchaseDate in self._purchaseDates else self._purchaseDates.index(aPurchaseDate))
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

    # Code from template attribute_GetMany 
    def getIsSpoiled(self, index):
        aIsSpoiled = self._isSpoileds[index]
        return aIsSpoiled

    def getIsSpoileds(self):
        newIsSpoileds = self._isSpoileds.copy()
        return newIsSpoileds

    def numberOfIsSpoileds(self):
        number = len(self._isSpoileds)
        return number

    def hasIsSpoileds(self):
        has = len(self._isSpoileds) > 0
        return has

    def indexOfIsSpoiled(self, aIsSpoiled):
        index = (-1 if not aIsSpoiled in self._isSpoileds else self._isSpoileds.index(aIsSpoiled))
        return index

    def delete(self):
        pass

    def __str__(self):
        return str(super().__str__()) + "[" + "email" + ":" + str(self.getEmail()) + "," + "password" + ":" + str(self.getPassword()) + "," + "name" + ":" + str(self.getName()) + "," + "address" + ":" + str(self.getAddress()) + "]"

