#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 86 "../model.ump"
# line 214 "../model.ump"
import os

class LogEntry():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #LogEntry Attributes
    #LogEntry Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aDescription, aRobot):
        self._robot = None
        self._description = None
        self._description = aDescription
        didAddRobot = self.setRobot(aRobot)
        if not didAddRobot :
            raise RuntimeError ("Unable to create log due to robot. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setDescription(self, aDescription):
        wasSet = False
        self._description = aDescription
        wasSet = True
        return wasSet

    def getDescription(self):
        return self._description

    # Code from template association_GetOne 
    def getRobot(self):
        return self._robot

    # Code from template association_SetOneToMany 
    def setRobot(self, aRobot):
        wasSet = False
        if aRobot is None :
            return wasSet
        existingRobot = self._robot
        self._robot = aRobot
        if not (existingRobot is None) and not existingRobot == aRobot :
            existingRobot.removeLog(self)
        self._robot.addLog(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderRobot = self._robot
        self._robot = None
        if not (placeholderRobot is None) :
            placeholderRobot.removeLog(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "description" + ":" + str(self.getDescription()) + "]" + str(os.linesep) + "  " + "robot = " + ((format(id(self.getRobot()), "x")) if not (self.getRobot() is None) else "null")

