#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 39 "../model.ump"
# line 179 "../model.ump"
import os

class Shelf():
    shelfsById = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Shelf Attributes
    #Shelf Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aId, aCheECSEManager):
        self._robot = None
        self._cheECSEManager = None
        self._locations = None
        self._id = None
        if not self.setId(aId) :
            raise RuntimeError ("Cannot create due to duplicate id. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        self._locations = []
        didAddCheECSEManager = self.setCheECSEManager(aCheECSEManager)
        if not didAddCheECSEManager :
            raise RuntimeError ("Unable to create shelve due to cheECSEManager. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setId(self, aId):
        wasSet = False
        anOldId = self.getId()
        if not (anOldId is None) and anOldId == aId :
            return True
        if Shelf.hasWithId(aId) :
            return wasSet
        self._id = aId
        wasSet = True
        if not (anOldId is None) :
            Shelf.shelfsById.pop(anOldId, None)
        Shelf.shelfsById[aId] = self
        return wasSet

    def getId(self):
        return self._id

    # Code from template attribute_GetUnique 
    @staticmethod
    def getWithId(aId):
        return Shelf.shelfsById.get(aId)

    # Code from template attribute_HasUnique 
    @staticmethod
    def hasWithId(aId):
        return not (Shelf.getWithId(aId) is None)

    # Code from template association_GetMany 
    def getLocation(self, index):
        aLocation = self._locations[index]
        return aLocation

    def getLocations(self):
        newLocations = tuple(self._locations)
        return newLocations

    def numberOfLocations(self):
        number = len(self._locations)
        return number

    def hasLocations(self):
        has = len(self._locations) > 0
        return has

    def indexOfLocation(self, aLocation):
        index = (-1 if not aLocation in self._locations else self._locations.index(aLocation))
        return index

    # Code from template association_GetOne 
    def getCheECSEManager(self):
        return self._cheECSEManager

    # Code from template association_GetOne 
    def getRobot(self):
        return self._robot

    def hasRobot(self):
        has = not (self._robot is None)
        return has

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfLocations():
        return 0

    # Code from template association_AddManyToOne 
    def addLocation1(self, aColumn, aRow):
        from ..generated_model_layer.ShelfLocation import ShelfLocation
        return ShelfLocation(aColumn, aRow, self)

    def addLocation2(self, aLocation):
        wasAdded = False
        if (aLocation) in self._locations :
            return False
        existingShelf = aLocation.getShelf()
        isNewShelf = not (existingShelf is None) and not self == existingShelf
        if isNewShelf :
            aLocation.setShelf(self)
        else :
            self._locations.append(aLocation)
        wasAdded = True
        return wasAdded

    def removeLocation(self, aLocation):
        wasRemoved = False
        #Unable to remove aLocation, as it must always have a shelf
        if not self == aLocation.getShelf() :
            self._locations.remove(aLocation)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addLocationAt(self, aLocation, index):
        wasAdded = False
        if self.addLocation(aLocation) :
            if index < 0 :
                index = 0
            if index > self.numberOfLocations() :
                index = self.numberOfLocations() - 1
            self._locations.remove(aLocation)
            self._locations.insert(index, aLocation)
            wasAdded = True
        return wasAdded

    def addOrMoveLocationAt(self, aLocation, index):
        wasAdded = False
        if (aLocation) in self._locations :
            if index < 0 :
                index = 0
            if index > self.numberOfLocations() :
                index = self.numberOfLocations() - 1
            self._locations.remove(aLocation)
            self._locations.insert(index, aLocation)
            wasAdded = True
        else :
            wasAdded = self.addLocationAt(aLocation, index)
        return wasAdded

    # Code from template association_SetOneToMany 
    def setCheECSEManager(self, aCheECSEManager):
        wasSet = False
        if aCheECSEManager is None :
            return wasSet
        existingCheECSEManager = self._cheECSEManager
        self._cheECSEManager = aCheECSEManager
        if not (existingCheECSEManager is None) and not existingCheECSEManager == aCheECSEManager :
            existingCheECSEManager.removeShelve(self)
        self._cheECSEManager.addShelve(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToOptionalOne 
    def setRobot(self, aNewRobot):
        wasSet = False
        if aNewRobot is None :
            existingRobot = self._robot
            self._robot = None
            if not (existingRobot is None) and not (existingRobot.getCurrentShelf() is None) :
                existingRobot.setCurrentShelf(None)
            wasSet = True
            return wasSet
        currentRobot = self.getRobot()
        if not (currentRobot is None) and not currentRobot == aNewRobot :
            currentRobot.setCurrentShelf(None)
        self._robot = aNewRobot
        existingCurrentShelf = aNewRobot.getCurrentShelf()
        if not self == existingCurrentShelf :
            aNewRobot.setCurrentShelf(self)
        wasSet = True
        return wasSet

    def delete(self):
        Shelf.shelfsById.pop(self.getId(), None)

        while len(self._locations) > 0 :
            aLocation = self._locations[len(self._locations) - 1]
            aLocation.delete()
            self._locations.remove(aLocation)

        placeholderCheECSEManager = self._cheECSEManager
        self._cheECSEManager = None
        if not (placeholderCheECSEManager is None) :
            placeholderCheECSEManager.removeShelve(self)
        if not (self._robot is None) :
            self._robot.setCurrentShelf(None)

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "]" + str(os.linesep) + "  " + "cheECSEManager = " + str(((format(id(self.getCheECSEManager()), "x")) if not (self.getCheECSEManager() is None) else "null")) + str(os.linesep) + "  " + "robot = " + ((format(id(self.getRobot()), "x")) if not (self.getRobot() is None) else "null")

    def addLocation(self, *argv):
        from ..generated_model_layer.ShelfLocation import ShelfLocation
        if len(argv) == 2 and isinstance(argv[0], int) and isinstance(argv[1], int) :
            return self.addLocation1(argv[0], argv[1])
        if len(argv) == 1 and isinstance(argv[0], ShelfLocation) :
            return self.addLocation2(argv[0])
        raise TypeError("No method matches provided parameters")

