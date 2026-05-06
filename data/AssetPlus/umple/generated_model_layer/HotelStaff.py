# %% NEW FILE HotelStaff BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 21 "model.ump"
# line 206 "model.ump"
from .User import User
from datetime import date
class HotelStaff(User):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #HotelStaff Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEmail, aName, aPassword, aPhoneNumber):
        self._maintenanceTasks = None
        self._maintenanceNotes = None
        super().__init__(aEmail, aName, aPassword, aPhoneNumber)
        self._maintenanceNotes = []
        self._maintenanceTasks = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany 
    def getMaintenanceNote(self, index):
        aMaintenanceNote = self._maintenanceNotes[index]
        return aMaintenanceNote

    def getMaintenanceNotes(self):
        newMaintenanceNotes = tuple(self._maintenanceNotes)
        return newMaintenanceNotes

    def numberOfMaintenanceNotes(self):
        number = len(self._maintenanceNotes)
        return number

    def hasMaintenanceNotes(self):
        has = len(self._maintenanceNotes) > 0
        return has

    def indexOfMaintenanceNote(self, aMaintenanceNote):
        index = (-1 if not aMaintenanceNote in self._maintenanceNotes else self._maintenanceNotes.index(aMaintenanceNote))
        return index

    # Code from template association_GetMany 
    def getMaintenanceTask(self, index):
        aMaintenanceTask = self._maintenanceTasks[index]
        return aMaintenanceTask

    def getMaintenanceTasks(self):
        newMaintenanceTasks = tuple(self._maintenanceTasks)
        return newMaintenanceTasks

    def numberOfMaintenanceTasks(self):
        number = len(self._maintenanceTasks)
        return number

    def hasMaintenanceTasks(self):
        has = len(self._maintenanceTasks) > 0
        return has

    def indexOfMaintenanceTask(self, aMaintenanceTask):
        index = (-1 if not aMaintenanceTask in self._maintenanceTasks else self._maintenanceTasks.index(aMaintenanceTask))
        return index

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfMaintenanceNotes():
        return 0

    # Code from template association_AddManyToOne 
    def addMaintenanceNote1(self, aDate, aDescription, aTicket):
        from .MaintenanceNote import MaintenanceNote
        return MaintenanceNote(aDate, aDescription, aTicket, self)

    def addMaintenanceNote2(self, aMaintenanceNote):
        wasAdded = False
        if (aMaintenanceNote) in self._maintenanceNotes :
            return False
        existingNoteTaker = aMaintenanceNote.getNoteTaker()
        isNewNoteTaker = not (existingNoteTaker is None) and not self == existingNoteTaker
        if isNewNoteTaker :
            aMaintenanceNote.setNoteTaker(self)
        else :
            self._maintenanceNotes.append(aMaintenanceNote)
        wasAdded = True
        return wasAdded

    def removeMaintenanceNote(self, aMaintenanceNote):
        wasRemoved = False
        #Unable to remove aMaintenanceNote, as it must always have a noteTaker
        if not self == aMaintenanceNote.getNoteTaker() :
            self._maintenanceNotes.remove(aMaintenanceNote)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addMaintenanceNoteAt(self, aMaintenanceNote, index):
        wasAdded = False
        if self.addMaintenanceNote(aMaintenanceNote) :
            if index < 0 :
                index = 0
            if index > self.numberOfMaintenanceNotes() :
                index = self.numberOfMaintenanceNotes() - 1
            self._maintenanceNotes.remove(aMaintenanceNote)
            self._maintenanceNotes.insert(index, aMaintenanceNote)
            wasAdded = True
        return wasAdded

    def addOrMoveMaintenanceNoteAt(self, aMaintenanceNote, index):
        wasAdded = False
        if (aMaintenanceNote) in self._maintenanceNotes :
            if index < 0 :
                index = 0
            if index > self.numberOfMaintenanceNotes() :
                index = self.numberOfMaintenanceNotes() - 1
            self._maintenanceNotes.remove(aMaintenanceNote)
            self._maintenanceNotes.insert(index, aMaintenanceNote)
            wasAdded = True
        else :
            wasAdded = self.addMaintenanceNoteAt(aMaintenanceNote, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfMaintenanceTasks():
        return 0

    # Code from template association_AddManyToOptionalOne 
    def addMaintenanceTask(self, aMaintenanceTask):
        wasAdded = False
        if (aMaintenanceTask) in self._maintenanceTasks :
            return False
        existingTicketFixer = aMaintenanceTask.getTicketFixer()
        if existingTicketFixer is None :
            aMaintenanceTask.setTicketFixer(self)
        elif not self == existingTicketFixer :
            existingTicketFixer.removeMaintenanceTask(aMaintenanceTask)
            self.addMaintenanceTask(aMaintenanceTask)
        else :
            self._maintenanceTasks.append(aMaintenanceTask)
        wasAdded = True
        return wasAdded

    def removeMaintenanceTask(self, aMaintenanceTask):
        wasRemoved = False
        if (aMaintenanceTask) in self._maintenanceTasks :
            self._maintenanceTasks.remove(aMaintenanceTask)
            aMaintenanceTask.setTicketFixer(None)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addMaintenanceTaskAt(self, aMaintenanceTask, index):
        wasAdded = False
        if self.addMaintenanceTask(aMaintenanceTask) :
            if index < 0 :
                index = 0
            if index > self.numberOfMaintenanceTasks() :
                index = self.numberOfMaintenanceTasks() - 1
            self._maintenanceTasks.remove(aMaintenanceTask)
            self._maintenanceTasks.insert(index, aMaintenanceTask)
            wasAdded = True
        return wasAdded

    def addOrMoveMaintenanceTaskAt(self, aMaintenanceTask, index):
        wasAdded = False
        if (aMaintenanceTask) in self._maintenanceTasks :
            if index < 0 :
                index = 0
            if index > self.numberOfMaintenanceTasks() :
                index = self.numberOfMaintenanceTasks() - 1
            self._maintenanceTasks.remove(aMaintenanceTask)
            self._maintenanceTasks.insert(index, aMaintenanceTask)
            wasAdded = True
        else :
            wasAdded = self.addMaintenanceTaskAt(aMaintenanceTask, index)
        return wasAdded

    def delete(self):
        i = len(self._maintenanceNotes)
        while i > 0 :
            aMaintenanceNote = self._maintenanceNotes[i - 1]
            aMaintenanceNote.delete()
            i -= 1

        while self._maintenanceTasks:
            aMaintenanceTask = self._maintenanceTasks[0]
            aMaintenanceTask.delete()

        super().delete()

    def addMaintenanceNote(self, *argv):
        from .MaintenanceTicket import MaintenanceTicket
        from .MaintenanceNote import MaintenanceNote
        if len(argv) == 3 and isinstance(argv[0], date) and isinstance(argv[1], str) and isinstance(argv[2], MaintenanceTicket) :
            return self.addMaintenanceNote1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], MaintenanceNote) :
            return self.addMaintenanceNote2(argv[0])
        raise TypeError("No method matches provided parameters")
