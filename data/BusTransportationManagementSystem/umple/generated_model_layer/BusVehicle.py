# %% NEW FILE BusVehicle BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 12 "../../../../../model.ump"
# line 46 "../../../../../model.ump"
import os
from datetime import date

class BusVehicle():
    busvehiclesByLicencePlate = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #BusVehicle Attributes
    #BusVehicle Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aLicencePlate, aBTMS):
        self._routeAssignments = None
        self._bTMS = None
        self._licencePlate = None
        if not self.setLicencePlate(aLicencePlate) :
            raise RuntimeError ("Cannot create due to duplicate licencePlate. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        didAddBTMS = self.setBTMS(aBTMS)
        if not didAddBTMS :
            raise RuntimeError ("Unable to create vehicle due to bTMS. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._routeAssignments = []

    #------------------------
    # INTERFACE
    #------------------------
    def setLicencePlate(self, aLicencePlate):
        wasSet = False
        anOldLicencePlate = self.getLicencePlate()
        if not (anOldLicencePlate is None) and anOldLicencePlate == aLicencePlate :
            return True
        if BusVehicle.hasWithLicencePlate(aLicencePlate) :
            return wasSet
        self._licencePlate = aLicencePlate
        wasSet = True
        if not (anOldLicencePlate is None) :
            BusVehicle.busvehiclesByLicencePlate.pop(anOldLicencePlate, None)
        BusVehicle.busvehiclesByLicencePlate[aLicencePlate] = self
        return wasSet

    def getLicencePlate(self):
        return self._licencePlate

    # Code from template attribute_GetUnique
    @staticmethod
    def getWithLicencePlate(aLicencePlate):
        return BusVehicle.busvehiclesByLicencePlate.get(aLicencePlate)

    # Code from template attribute_HasUnique
    @staticmethod
    def hasWithLicencePlate(aLicencePlate):
        return not (BusVehicle.getWithLicencePlate(aLicencePlate) is None)

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
        number = len(self._routeAssignments)
        return number

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
            existingBTMS.removeVehicle(self)
        self._bTMS.addVehicle(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfRouteAssignments():
        return 0

    # Code from template association_AddManyToOne
    def addRouteAssignment1(self, aDate, aRoute, aBTMS):
        from . import RouteAssignment
        return RouteAssignment(aDate, self, aRoute, aBTMS)

    def addRouteAssignment2(self, aRouteAssignment):
        wasAdded = False
        if (aRouteAssignment) in self._routeAssignments :
            return False
        existingBus = aRouteAssignment.getBus()
        isNewBus = not (existingBus is None) and not self == existingBus
        if isNewBus :
            aRouteAssignment.setBus(self)
        else :
            self._routeAssignments.append(aRouteAssignment)
        wasAdded = True
        return wasAdded

    def removeRouteAssignment(self, aRouteAssignment):
        wasRemoved = False
        #Unable to remove aRouteAssignment, as it must always have a bus
        if not self == aRouteAssignment.getBus() :
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
        BusVehicle.busvehiclesByLicencePlate.pop(self.getLicencePlate(), None)
        placeholderBTMS = self._bTMS
        self._bTMS = None
        if not (placeholderBTMS is None) :
            placeholderBTMS.removeVehicle(self)
        i = len(self._routeAssignments)
        while i > 0 :
            aRouteAssignment = self._routeAssignments[i - 1]
            aRouteAssignment.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "licencePlate" + ":" + str(self.getLicencePlate()) + "]" + str(os.linesep) + "  " + "bTMS = " + ((format(id(self.getBTMS()), "x")) if not (self.getBTMS() is None) else "null")

    def addRouteAssignment(self, *argv):
        from . import RouteAssignment
        from . import BusTransportationManagementSystem
        from . import Route
        if len(argv) == 3 and isinstance(argv[0], date) and isinstance(argv[1], Route) and isinstance(argv[2], BTMS) :
            return self.addRouteAssignment1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], RouteAssignment) :
            return self.addRouteAssignment2(argv[0])
        raise TypeError("No method matches provided parameters")
