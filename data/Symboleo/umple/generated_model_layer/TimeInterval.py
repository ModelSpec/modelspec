# %% NEW FILE TimeInterval BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 54 "model.ump"

class TimeInterval():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #TimeInterval Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aStart, aEnd):
        self._end = None
        self._start = None
        if not self.setStart(aStart) :
            raise RuntimeError ("Unable to create TimeInterval due to aStart. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        if not self.setEnd(aEnd) :
            raise RuntimeError ("Unable to create TimeInterval due to aEnd. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne
    def getStart(self):
        return self._start

    # Code from template association_GetOne
    def getEnd(self):
        return self._end

    # Code from template association_SetUnidirectionalOne
    def setStart(self, aNewStart):
        wasSet = False
        if not (aNewStart is None) :
            self._start = aNewStart
            wasSet = True
        return wasSet

    # Code from template association_SetUnidirectionalOne
    def setEnd(self, aNewEnd):
        wasSet = False
        if not (aNewEnd is None) :
            self._end = aNewEnd
            wasSet = True
        return wasSet

    def delete(self):
        self._start = None
        self._end = None
