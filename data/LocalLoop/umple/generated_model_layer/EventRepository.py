# %% NEW FILE EventRepository BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 72 "model.ump"
# line 202 "model.ump"

class EventRepository():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #EventRepository Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._organizerViewModel = None
        self._events = None
        self._events = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany 
    def getEvent(self, index):
        aEvent = self._events[index]
        return aEvent

    def getEvents(self):
        newEvents = tuple(self._events)
        return newEvents

    def numberOfEvents(self):
        number = len(self._events)
        return number

    def hasEvents(self):
        has = len(self._events) > 0
        return has

    def indexOfEvent(self, aEvent):
        index = (-1 if not aEvent in self._events else self._events.index(aEvent))
        return index

    # Code from template association_GetOne 
    def getOrganizerViewModel(self):
        return self._organizerViewModel

    def hasOrganizerViewModel(self):
        has = not (self._organizerViewModel is None)
        return has

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfEvents():
        return 0

    # Code from template association_AddManyToOne 
    def addEvent1(self, aEventId, aOrganizerId, aName, aDescription, aCategoryId, aFee, aEventStart, aEventEnd, aCapacity, aCategory, aOrganizer):
        from .Event import Event
        return Event(aEventId, aOrganizerId, aName, aDescription, aCategoryId, aFee, aEventStart, aEventEnd, aCapacity, aCategory, aOrganizer, self)

    def addEvent2(self, aEvent):
        wasAdded = False
        if (aEvent) in self._events :
            return False
        existingEventRepository = aEvent.getEventRepository()
        isNewEventRepository = not (existingEventRepository is None) and not self == existingEventRepository
        if isNewEventRepository :
            aEvent.setEventRepository(self)
        else :
            self._events.append(aEvent)
        wasAdded = True
        return wasAdded

    def removeEvent(self, aEvent):
        wasRemoved = False
        #Unable to remove aEvent, as it must always have a eventRepository
        if not self == aEvent.getEventRepository() :
            self._events.remove(aEvent)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addEventAt(self, aEvent, index):
        wasAdded = False
        if self.addEvent(aEvent) :
            if index < 0 :
                index = 0
            if index > self.numberOfEvents() :
                index = self.numberOfEvents() - 1
            self._events.remove(aEvent)
            self._events.insert(index, aEvent)
            wasAdded = True
        return wasAdded

    def addOrMoveEventAt(self, aEvent, index):
        wasAdded = False
        if (aEvent) in self._events :
            if index < 0 :
                index = 0
            if index > self.numberOfEvents() :
                index = self.numberOfEvents() - 1
            self._events.remove(aEvent)
            self._events.insert(index, aEvent)
            wasAdded = True
        else :
            wasAdded = self.addEventAt(aEvent, index)
        return wasAdded

    # Code from template association_SetOptionalOneToOne 
    def setOrganizerViewModel(self, aNewOrganizerViewModel):
        wasSet = False
        if not (self._organizerViewModel is None) and not self._organizerViewModel == aNewOrganizerViewModel and self == self._organizerViewModel.getEventRepository() :
            #Unable to setOrganizerViewModel, as existing organizerViewModel would become an orphan
            return wasSet
        self._organizerViewModel = aNewOrganizerViewModel
        anOldEventRepository = (aNewOrganizerViewModel.getEventRepository()) if not (aNewOrganizerViewModel is None) else None
        if not self == anOldEventRepository :
            if not (anOldEventRepository is None) :
                anOldEventRepository.organizerViewModel = None
            if not (self._organizerViewModel is None) :
                self._organizerViewModel.setEventRepository(self)
        wasSet = True
        return wasSet

    def delete(self):
        i = len(self._events)
        while i > 0 :
            aEvent = self._events[i - 1]
            aEvent.delete()
            i -= 1

        existingOrganizerViewModel = self._organizerViewModel
        self._organizerViewModel = None
        if not (existingOrganizerViewModel is None) :
            existingOrganizerViewModel.delete()

    def addEvent(self, *argv):
        from .Event import Event
        from .Category import Category
        from .Organizer import Organizer
        if len(argv) == 11 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], str) and isinstance(argv[4], str) and isinstance(argv[5], (float, int)) and isinstance(argv[6], int) and isinstance(argv[7], int) and isinstance(argv[8], int) and isinstance(argv[9], Category) and isinstance(argv[10], Organizer) :
            return self.addEvent1(argv[0], argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10])
        if len(argv) == 1 and isinstance(argv[0], Event) :
            return self.addEvent2(argv[0])
        raise TypeError("No method matches provided parameters")
