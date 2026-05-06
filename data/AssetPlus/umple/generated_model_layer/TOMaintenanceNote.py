# %% NEW FILE TOMaintenanceNote BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 113 "model.ump"
# line 251 "model.ump"
import os
from datetime import date
class TOMaintenanceNote():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #TOMaintenanceNote Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aDate, aDescription, aNoteTakerEmail):
        self._noteTakerEmail = None
        self._description = None
        self._date = None
        self._date = aDate
        self._description = aDescription
        self._noteTakerEmail = aNoteTakerEmail

    #------------------------
    # INTERFACE
    #------------------------
    def getDate(self):
        return self._date

    def getDescription(self):
        return self._description

    def getNoteTakerEmail(self):
        return self._noteTakerEmail

    def delete(self):
        pass

    def __str__(self):
        return str(super().__str__()) + "[" + "description" + ":" + str(self.getDescription()) + "," + "noteTakerEmail" + ":" + str(self.getNoteTakerEmail()) + "]" + str(os.linesep) + "  " + "date" + "=" + (((self.getDate().__str__().replaceAll("  ", "    ")) if not self.getDate() == self else "this") if not (self.getDate() is None) else "null")
