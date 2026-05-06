# %% NEW FILE House BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8183.32a6408a9 modeling language!
# line 25 "model.ump"
# line 96 "model.ump"
import os
from enum import Enum, auto

class House():
    #------------------------
    # ENUMERATIONS
    #------------------------
    class BMType(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        WOOD = auto()
        BRICK = auto()
        CONCRETE = auto()

    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #House Attributes
    #House Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aAddress, aBuildingMaterial):
        self._basement = None
        self._jobLogs = None
        self._BuildingMaterial = None
        self._Address = None
        self._Address = aAddress
        self._BuildingMaterial = aBuildingMaterial
        self._jobLogs = []

    #------------------------
    # INTERFACE
    #------------------------
    def setAddress(self, aAddress):
        wasSet = False
        self._Address = aAddress
        wasSet = True
        return wasSet

    def setBuildingMaterial(self, aBuildingMaterial):
        wasSet = False
        self._BuildingMaterial = aBuildingMaterial
        wasSet = True
        return wasSet

    def getAddress(self):
        return self._Address

    def getBuildingMaterial(self):
        return self._BuildingMaterial

    # Code from template association_GetMany 
    def getJobLog(self, index):
        aJobLog = self._jobLogs[index]
        return aJobLog

    def getJobLogs(self):
        newJobLogs = tuple(self._jobLogs)
        return newJobLogs

    def numberOfJobLogs(self):
        number = len(self._jobLogs)
        return number

    def hasJobLogs(self):
        has = len(self._jobLogs) > 0
        return has

    def indexOfJobLog(self, aJobLog):
        index = (-1 if not aJobLog in self._jobLogs else self._jobLogs.index(aJobLog))
        return index

    # Code from template association_GetOne 
    def getBasement(self):
        return self._basement

    def hasBasement(self):
        has = not (self._basement is None)
        return has

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfJobLogs():
        return 0

    # Code from template association_AddManyToOne 
    def addJobLog1(self, aHours, aPrice, aCompany):
        from .JobLog import JobLog
        return JobLog(aHours, aPrice, self, aCompany)

    def addJobLog2(self, aJobLog):
        wasAdded = False
        if (aJobLog) in self._jobLogs :
            return False
        existingHouse = aJobLog.getHouse()
        isNewHouse = not (existingHouse is None) and not self == existingHouse
        if isNewHouse :
            aJobLog.setHouse(self)
        else :
            self._jobLogs.append(aJobLog)
        wasAdded = True
        return wasAdded

    def removeJobLog(self, aJobLog):
        wasRemoved = False
        #Unable to remove aJobLog, as it must always have a house
        if not self == aJobLog.getHouse() :
            self._jobLogs.remove(aJobLog)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addJobLogAt(self, aJobLog, index):
        wasAdded = False
        if self.addJobLog(aJobLog) :
            if index < 0 :
                index = 0
            if index > self.numberOfJobLogs() :
                index = self.numberOfJobLogs() - 1
            self._jobLogs.remove(aJobLog)
            self._jobLogs.insert(index, aJobLog)
            wasAdded = True
        return wasAdded

    def addOrMoveJobLogAt(self, aJobLog, index):
        wasAdded = False
        if (aJobLog) in self._jobLogs :
            if index < 0 :
                index = 0
            if index > self.numberOfJobLogs() :
                index = self.numberOfJobLogs() - 1
            self._jobLogs.remove(aJobLog)
            self._jobLogs.insert(index, aJobLog)
            wasAdded = True
        else :
            wasAdded = self.addJobLogAt(aJobLog, index)
        return wasAdded

    # Code from template association_SetOptionalOneToOne 
    def setBasement(self, aNewBasement):
        wasSet = False
        if not (self._basement is None) and not self._basement == aNewBasement and self == self._basement.getHouse() :
            #Unable to setBasement, as existing basement would become an orphan
            return wasSet
        self._basement = aNewBasement
        anOldHouse = (aNewBasement.getHouse()) if not (aNewBasement is None) else None
        if not self == anOldHouse :
            if not (anOldHouse is None) :
                anOldHouse.basement = None
            if not (self._basement is None) :
                self._basement.setHouse(self)
        wasSet = True
        return wasSet

    def delete(self):
        i = len(self._jobLogs)
        while i > 0 :
            aJobLog = self._jobLogs[i - 1]
            aJobLog.delete()
            i -= 1

        existingBasement = self._basement
        self._basement = None
        if not (existingBasement is None) :
            existingBasement.delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "Address" + ":" + str(self.getAddress()) + "]" + str(os.linesep) + "  " + "BuildingMaterial" + "=" + str((((self.getBuildingMaterial().__str__().replaceAll("  ", "    ")) if not self.getBuildingMaterial() == self else "this") if not (self.getBuildingMaterial() is None) else "null")) + str(os.linesep) + "  " + "basement = " + ((format(id(self.getBasement()), "x")) if not (self.getBasement() is None) else "null")

    def addJobLog(self, *argv):
        from .Company import Company
        from .JobLog import JobLog
        if len(argv) == 3 and isinstance(argv[0], int) and isinstance(argv[1], (float, int)) and isinstance(argv[2], Company) :
            return self.addJobLog1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], JobLog) :
            return self.addJobLog2(argv[0])
        raise TypeError("No method matches provided parameters")
