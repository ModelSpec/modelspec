# %% NEW FILE Obligation BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 65 "model.ump"
from .LegalPosition import LegalPosition
import os
from enum import Enum, auto

class Obligation(LegalPosition):
    #------------------------
    # ENUMERATIONS
    #------------------------
    class ObligationStatus(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        Start = auto()
        Create = auto()
        Active = auto()
        Violation = auto()
        Discharge = auto()
        Fulfillment = auto()
        UnsuccessfulTermination = auto()

    class ObligationStatusActive(Enum):
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
    #Obligation Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aAntecedent, aConsequent, aContract, aDebtor, aCreditor, aSurviving):
        self._statusActive = None
        self._status = None
        self._surviving = None
        super().__init__(aName, aAntecedent, aConsequent, aContract, aDebtor, aCreditor)
        self._surviving = aSurviving
        self.resetStatus()
        self.resetStatusActive()

    #------------------------
    # INTERFACE
    #------------------------
    def setSurviving(self, aSurviving):
        wasSet = False
        self._surviving = aSurviving
        wasSet = True
        return wasSet

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

    def getSurviving(self):
        return self._surviving

    def getStatus(self):
        return self._status

    # Code from template attribute_GetDefaulted
    def getDefaultStatus(self):
        return Obligation.ObligationStatus.Start

    def getStatusActive(self):
        return self._statusActive

    # Code from template attribute_GetDefaulted
    def getDefaultStatusActive(self):
        return Obligation.ObligationStatusActive.Null

    # Code from template attribute_IsBoolean
    def isSurviving(self):
        return self._surviving

    def delete(self):
        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "surviving" + ":" + str(self.getSurviving()) + "]" + str(os.linesep) + "  " + "status" + "=" + str((((self.getStatus().__str__().replaceAll("  ", "    ")) if not self.getStatus() == self else "this") if not (self.getStatus() is None) else "null")) + str(os.linesep) + "  " + "statusActive" + "=" + (((self.getStatusActive().__str__().replaceAll("  ", "    ")) if not self.getStatusActive() == self else "this") if not (self.getStatusActive() is None) else "null")
