# %% NEW FILE MaintenanceNote BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 58 "model.ump"
# line 231 "model.ump"
import os
from datetime import date
class MaintenanceNote():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #MaintenanceNote Attributes
    #MaintenanceNote Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aDate, aDescription, aTicket, aNoteTaker):
        self._noteTaker = None
        self._ticket = None
        self._description = None
        self._date = None
        self._date = aDate
        self._description = aDescription
        didAddTicket = self.setTicket(aTicket)
        if not didAddTicket :
            raise RuntimeError ("Unable to create ticketNote due to ticket. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddNoteTaker = self.setNoteTaker(aNoteTaker)
        if not didAddNoteTaker :
            raise RuntimeError ("Unable to create maintenanceNote due to noteTaker. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setDate(self, aDate):
        wasSet = False
        self._date = aDate
        wasSet = True
        return wasSet

    def setDescription(self, aDescription):
        wasSet = False
        self._description = aDescription
        wasSet = True
        return wasSet

    def getDate(self):
        return self._date

    def getDescription(self):
        return self._description

    # Code from template association_GetOne 
    def getTicket(self):
        return self._ticket

    # Code from template association_GetOne 
    def getNoteTaker(self):
        return self._noteTaker

    # Code from template association_SetOneToMany 
    def setTicket(self, aTicket):
        wasSet = False
        if aTicket is None :
            return wasSet
        existingTicket = self._ticket
        self._ticket = aTicket
        if not (existingTicket is None) and not existingTicket == aTicket :
            existingTicket.removeTicketNote(self)
        self._ticket.addTicketNote(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany 
    def setNoteTaker(self, aNoteTaker):
        wasSet = False
        if aNoteTaker is None :
            return wasSet
        existingNoteTaker = self._noteTaker
        self._noteTaker = aNoteTaker
        if not (existingNoteTaker is None) and not existingNoteTaker == aNoteTaker :
            existingNoteTaker.removeMaintenanceNote(self)
        self._noteTaker.addMaintenanceNote(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderTicket = self._ticket
        self._ticket = None
        if not (placeholderTicket is None) :
            placeholderTicket.removeTicketNote(self)
        placeholderNoteTaker = self._noteTaker
        self._noteTaker = None
        if not (placeholderNoteTaker is None) :
            placeholderNoteTaker.removeMaintenanceNote(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "description" + ":" + str(self.getDescription()) + "]" + str(os.linesep) + "  " + "date" + "=" + str((((self.getDate().__str__().replaceAll("  ", "    ")) if not self.getDate() == self else "this") if not (self.getDate() is None) else "null")) + str(os.linesep) + "  " + "ticket = " + str(((format(id(self.getTicket()), "x")) if not (self.getTicket() is None) else "null")) + str(os.linesep) + "  " + "noteTaker = " + ((format(id(self.getNoteTaker()), "x")) if not (self.getNoteTaker() is None) else "null")
