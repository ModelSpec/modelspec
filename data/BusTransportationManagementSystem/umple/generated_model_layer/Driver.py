# %% NEW FILE Driver BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 26 "../../../../../model.ump"
# line 61 "../../../../../model.ump"
import os

class Driver():
    nextId = 1
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Driver Attributes
    #Autounique Attributes
    #Driver Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aBTMS):
        self._driverSchedules = None
        self._bTMS = None
        self._id = None
        self._name = None
        self._name = aName
        self._id, Driver.nextId = Driver.nextId, Driver.nextId + 1
        didAddBTMS = self.setBTMS(aBTMS)
        if not didAddBTMS :
            raise RuntimeError ("Unable to create driver due to bTMS. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._driverSchedules = []

    #------------------------
    # INTERFACE
    #------------------------
    def setName(self, aName):
        wasSet = False
        self._name = aName
        wasSet = True
        return wasSet

    def getName(self):
        return self._name

    def getId(self):
        return self._id

    # Code from template association_GetOne
    def getBTMS(self):
        return self._bTMS

    # Code from template association_GetMany
    def getDriverSchedule(self, index):
        aDriverSchedule = self._driverSchedules[index]
        return aDriverSchedule

    def getDriverSchedules(self):
        newDriverSchedules = tuple(self._driverSchedules)
        return newDriverSchedules

    def numberOfDriverSchedules(self):
        number = len(self._driverSchedules)
        return number

    def hasDriverSchedules(self):
        has = len(self._driverSchedules) > 0
        return has

    def indexOfDriverSchedule(self, aDriverSchedule):
        index = (-1 if not aDriverSchedule in self._driverSchedules else self._driverSchedules.index(aDriverSchedule))
        return index

    # Code from template association_SetOneToMany
    def setBTMS(self, aBTMS):
        wasSet = False
        if aBTMS is None :
            return wasSet
        existingBTMS = self._bTMS
        self._bTMS = aBTMS
        if not (existingBTMS is None) and not existingBTMS == aBTMS :
            existingBTMS.removeDriver(self)
        self._bTMS.addDriver(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfDriverSchedules():
        return 0

    # Code from template association_AddManyToOne
    def addDriverSchedule1(self, aShift, aAssignment, aBTMS):
        from . import DriverSchedule
        return DriverSchedule(aShift, self, aAssignment, aBTMS)

    def addDriverSchedule2(self, aDriverSchedule):
        wasAdded = False
        if (aDriverSchedule) in self._driverSchedules :
            return False
        existingDriver = aDriverSchedule.getDriver()
        isNewDriver = not (existingDriver is None) and not self == existingDriver
        if isNewDriver :
            aDriverSchedule.setDriver(self)
        else :
            self._driverSchedules.append(aDriverSchedule)
        wasAdded = True
        return wasAdded

    def removeDriverSchedule(self, aDriverSchedule):
        wasRemoved = False
        #Unable to remove aDriverSchedule, as it must always have a driver
        if not self == aDriverSchedule.getDriver() :
            self._driverSchedules.remove(aDriverSchedule)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addDriverScheduleAt(self, aDriverSchedule, index):
        wasAdded = False
        if self.addDriverSchedule(aDriverSchedule) :
            if index < 0 :
                index = 0
            if index > self.numberOfDriverSchedules() :
                index = self.numberOfDriverSchedules() - 1
            self._driverSchedules.remove(aDriverSchedule)
            self._driverSchedules.insert(index, aDriverSchedule)
            wasAdded = True
        return wasAdded

    def addOrMoveDriverScheduleAt(self, aDriverSchedule, index):
        wasAdded = False
        if (aDriverSchedule) in self._driverSchedules :
            if index < 0 :
                index = 0
            if index > self.numberOfDriverSchedules() :
                index = self.numberOfDriverSchedules() - 1
            self._driverSchedules.remove(aDriverSchedule)
            self._driverSchedules.insert(index, aDriverSchedule)
            wasAdded = True
        else :
            wasAdded = self.addDriverScheduleAt(aDriverSchedule, index)
        return wasAdded

    def delete(self):
        placeholderBTMS = self._bTMS
        self._bTMS = None
        if not (placeholderBTMS is None) :
            placeholderBTMS.removeDriver(self)
        i = len(self._driverSchedules)
        while i > 0 :
            aDriverSchedule = self._driverSchedules[i - 1]
            aDriverSchedule.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "," + "name" + ":" + str(self.getName()) + "]" + str(os.linesep) + "  " + "bTMS = " + ((format(id(self.getBTMS()), "x")) if not (self.getBTMS() is None) else "null")

    def addDriverSchedule(self, *argv):
        from . import DriverSchedule
        from . import BusTransportationManagementSystem
        from . import RouteAssignment
        if len(argv) == 3 and isinstance(argv[0], DriverSchedule.Shift) and isinstance(argv[1], RouteAssignment) and isinstance(argv[2], BTMS) :
            return self.addDriverSchedule1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], DriverSchedule) :
            return self.addDriverSchedule2(argv[0])
        raise TypeError("No method matches provided parameters")
