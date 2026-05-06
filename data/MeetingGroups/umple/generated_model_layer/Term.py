# %% NEW FILE Term BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 113 "model.ump"
# line 315 "model.ump"
import os

class Term():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Term Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aStartDate, aEndDate):
        self._endDate = None
        self._startDate = None
        self._startDate = aStartDate
        self._endDate = aEndDate

    #------------------------
    # INTERFACE
    #------------------------
    def setStartDate(self, aStartDate):
        wasSet = False
        self._startDate = aStartDate
        wasSet = True
        return wasSet

    def setEndDate(self, aEndDate):
        wasSet = False
        self._endDate = aEndDate
        wasSet = True
        return wasSet

    def getStartDate(self):
        return self._startDate

    def getEndDate(self):
        return self._endDate

    def delete(self):
        pass

    def __str__(self):
        return str(super().__str__()) + "[" + "]" + str(os.linesep) + "  " + "startDate" + "=" + str((((self.getStartDate().__str__().replaceAll("  ", "    ")) if not self.getStartDate() == self else "this") if not (self.getStartDate() is None) else "null")) + str(os.linesep) + "  " + "endDate" + "=" + (((self.getEndDate().__str__().replaceAll("  ", "    ")) if not self.getEndDate() == self else "this") if not (self.getEndDate() is None) else "null")
