# %% NEW FILE RouteAssignment BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 20 "../../../../../model.ump"
# line 56 "../../../../../model.ump"
import os
from datetime import date

class RouteAssignment():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #RouteAssignment Attributes
    #RouteAssignment Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aDate, aBus, aRoute, aBTMS):
        self._driverSchedules = None
        self._bTMS = None
        self._route = None
        self._bus = None
        self._date = None
        self._date = aDate
        didAddBus = self.setBus(aBus)
        if not didAddBus :
            raise RuntimeError ("Unable to create routeAssignment due to bus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddRoute = self.setRoute(aRoute)
        if not didAddRoute :
            raise RuntimeError ("Unable to create routeAssignment due to route. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddBTMS = self.setBTMS(aBTMS)
        if not didAddBTMS :
            raise RuntimeError ("Unable to create assignment due to bTMS. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._driverSchedules = []

    #------------------------
    # INTERFACE
    #------------------------
    def setDate(self, aDate):
        wasSet = False
        self._date = aDate
        wasSet = True
        return wasSet

    def getDate(self):
        return self._date

    # Code from template association_GetOne
    def getBus(self):
        return self._bus

    # Code from template association_GetOne
    def getRoute(self):
        return self._route

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
    def setBus(self, aBus):
        wasSet = False
        if aBus is None :
            return wasSet
        existingBus = self._bus
        self._bus = aBus
        if not (existingBus is None) and not existingBus == aBus :
            existingBus.removeRouteAssignment(self)
        self._bus.addRouteAssignment(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setRoute(self, aRoute):
        wasSet = False
        if aRoute is None :
            return wasSet
        existingRoute = self._route
        self._route = aRoute
        if not (existingRoute is None) and not existingRoute == aRoute :
            existingRoute.removeRouteAssignment(self)
        self._route.addRouteAssignment(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setBTMS(self, aBTMS):
        wasSet = False
        if aBTMS is None :
            return wasSet
        existingBTMS = self._bTMS
        self._bTMS = aBTMS
        if not (existingBTMS is None) and not existingBTMS == aBTMS :
            existingBTMS.removeAssignment(self)
        self._bTMS.addAssignment(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfDriverSchedules():
        return 0

    # Code from template association_AddManyToOne
    def addDriverSchedule1(self, aShift, aDriver, aBTMS):
        from . import DriverSchedule
        return DriverSchedule(aShift, aDriver, self, aBTMS)

    def addDriverSchedule2(self, aDriverSchedule):
        wasAdded = False
        if (aDriverSchedule) in self._driverSchedules :
            return False
        existingAssignment = aDriverSchedule.getAssignment()
        isNewAssignment = not (existingAssignment is None) and not self == existingAssignment
        if isNewAssignment :
            aDriverSchedule.setAssignment(self)
        else :
            self._driverSchedules.append(aDriverSchedule)
        wasAdded = True
        return wasAdded

    def removeDriverSchedule(self, aDriverSchedule):
        wasRemoved = False
        #Unable to remove aDriverSchedule, as it must always have a assignment
        if not self == aDriverSchedule.getAssignment() :
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
        placeholderBus = self._bus
        self._bus = None
        if not (placeholderBus is None) :
            placeholderBus.removeRouteAssignment(self)
        placeholderRoute = self._route
        self._route = None
        if not (placeholderRoute is None) :
            placeholderRoute.removeRouteAssignment(self)
        placeholderBTMS = self._bTMS
        self._bTMS = None
        if not (placeholderBTMS is None) :
            placeholderBTMS.removeAssignment(self)
        i = len(self._driverSchedules)
        while i > 0 :
            aDriverSchedule = self._driverSchedules[i - 1]
            aDriverSchedule.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "]" + str(os.linesep) + "  " + "date" + "=" + str((((self.getDate().__str__().replaceAll("  ", "    ")) if not self.getDate() == self else "this") if not (self.getDate() is None) else "null")) + str(os.linesep) + "  " + "bus = " + str(((format(id(self.getBus()), "x")) if not (self.getBus() is None) else "null")) + str(os.linesep) + "  " + "route = " + str(((format(id(self.getRoute()), "x")) if not (self.getRoute() is None) else "null")) + str(os.linesep) + "  " + "bTMS = " + ((format(id(self.getBTMS()), "x")) if not (self.getBTMS() is None) else "null")

    def addDriverSchedule(self, *argv):
        from . import DriverSchedule
        from . import BusTransportationManagementSystem
        from . import Driver
        if len(argv) == 3 and isinstance(argv[0], DriverSchedule.Shift) and isinstance(argv[1], Driver) and isinstance(argv[2], BTMS) :
            return self.addDriverSchedule1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], DriverSchedule) :
            return self.addDriverSchedule2(argv[0])
        raise TypeError("No method matches provided parameters")
