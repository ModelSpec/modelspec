# %% NEW FILE DriverSchedule BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 31 "../../../../../model.ump"
# line 66 "../../../../../model.ump"
import os
from enum import Enum, auto

class DriverSchedule():
    #------------------------
    # ENUMERATIONS
    #------------------------
    class Shift(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        Morning = auto()
        Afternoon = auto()
        Night = auto()

    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #DriverSchedule Attributes
    #DriverSchedule Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aShift, aDriver, aAssignment, aBTMS):
        self._bTMS = None
        self._assignment = None
        self._driver = None
        self._shift = None
        self._shift = aShift
        didAddDriver = self.setDriver(aDriver)
        if not didAddDriver :
            raise RuntimeError ("Unable to create driverSchedule due to driver. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddAssignment = self.setAssignment(aAssignment)
        if not didAddAssignment :
            raise RuntimeError ("Unable to create driverSchedule due to assignment. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddBTMS = self.setBTMS(aBTMS)
        if not didAddBTMS :
            raise RuntimeError ("Unable to create schedule due to bTMS. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setShift(self, aShift):
        wasSet = False
        self._shift = aShift
        wasSet = True
        return wasSet

    def getShift(self):
        return self._shift

    # Code from template association_GetOne
    def getDriver(self):
        return self._driver

    # Code from template association_GetOne
    def getAssignment(self):
        return self._assignment

    # Code from template association_GetOne
    def getBTMS(self):
        return self._bTMS

    # Code from template association_SetOneToMany
    def setDriver(self, aDriver):
        wasSet = False
        if aDriver is None :
            return wasSet
        existingDriver = self._driver
        self._driver = aDriver
        if not (existingDriver is None) and not existingDriver == aDriver :
            existingDriver.removeDriverSchedule(self)
        self._driver.addDriverSchedule(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setAssignment(self, aAssignment):
        wasSet = False
        if aAssignment is None :
            return wasSet
        existingAssignment = self._assignment
        self._assignment = aAssignment
        if not (existingAssignment is None) and not existingAssignment == aAssignment :
            existingAssignment.removeDriverSchedule(self)
        self._assignment.addDriverSchedule(self)
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
            existingBTMS.removeSchedule(self)
        self._bTMS.addSchedule(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderDriver = self._driver
        self._driver = None
        if not (placeholderDriver is None) :
            placeholderDriver.removeDriverSchedule(self)
        placeholderAssignment = self._assignment
        self._assignment = None
        if not (placeholderAssignment is None) :
            placeholderAssignment.removeDriverSchedule(self)
        placeholderBTMS = self._bTMS
        self._bTMS = None
        if not (placeholderBTMS is None) :
            placeholderBTMS.removeSchedule(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "]" + str(os.linesep) + "  " + "shift" + "=" + str((((self.getShift().__str__().replaceAll("  ", "    ")) if not self.getShift() == self else "this") if not (self.getShift() is None) else "null")) + str(os.linesep) + "  " + "driver = " + str(((format(id(self.getDriver()), "x")) if not (self.getDriver() is None) else "null")) + str(os.linesep) + "  " + "assignment = " + str(((format(id(self.getAssignment()), "x")) if not (self.getAssignment() is None) else "null")) + str(os.linesep) + "  " + "bTMS = " + ((format(id(self.getBTMS()), "x")) if not (self.getBTMS() is None) else "null")
