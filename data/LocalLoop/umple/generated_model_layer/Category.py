# %% NEW FILE Category BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 15 "model.ump"
# line 162 "model.ump"
import os

class Category():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Category Attributes
    #Category Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aCategoryId, aName, aDescription, aCategoryViewModel):
        self._categoryViewModel = None
        self._events = None
        self._description = None
        self._name = None
        self._categoryId = None
        self._categoryId = aCategoryId
        self._name = aName
        self._description = aDescription
        self._events = []
        didAddCategoryViewModel = self.setCategoryViewModel(aCategoryViewModel)
        if not didAddCategoryViewModel :
            raise RuntimeError ("Unable to create category due to categoryViewModel. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setCategoryId(self, aCategoryId):
        wasSet = False
        self._categoryId = aCategoryId
        wasSet = True
        return wasSet

    def setName(self, aName):
        wasSet = False
        self._name = aName
        wasSet = True
        return wasSet

    def setDescription(self, aDescription):
        wasSet = False
        self._description = aDescription
        wasSet = True
        return wasSet

    def getCategoryId(self):
        return self._categoryId

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

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
    def getCategoryViewModel(self):
        return self._categoryViewModel

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfEvents():
        return 0

    # Code from template association_AddManyToOne 
    def addEvent1(self, aEventId, aOrganizerId, aName, aDescription, aCategoryId, aFee, aEventStart, aEventEnd, aCapacity, aOrganizer, aEventRepository):
        from .Event import Event
        return Event(aEventId, aOrganizerId, aName, aDescription, aCategoryId, aFee, aEventStart, aEventEnd, aCapacity, self, aOrganizer, aEventRepository)

    def addEvent2(self, aEvent):
        wasAdded = False
        if (aEvent) in self._events :
            return False
        existingCategory = aEvent.getCategory()
        isNewCategory = not (existingCategory is None) and not self == existingCategory
        if isNewCategory :
            aEvent.setCategory(self)
        else :
            self._events.append(aEvent)
        wasAdded = True
        return wasAdded

    def removeEvent(self, aEvent):
        wasRemoved = False
        #Unable to remove aEvent, as it must always have a category
        if not self == aEvent.getCategory() :
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

    # Code from template association_SetOneToMany 
    def setCategoryViewModel(self, aCategoryViewModel):
        wasSet = False
        if aCategoryViewModel is None :
            return wasSet
        existingCategoryViewModel = self._categoryViewModel
        self._categoryViewModel = aCategoryViewModel
        if not (existingCategoryViewModel is None) and not existingCategoryViewModel == aCategoryViewModel :
            existingCategoryViewModel.removeCategory(self)
        self._categoryViewModel.addCategory(self)
        wasSet = True
        return wasSet

    def delete(self):
        i = len(self._events)
        while i > 0 :
            aEvent = self._events[i - 1]
            aEvent.delete()
            i -= 1

        placeholderCategoryViewModel = self._categoryViewModel
        self._categoryViewModel = None
        if not (placeholderCategoryViewModel is None) :
            placeholderCategoryViewModel.removeCategory(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "categoryId" + ":" + str(self.getCategoryId()) + "," + "name" + ":" + str(self.getName()) + "," + "description" + ":" + str(self.getDescription()) + "]" + str(os.linesep) + "  " + "categoryViewModel = " + ((format(id(self.getCategoryViewModel()), "x")) if not (self.getCategoryViewModel() is None) else "null")

    def addEvent(self, *argv):
        from .Event import Event
        from .EventRepository import EventRepository
        from .Organizer import Organizer
        if len(argv) == 11 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], str) and isinstance(argv[4], str) and isinstance(argv[5], (float, int)) and isinstance(argv[6], int) and isinstance(argv[7], int) and isinstance(argv[8], int) and isinstance(argv[9], Organizer) and isinstance(argv[10], EventRepository) :
            return self.addEvent1(argv[0], argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10])
        if len(argv) == 1 and isinstance(argv[0], Event) :
            return self.addEvent2(argv[0])
        raise TypeError("No method matches provided parameters")
