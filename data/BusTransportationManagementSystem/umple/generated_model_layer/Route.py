# %% NEW FILE Route BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 16 "../../../../../model.ump"
# line 51 "../../../../../model.ump"
import os
from datetime import date

class Route():
    routesByNumber = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Route Attributes
    #Route Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aNumber, aBTMS):
        self._routeAssignments = None
        self._bTMS = None
        self._number = None
        if not self.setNumber(aNumber) :
            raise RuntimeError ("Cannot create due to duplicate number. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        didAddBTMS = self.setBTMS(aBTMS)
        if not didAddBTMS :
            raise RuntimeError ("Unable to create route due to bTMS. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._routeAssignments = []

    #------------------------
    # INTERFACE
    #------------------------
    def setNumber(self, aNumber):
        wasSet = False
        anOldNumber = self.getNumber()
        if not (anOldNumber is None) and anOldNumber == aNumber :
            return True
        if Route.hasWithNumber(aNumber) :
            return wasSet
        self._number = aNumber
        wasSet = True
        if not (anOldNumber is None) :
            Route.routesByNumber.pop(anOldNumber, None)
        Route.routesByNumber[aNumber] = self
        return wasSet

    def getNumber(self):
        return self._number

    # Code from template attribute_GetUnique
    @staticmethod
    def getWithNumber(aNumber):
        return Route.routesByNumber.get(aNumber)

    # Code from template attribute_HasUnique
    @staticmethod
    def hasWithNumber(aNumber):
        return not (Route.getWithNumber(aNumber) is None)

    # Code from template association_GetOne
    def getBTMS(self):
        return self._bTMS

    # Code from template association_GetMany
    def getRouteAssignment(self, index):
        aRouteAssignment = self._routeAssignments[index]
        return aRouteAssignment

    def getRouteAssignments(self):
        newRouteAssignments = tuple(self._routeAssignments)
        return newRouteAssignments

    def numberOfRouteAssignments(self):
        self._number = len(self._routeAssignments)
        return self._number

    def hasRouteAssignments(self):
        has = len(self._routeAssignments) > 0
        return has

    def indexOfRouteAssignment(self, aRouteAssignment):
        index = (-1 if not aRouteAssignment in self._routeAssignments else self._routeAssignments.index(aRouteAssignment))
        return index

    # Code from template association_SetOneToMany
    def setBTMS(self, aBTMS):
        wasSet = False
        if aBTMS is None :
            return wasSet
        existingBTMS = self._bTMS
        self._bTMS = aBTMS
        if not (existingBTMS is None) and not existingBTMS == aBTMS :
            existingBTMS.removeRoute(self)
        self._bTMS.addRoute(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfRouteAssignments():
        return 0

    # Code from template association_AddManyToOne
    def addRouteAssignment1(self, aDate, aBus, aBTMS):
        from . import RouteAssignment
        return RouteAssignment(aDate, aBus, self, aBTMS)

    def addRouteAssignment2(self, aRouteAssignment):
        wasAdded = False
        if (aRouteAssignment) in self._routeAssignments :
            return False
        existingRoute = aRouteAssignment.getRoute()
        isNewRoute = not (existingRoute is None) and not self == existingRoute
        if isNewRoute :
            aRouteAssignment.setRoute(self)
        else :
            self._routeAssignments.append(aRouteAssignment)
        wasAdded = True
        return wasAdded

    def removeRouteAssignment(self, aRouteAssignment):
        wasRemoved = False
        #Unable to remove aRouteAssignment, as it must always have a route
        if not self == aRouteAssignment.getRoute() :
            self._routeAssignments.remove(aRouteAssignment)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addRouteAssignmentAt(self, aRouteAssignment, index):
        wasAdded = False
        if self.addRouteAssignment(aRouteAssignment) :
            if index < 0 :
                index = 0
            if index > self.numberOfRouteAssignments() :
                index = self.numberOfRouteAssignments() - 1
            self._routeAssignments.remove(aRouteAssignment)
            self._routeAssignments.insert(index, aRouteAssignment)
            wasAdded = True
        return wasAdded

    def addOrMoveRouteAssignmentAt(self, aRouteAssignment, index):
        wasAdded = False
        if (aRouteAssignment) in self._routeAssignments :
            if index < 0 :
                index = 0
            if index > self.numberOfRouteAssignments() :
                index = self.numberOfRouteAssignments() - 1
            self._routeAssignments.remove(aRouteAssignment)
            self._routeAssignments.insert(index, aRouteAssignment)
            wasAdded = True
        else :
            wasAdded = self.addRouteAssignmentAt(aRouteAssignment, index)
        return wasAdded

    def delete(self):
        Route.routesByNumber.pop(self.getNumber(), None)
        placeholderBTMS = self._bTMS
        self._bTMS = None
        if not (placeholderBTMS is None) :
            placeholderBTMS.removeRoute(self)
        i = len(self._routeAssignments)
        while i > 0 :
            aRouteAssignment = self._routeAssignments[i - 1]
            aRouteAssignment.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "number" + ":" + str(self.getNumber()) + "]" + str(os.linesep) + "  " + "bTMS = " + ((format(id(self.getBTMS()), "x")) if not (self.getBTMS() is None) else "null")

    def addRouteAssignment(self, *argv):
        from . import RouteAssignment
        from . import BusTransportationManagementSystem
        from . import BusVehicle
        if len(argv) == 3 and isinstance(argv[0], date) and isinstance(argv[1], BusVehicle) and isinstance(argv[2], BusTransportationManagementSystem) :
            return self.addRouteAssignment1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], RouteAssignment) :
            return self.addRouteAssignment2(argv[0])
        raise TypeError("No method matches provided parameters")