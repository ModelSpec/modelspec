# %% NEW FILE Power BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 74 "model.ump"
from .LegalPosition import LegalPosition
import os
from enum import Enum, auto

class Power(LegalPosition):
    #------------------------
    # ENUMERATIONS
    #------------------------
    class PowerStatus(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        Start = auto()
        Create = auto()
        Active = auto()
        SuccessfulTermination = auto()
        UnsuccessfulTermination = auto()

    class PowerStatusActive(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        Null = auto()
        InEffect = auto()
        Suspension = auto()

    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Power Attributes
    #Power Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aAntecedent, aConsequent, aContract, aDebtor, aCreditor):
        self._terminated = None
        self._legalPositions = None
        self._statusActive = None
        self._status = None
        super().__init__(aName, aAntecedent, aConsequent, aContract, aDebtor, aCreditor)
        self.resetStatus()
        self.resetStatusActive()
        self._legalPositions = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template attribute_SetDefaulted
    def setStatus(self, aStatus):
        wasSet = False
        self._status = aStatus
        wasSet = True
        return wasSet

    def resetStatus(self):
        wasReset = False
        self._status = self.getDefaultStatus()
        wasReset = True
        return wasReset

    # Code from template attribute_SetDefaulted
    def setStatusActive(self, aStatusActive):
        wasSet = False
        self._statusActive = aStatusActive
        wasSet = True
        return wasSet

    def resetStatusActive(self):
        wasReset = False
        self._statusActive = self.getDefaultStatusActive()
        wasReset = True
        return wasReset

    def getStatus(self):
        return self._status

    # Code from template attribute_GetDefaulted
    def getDefaultStatus(self):
        return Power.PowerStatus.Start

    def getStatusActive(self):
        return self._statusActive

    # Code from template attribute_GetDefaulted
    def getDefaultStatusActive(self):
        return Power.PowerStatusActive.Null

    # Code from template association_GetMany
    def getLegalPosition(self, index):
        aLegalPosition = self._legalPositions[index]
        return aLegalPosition

    def getLegalPositions(self):
        newLegalPositions = tuple(self._legalPositions)
        return newLegalPositions

    def numberOfLegalPositions(self):
        number = len(self._legalPositions)
        return number

    def hasLegalPositions(self):
        has = len(self._legalPositions) > 0
        return has

    def indexOfLegalPosition(self, aLegalPosition):
        index = (-1 if not aLegalPosition in self._legalPositions else self._legalPositions.index(aLegalPosition))
        return index

    # Code from template association_GetOne
    def getTerminated(self):
        return self._terminated

    def hasTerminated(self):
        has = not (self._terminated is None)
        return has

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfLegalPositions():
        return 0

    # Code from template association_AddUnidirectionalMany
    def addLegalPosition(self, aLegalPosition):
        wasAdded = False
        if (aLegalPosition) in self._legalPositions :
            return False
        self._legalPositions.append(aLegalPosition)
        wasAdded = True
        return wasAdded

    def removeLegalPosition(self, aLegalPosition):
        wasRemoved = False
        if (aLegalPosition) in self._legalPositions :
            self._legalPositions.remove(aLegalPosition)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addLegalPositionAt(self, aLegalPosition, index):
        wasAdded = False
        if self.addLegalPosition(aLegalPosition) :
            if index < 0 :
                index = 0
            if index > self.numberOfLegalPositions() :
                index = self.numberOfLegalPositions() - 1
            self._legalPositions.remove(aLegalPosition)
            self._legalPositions.insert(index, aLegalPosition)
            wasAdded = True
        return wasAdded

    def addOrMoveLegalPositionAt(self, aLegalPosition, index):
        wasAdded = False
        if (aLegalPosition) in self._legalPositions :
            if index < 0 :
                index = 0
            if index > self.numberOfLegalPositions() :
                index = self.numberOfLegalPositions() - 1
            self._legalPositions.remove(aLegalPosition)
            self._legalPositions.insert(index, aLegalPosition)
            wasAdded = True
        else :
            wasAdded = self.addLegalPositionAt(aLegalPosition, index)
        return wasAdded

    # Code from template association_SetOptionalOneToMany
    def setTerminated(self, aTerminated):
        wasSet = False
        existingTerminated = self._terminated
        self._terminated = aTerminated
        if not (existingTerminated is None) and not existingTerminated == aTerminated :
            existingTerminated.removeTerminator(self)
        if not (aTerminated is None) :
            aTerminated.addTerminator(self)
        wasSet = True
        return wasSet

    def delete(self):
        self._legalPositions.clear()
        if not (self._terminated is None) :
            placeholderTerminated = self._terminated
            self._terminated = None
            placeholderTerminated.removeTerminator(self)
        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "]" + str(os.linesep) + "  " + "status" + "=" + str((((self.getStatus().__str__().replaceAll("  ", "    ")) if not self.getStatus() == self else "this") if not (self.getStatus() is None) else "null")) + str(os.linesep) + "  " + "statusActive" + "=" + str((((self.getStatusActive().__str__().replaceAll("  ", "    ")) if not self.getStatusActive() == self else "this") if not (self.getStatusActive() is None) else "null")) + str(os.linesep) + "  " + "terminated = " + ((format(id(self.getTerminated()), "x")) if not (self.getTerminated() is None) else "null")