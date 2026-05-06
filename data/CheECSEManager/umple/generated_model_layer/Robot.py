#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 79 "../model.ump"
# line 209 "../model.ump"
import os

class Robot():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Robot Attributes
    #Robot Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aIsFacingAisle, aCheECSEManager):
        self._cheECSEManager = None
        self._log = None
        self._currentCheeseWheel = None
        self._currentShelf = None
        self._isFacingAisle = None
        self._isFacingAisle = aIsFacingAisle
        self._log = []
        didAddCheECSEManager = self.setCheECSEManager(aCheECSEManager)
        if not didAddCheECSEManager :
            raise RuntimeError ("Unable to create robot due to cheECSEManager. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setIsFacingAisle(self, aIsFacingAisle):
        wasSet = False
        self._isFacingAisle = aIsFacingAisle
        wasSet = True
        return wasSet

    def getIsFacingAisle(self):
        return self._isFacingAisle

    # Code from template attribute_IsBoolean 
    def isIsFacingAisle(self):
        return self._isFacingAisle

    # Code from template association_GetOne 
    def getCurrentShelf(self):
        return self._currentShelf

    def hasCurrentShelf(self):
        has = not (self._currentShelf is None)
        return has

    # Code from template association_GetOne 
    def getCurrentCheeseWheel(self):
        return self._currentCheeseWheel

    def hasCurrentCheeseWheel(self):
        has = not (self._currentCheeseWheel is None)
        return has

    # Code from template association_GetMany 
    def getLog1(self, index):
        aLog = self._log[index]
        return aLog

    def getLog2(self):
        newLog = tuple(self._log)
        return newLog

    def numberOfLog(self):
        number = len(self._log)
        return number

    def hasLog(self):
        has = len(self._log) > 0
        return has

    def indexOfLog(self, aLog):
        index = (-1 if not aLog in self._log else self._log.index(aLog))
        return index

    # Code from template association_GetOne 
    def getCheECSEManager(self):
        return self._cheECSEManager

    # Code from template association_SetOptionalOneToOptionalOne 
    def setCurrentShelf(self, aNewCurrentShelf):
        wasSet = False
        if aNewCurrentShelf is None :
            existingCurrentShelf = self._currentShelf
            self._currentShelf = None
            if not (existingCurrentShelf is None) and not (existingCurrentShelf.getRobot() is None) :
                existingCurrentShelf.setRobot(None)
            wasSet = True
            return wasSet
        currentCurrentShelf = self.getCurrentShelf()
        if not (currentCurrentShelf is None) and not currentCurrentShelf == aNewCurrentShelf :
            currentCurrentShelf.setRobot(None)
        self._currentShelf = aNewCurrentShelf
        existingRobot = aNewCurrentShelf.getRobot()
        if not self == existingRobot :
            aNewCurrentShelf.setRobot(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToOptionalOne 
    def setCurrentCheeseWheel(self, aNewCurrentCheeseWheel):
        wasSet = False
        if aNewCurrentCheeseWheel is None :
            existingCurrentCheeseWheel = self._currentCheeseWheel
            self._currentCheeseWheel = None
            if not (existingCurrentCheeseWheel is None) and not (existingCurrentCheeseWheel.getRobot() is None) :
                existingCurrentCheeseWheel.setRobot(None)
            wasSet = True
            return wasSet
        currentCurrentCheeseWheel = self.getCurrentCheeseWheel()
        if not (currentCurrentCheeseWheel is None) and not currentCurrentCheeseWheel == aNewCurrentCheeseWheel :
            currentCurrentCheeseWheel.setRobot(None)
        self._currentCheeseWheel = aNewCurrentCheeseWheel
        existingRobot = aNewCurrentCheeseWheel.getRobot()
        if not self == existingRobot :
            aNewCurrentCheeseWheel.setRobot(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfLog():
        return 0

    # Code from template association_AddManyToOne 
    def addLog1(self, aDescription):
        from ..generated_model_layer.LogEntry import LogEntry
        return LogEntry(aDescription, self)

    def addLog2(self, aLog):
        wasAdded = False
        if (aLog) in self._log :
            return False
        existingRobot = aLog.getRobot()
        isNewRobot = not (existingRobot is None) and not self == existingRobot
        if isNewRobot :
            aLog.setRobot(self)
        else :
            self._log.append(aLog)
        wasAdded = True
        return wasAdded

    def removeLog(self, aLog):
        wasRemoved = False
        #Unable to remove aLog, as it must always have a robot
        if not self == aLog.getRobot() :
            self._log.remove(aLog)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addLogAt(self, aLog, index):
        wasAdded = False
        if self.addLog(aLog) :
            if index < 0 :
                index = 0
            if index > self.numberOfLog() :
                index = self.numberOfLog() - 1
            self._log.remove(aLog)
            self._log.insert(index, aLog)
            wasAdded = True
        return wasAdded

    def addOrMoveLogAt(self, aLog, index):
        wasAdded = False
        if (aLog) in self._log :
            if index < 0 :
                index = 0
            if index > self.numberOfLog() :
                index = self.numberOfLog() - 1
            self._log.remove(aLog)
            self._log.insert(index, aLog)
            wasAdded = True
        else :
            wasAdded = self.addLogAt(aLog, index)
        return wasAdded

    # Code from template association_SetOneToOptionalOne 
    def setCheECSEManager(self, aNewCheECSEManager):
        wasSet = False
        if aNewCheECSEManager is None :
            #Unable to setCheECSEManager to null, as robot must always be associated to a cheECSEManager
            return wasSet
        existingRobot = aNewCheECSEManager.getRobot()
        if not (existingRobot is None) and not self == existingRobot :
            #Unable to setCheECSEManager, the current cheECSEManager already has a robot, which would be orphaned if it were re-assigned
            return wasSet
        anOldCheECSEManager = self._cheECSEManager
        self._cheECSEManager = aNewCheECSEManager
        self._cheECSEManager.setRobot(self)
        if not (anOldCheECSEManager is None) :
            anOldCheECSEManager.setRobot(None)
        wasSet = True
        return wasSet

    def delete(self):
        if not (self._currentShelf is None) :
            self._currentShelf.setRobot(None)
        if not (self._currentCheeseWheel is None) :
            self._currentCheeseWheel.setRobot(None)

        while len(self._log) > 0 :
            aLog = self._log[len(self._log) - 1]
            aLog.delete()
            self._log.remove(aLog)

        existingCheECSEManager = self._cheECSEManager
        self._cheECSEManager = None
        if not (existingCheECSEManager is None) :
            existingCheECSEManager.setRobot(None)

    def __str__(self):
        return str(super().__str__()) + "[" + "isFacingAisle" + ":" + str(self.getIsFacingAisle()) + "]" + str(os.linesep) + "  " + "currentShelf = " + str(((format(id(self.getCurrentShelf()), "x")) if not (self.getCurrentShelf() is None) else "null")) + str(os.linesep) + "  " + "currentCheeseWheel = " + str(((format(id(self.getCurrentCheeseWheel()), "x")) if not (self.getCurrentCheeseWheel() is None) else "null")) + str(os.linesep) + "  " + "cheECSEManager = " + ((format(id(self.getCheECSEManager()), "x")) if not (self.getCheECSEManager() is None) else "null")

    def getLog(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getLog1(argv[0])
        if len(argv) == 0 :
            return self.getLog2()
        raise TypeError("No method matches provided parameters")

    def addLog(self, *argv):
        from ..generated_model_layer.LogEntry import LogEntry
        if len(argv) == 1 and isinstance(argv[0], str) :
            return self.addLog1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], LogEntry) :
            return self.addLog2(argv[0])
        raise TypeError("No method matches provided parameters")

