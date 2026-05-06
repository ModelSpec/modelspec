#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 50 "../model.ump"
# line 189 "../model.ump"
import os
from enum import Enum, auto

class CheeseWheel():
    nextId = 1
    #------------------------
    # ENUMERATIONS
    #------------------------
    class MaturationPeriod(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        Six = auto()
        Twelve = auto()
        TwentyFour = auto()
        ThirtySix = auto()

    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #CheeseWheel Attributes
    #Autounique Attributes
    #CheeseWheel Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aMonthsAged, aIsSpoiled, aPurchase, aCheECSEManager):
        self._robot = None
        self._cheECSEManager = None
        self._order = None
        self._location = None
        self._purchase = None
        self._id = None
        self._isSpoiled = None
        self._monthsAged = None
        self._monthsAged = aMonthsAged
        self._isSpoiled = aIsSpoiled
        self._id, CheeseWheel.nextId = CheeseWheel.nextId, CheeseWheel.nextId + 1
        didAddPurchase = self.setPurchase(aPurchase)
        if not didAddPurchase :
            raise RuntimeError ("Unable to create cheeseWheel due to purchase. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddCheECSEManager = self.setCheECSEManager(aCheECSEManager)
        if not didAddCheECSEManager :
            raise RuntimeError ("Unable to create cheeseWheel due to cheECSEManager. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
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

    def getMonthsAged(self):
        return self._monthsAged

    def getIsSpoiled(self):
        return self._isSpoiled

    def getId(self):
        return self._id

    # Code from template attribute_IsBoolean 
    def isIsSpoiled(self):
        return self._isSpoiled

    # Code from template association_GetOne 
    def getPurchase(self):
        return self._purchase

    # Code from template association_GetOne 
    def getLocation(self):
        return self._location

    def hasLocation(self):
        has = not (self._location is None)
        return has

    # Code from template association_GetOne 
    def getOrder(self):
        return self._order

    def hasOrder(self):
        has = not (self._order is None)
        return has

    # Code from template association_GetOne 
    def getCheECSEManager(self):
        return self._cheECSEManager

    # Code from template association_GetOne 
    def getRobot(self):
        return self._robot

    def hasRobot(self):
        has = not (self._robot is None)
        return has

    # Code from template association_SetOneToMany 
    def setPurchase(self, aPurchase):
        wasSet = False
        if aPurchase is None :
            return wasSet
        existingPurchase = self._purchase
        self._purchase = aPurchase
        if not (existingPurchase is None) and not existingPurchase == aPurchase :
            existingPurchase.removeCheeseWheel(self)
        self._purchase.addCheeseWheel(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToOptionalOne 
    def setLocation(self, aNewLocation):
        wasSet = False
        if aNewLocation is None :
            existingLocation = self._location
            self._location = None
            if not (existingLocation is None) and not (existingLocation.getCheeseWheel() is None) :
                existingLocation.setCheeseWheel(None)
            wasSet = True
            return wasSet
        currentLocation = self.getLocation()
        if not (currentLocation is None) and not currentLocation == aNewLocation :
            currentLocation.setCheeseWheel(None)
        self._location = aNewLocation
        existingCheeseWheel = aNewLocation.getCheeseWheel()
        if not self == existingCheeseWheel :
            aNewLocation.setCheeseWheel(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToMany 
    def setOrder(self, aOrder):
        wasSet = False
        existingOrder = self._order
        self._order = aOrder
        if not (existingOrder is None) and not existingOrder == aOrder :
            existingOrder.removeCheeseWheel(self)
        if not (aOrder is None) :
            aOrder.addCheeseWheel(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany 
    def setCheECSEManager(self, aCheECSEManager):
        wasSet = False
        if aCheECSEManager is None :
            return wasSet
        existingCheECSEManager = self._cheECSEManager
        self._cheECSEManager = aCheECSEManager
        if not (existingCheECSEManager is None) and not existingCheECSEManager == aCheECSEManager :
            existingCheECSEManager.removeCheeseWheel(self)
        self._cheECSEManager.addCheeseWheel(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToOptionalOne 
    def setRobot(self, aNewRobot):
        wasSet = False
        if aNewRobot is None :
            existingRobot = self._robot
            self._robot = None
            if not (existingRobot is None) and not (existingRobot.getCurrentCheeseWheel() is None) :
                existingRobot.setCurrentCheeseWheel(None)
            wasSet = True
            return wasSet
        currentRobot = self.getRobot()
        if not (currentRobot is None) and not currentRobot == aNewRobot :
            currentRobot.setCurrentCheeseWheel(None)
        self._robot = aNewRobot
        existingCurrentCheeseWheel = aNewRobot.getCurrentCheeseWheel()
        if not self == existingCurrentCheeseWheel :
            aNewRobot.setCurrentCheeseWheel(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderPurchase = self._purchase
        self._purchase = None
        if not (placeholderPurchase is None) :
            placeholderPurchase.removeCheeseWheel(self)
        if not (self._location is None) :
            self._location.setCheeseWheel(None)
        if not (self._order is None) :
            placeholderOrder = self._order
            self._order = None
            placeholderOrder.removeCheeseWheel(self)
        placeholderCheECSEManager = self._cheECSEManager
        self._cheECSEManager = None
        if not (placeholderCheECSEManager is None) :
            placeholderCheECSEManager.removeCheeseWheel(self)
        if not (self._robot is None) :
            self._robot.setCurrentCheeseWheel(None)

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "," + "isSpoiled" + ":" + str(self.getIsSpoiled()) + "]" + str(os.linesep) + "  " + "monthsAged" + "=" + str((((self.getMonthsAged().__str__().replaceAll("  ", "    ")) if not self.getMonthsAged() == self else "this") if not (self.getMonthsAged() is None) else "null")) + str(os.linesep) + "  " + "purchase = " + str(((format(id(self.getPurchase()), "x")) if not (self.getPurchase() is None) else "null")) + str(os.linesep) + "  " + "location = " + str(((format(id(self.getLocation()), "x")) if not (self.getLocation() is None) else "null")) + str(os.linesep) + "  " + "order = " + str(((format(id(self.getOrder()), "x")) if not (self.getOrder() is None) else "null")) + str(os.linesep) + "  " + "cheECSEManager = " + str(((format(id(self.getCheECSEManager()), "x")) if not (self.getCheECSEManager() is None) else "null")) + str(os.linesep) + "  " + "robot = " + ((format(id(self.getRobot()), "x")) if not (self.getRobot() is None) else "null")

