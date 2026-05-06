# %% NEW FILE BTMS BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 4 "../../../../../model.ump"
# line 41 "../../../../../model.ump"
from datetime import date

class BusTransportationManagementSystem():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #BTMS Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._schedules = None
        self._drivers = None
        self._assignments = None
        self._routes = None
        self._vehicles = None
        self._vehicles = []
        self._routes = []
        self._assignments = []
        self._drivers = []
        self._schedules = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany
    def getVehicle(self, index):
        aVehicle = self._vehicles[index]
        return aVehicle

    def getVehicles(self):
        newVehicles = tuple(self._vehicles)
        return newVehicles

    def numberOfVehicles(self):
        number = len(self._vehicles)
        return number

    def hasVehicles(self):
        has = len(self._vehicles) > 0
        return has

    def indexOfVehicle(self, aVehicle):
        index = (-1 if not aVehicle in self._vehicles else self._vehicles.index(aVehicle))
        return index

    # Code from template association_GetMany
    def getRoute(self, index):
        aRoute = self._routes[index]
        return aRoute

    def getRoutes(self):
        newRoutes = tuple(self._routes)
        return newRoutes

    def numberOfRoutes(self):
        number = len(self._routes)
        return number

    def hasRoutes(self):
        has = len(self._routes) > 0
        return has

    def indexOfRoute(self, aRoute):
        index = (-1 if not aRoute in self._routes else self._routes.index(aRoute))
        return index

    # Code from template association_GetMany
    def getAssignment(self, index):
        aAssignment = self._assignments[index]
        return aAssignment

    def getAssignments(self):
        newAssignments = tuple(self._assignments)
        return newAssignments

    def numberOfAssignments(self):
        number = len(self._assignments)
        return number

    def hasAssignments(self):
        has = len(self._assignments) > 0
        return has

    def indexOfAssignment(self, aAssignment):
        index = (-1 if not aAssignment in self._assignments else self._assignments.index(aAssignment))
        return index

    # Code from template association_GetMany
    def getDriver(self, index):
        aDriver = self._drivers[index]
        return aDriver

    def getDrivers(self):
        newDrivers = tuple(self._drivers)
        return newDrivers

    def numberOfDrivers(self):
        number = len(self._drivers)
        return number

    def hasDrivers(self):
        has = len(self._drivers) > 0
        return has

    def indexOfDriver(self, aDriver):
        index = (-1 if not aDriver in self._drivers else self._drivers.index(aDriver))
        return index

    # Code from template association_GetMany
    def getSchedule(self, index):
        aSchedule = self._schedules[index]
        return aSchedule

    def getSchedules(self):
        newSchedules = tuple(self._schedules)
        return newSchedules

    def numberOfSchedules(self):
        number = len(self._schedules)
        return number

    def hasSchedules(self):
        has = len(self._schedules) > 0
        return has

    def indexOfSchedule(self, aSchedule):
        index = (-1 if not aSchedule in self._schedules else self._schedules.index(aSchedule))
        return index

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfVehicles():
        return 0

    # Code from template association_AddManyToOne
    def addVehicle1(self, aLicencePlate):
        from . import BusVehicle
        return BusVehicle(aLicencePlate, self)

    def addVehicle2(self, aVehicle):
        wasAdded = False
        if (aVehicle) in self._vehicles :
            return False
        existingBTMS = aVehicle.getBTMS()
        isNewBTMS = not (existingBTMS is None) and not self == existingBTMS
        if isNewBTMS :
            aVehicle.setBTMS(self)
        else :
            self._vehicles.append(aVehicle)
        wasAdded = True
        return wasAdded

    def removeVehicle(self, aVehicle):
        wasRemoved = False
        #Unable to remove aVehicle, as it must always have a bTMS
        if not self == aVehicle.getBTMS() :
            self._vehicles.remove(aVehicle)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addVehicleAt(self, aVehicle, index):
        wasAdded = False
        if self.addVehicle(aVehicle) :
            if index < 0 :
                index = 0
            if index > self.numberOfVehicles() :
                index = self.numberOfVehicles() - 1
            self._vehicles.remove(aVehicle)
            self._vehicles.insert(index, aVehicle)
            wasAdded = True
        return wasAdded

    def addOrMoveVehicleAt(self, aVehicle, index):
        wasAdded = False
        if (aVehicle) in self._vehicles :
            if index < 0 :
                index = 0
            if index > self.numberOfVehicles() :
                index = self.numberOfVehicles() - 1
            self._vehicles.remove(aVehicle)
            self._vehicles.insert(index, aVehicle)
            wasAdded = True
        else :
            wasAdded = self.addVehicleAt(aVehicle, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfRoutes():
        return 0

    # Code from template association_AddManyToOne
    def addRoute1(self, aNumber):
        from . import Route
        return Route(aNumber, self)

    def addRoute2(self, aRoute):
        wasAdded = False
        if (aRoute) in self._routes :
            return False
        existingBTMS = aRoute.getBTMS()
        isNewBTMS = not (existingBTMS is None) and not self == existingBTMS
        if isNewBTMS :
            aRoute.setBTMS(self)
        else :
            self._routes.append(aRoute)
        wasAdded = True
        return wasAdded

    def removeRoute(self, aRoute):
        wasRemoved = False
        #Unable to remove aRoute, as it must always have a bTMS
        if not self == aRoute.getBTMS() :
            self._routes.remove(aRoute)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addRouteAt(self, aRoute, index):
        wasAdded = False
        if self.addRoute(aRoute) :
            if index < 0 :
                index = 0
            if index > self.numberOfRoutes() :
                index = self.numberOfRoutes() - 1
            self._routes.remove(aRoute)
            self._routes.insert(index, aRoute)
            wasAdded = True
        return wasAdded

    def addOrMoveRouteAt(self, aRoute, index):
        wasAdded = False
        if (aRoute) in self._routes :
            if index < 0 :
                index = 0
            if index > self.numberOfRoutes() :
                index = self.numberOfRoutes() - 1
            self._routes.remove(aRoute)
            self._routes.insert(index, aRoute)
            wasAdded = True
        else :
            wasAdded = self.addRouteAt(aRoute, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfAssignments():
        return 0

    # Code from template association_AddManyToOne
    def addAssignment1(self, aDate, aBus, aRoute):
        from . import RouteAssignment
        return RouteAssignment(aDate, aBus, aRoute, self)

    def addAssignment2(self, aAssignment):
        wasAdded = False
        if (aAssignment) in self._assignments :
            return False
        existingBTMS = aAssignment.getBTMS()
        isNewBTMS = not (existingBTMS is None) and not self == existingBTMS
        if isNewBTMS :
            aAssignment.setBTMS(self)
        else :
            self._assignments.append(aAssignment)
        wasAdded = True
        return wasAdded

    def removeAssignment(self, aAssignment):
        wasRemoved = False
        #Unable to remove aAssignment, as it must always have a bTMS
        if not self == aAssignment.getBTMS() :
            self._assignments.remove(aAssignment)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addAssignmentAt(self, aAssignment, index):
        wasAdded = False
        if self.addAssignment(aAssignment) :
            if index < 0 :
                index = 0
            if index > self.numberOfAssignments() :
                index = self.numberOfAssignments() - 1
            self._assignments.remove(aAssignment)
            self._assignments.insert(index, aAssignment)
            wasAdded = True
        return wasAdded

    def addOrMoveAssignmentAt(self, aAssignment, index):
        wasAdded = False
        if (aAssignment) in self._assignments :
            if index < 0 :
                index = 0
            if index > self.numberOfAssignments() :
                index = self.numberOfAssignments() - 1
            self._assignments.remove(aAssignment)
            self._assignments.insert(index, aAssignment)
            wasAdded = True
        else :
            wasAdded = self.addAssignmentAt(aAssignment, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfDrivers():
        return 0

    # Code from template association_AddManyToOne
    def addDriver1(self, aName):
        from . import Driver
        return Driver(aName, self)

    def addDriver2(self, aDriver):
        wasAdded = False
        if (aDriver) in self._drivers :
            return False
        existingBTMS = aDriver.getBTMS()
        isNewBTMS = not (existingBTMS is None) and not self == existingBTMS
        if isNewBTMS :
            aDriver.setBTMS(self)
        else :
            self._drivers.append(aDriver)
        wasAdded = True
        return wasAdded

    def removeDriver(self, aDriver):
        wasRemoved = False
        #Unable to remove aDriver, as it must always have a bTMS
        if not self == aDriver.getBTMS() :
            self._drivers.remove(aDriver)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addDriverAt(self, aDriver, index):
        wasAdded = False
        if self.addDriver(aDriver) :
            if index < 0 :
                index = 0
            if index > self.numberOfDrivers() :
                index = self.numberOfDrivers() - 1
            self._drivers.remove(aDriver)
            self._drivers.insert(index, aDriver)
            wasAdded = True
        return wasAdded

    def addOrMoveDriverAt(self, aDriver, index):
        wasAdded = False
        if (aDriver) in self._drivers :
            if index < 0 :
                index = 0
            if index > self.numberOfDrivers() :
                index = self.numberOfDrivers() - 1
            self._drivers.remove(aDriver)
            self._drivers.insert(index, aDriver)
            wasAdded = True
        else :
            wasAdded = self.addDriverAt(aDriver, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfSchedules():
        return 0

    # Code from template association_AddManyToOne
    def addSchedule1(self, aShift, aDriver, aAssignment):
        from . import DriverSchedule
        return DriverSchedule(aShift, aDriver, aAssignment, self)

    def addSchedule2(self, aSchedule):
        wasAdded = False
        if (aSchedule) in self._schedules :
            return False
        existingBTMS = aSchedule.getBTMS()
        isNewBTMS = not (existingBTMS is None) and not self == existingBTMS
        if isNewBTMS :
            aSchedule.setBTMS(self)
        else :
            self._schedules.append(aSchedule)
        wasAdded = True
        return wasAdded

    def removeSchedule(self, aSchedule):
        wasRemoved = False
        #Unable to remove aSchedule, as it must always have a bTMS
        if not self == aSchedule.getBTMS() :
            self._schedules.remove(aSchedule)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addScheduleAt(self, aSchedule, index):
        wasAdded = False
        if self.addSchedule(aSchedule) :
            if index < 0 :
                index = 0
            if index > self.numberOfSchedules() :
                index = self.numberOfSchedules() - 1
            self._schedules.remove(aSchedule)
            self._schedules.insert(index, aSchedule)
            wasAdded = True
        return wasAdded

    def addOrMoveScheduleAt(self, aSchedule, index):
        wasAdded = False
        if (aSchedule) in self._schedules :
            if index < 0 :
                index = 0
            if index > self.numberOfSchedules() :
                index = self.numberOfSchedules() - 1
            self._schedules.remove(aSchedule)
            self._schedules.insert(index, aSchedule)
            wasAdded = True
        else :
            wasAdded = self.addScheduleAt(aSchedule, index)
        return wasAdded

    def delete(self):

        while len(self._vehicles) > 0 :
            aVehicle = self._vehicles[len(self._vehicles) - 1]
            aVehicle.delete()
            self._vehicles.remove(aVehicle)

        while len(self._routes) > 0 :
            aRoute = self._routes[len(self._routes) - 1]
            aRoute.delete()
            self._routes.remove(aRoute)

        while len(self._assignments) > 0 :
            aAssignment = self._assignments[len(self._assignments) - 1]
            aAssignment.delete()
            self._assignments.remove(aAssignment)

        while len(self._drivers) > 0 :
            aDriver = self._drivers[len(self._drivers) - 1]
            aDriver.delete()
            self._drivers.remove(aDriver)

        while len(self._schedules) > 0 :
            aSchedule = self._schedules[len(self._schedules) - 1]
            aSchedule.delete()
            self._schedules.remove(aSchedule)

    def addVehicle(self, *argv):
        from . import BusVehicle
        if len(argv) == 1 and isinstance(argv[0], str) :
            return self.addVehicle1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], BusVehicle) :
            return self.addVehicle2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addRoute(self, *argv):
        from . import Route
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.addRoute1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], Route) :
            return self.addRoute2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addAssignment(self, *argv):
        from . import RouteAssignment
        from . import Route
        from . import BusVehicle
        if len(argv) == 3 and isinstance(argv[0], date) and isinstance(argv[1], BusVehicle) and isinstance(argv[2], Route) :
            return self.addAssignment1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], RouteAssignment) :
            return self.addAssignment2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addDriver(self, *argv):
        from . import Driver
        if len(argv) == 1 and isinstance(argv[0], str) :
            return self.addDriver1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], Driver) :
            return self.addDriver2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addSchedule(self, *argv):
        from . import DriverSchedule
        from . import Driver
        from . import RouteAssignment
        if len(argv) == 3 and isinstance(argv[0], DriverSchedule.Shift) and isinstance(argv[1], Driver) and isinstance(argv[2], RouteAssignment) :
            return self.addSchedule1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], DriverSchedule) :
            return self.addSchedule2(argv[0])
        raise TypeError("No method matches provided parameters")
