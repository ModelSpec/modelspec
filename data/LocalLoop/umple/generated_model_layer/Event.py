# %% NEW FILE Event BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 2 "model.ump"
# line 157 "model.ump"
import os

class Event():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Event Attributes
    #Event Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEventId, aOrganizerId, aName, aDescription, aCategoryId, aFee, aEventStart, aEventEnd, aCapacity, aCategory, aOrganizer, aEventRepository):
        self._eventRepository = None
        self._organizer = None
        self._registrations = None
        self._category = None
        self._capacity = None
        self._eventEnd = None
        self._eventStart = None
        self._fee = None
        self._categoryId = None
        self._description = None
        self._name = None
        self._organizerId = None
        self._eventId = None
        self._eventId = aEventId
        self._organizerId = aOrganizerId
        self._name = aName
        self._description = aDescription
        self._categoryId = aCategoryId
        self._fee = aFee
        self._eventStart = aEventStart
        self._eventEnd = aEventEnd
        self._capacity = aCapacity
        didAddCategory = self.setCategory(aCategory)
        if not didAddCategory :
            raise RuntimeError ("Unable to create event due to category. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._registrations = []
        didAddOrganizer = self.setOrganizer(aOrganizer)
        if not didAddOrganizer :
            raise RuntimeError ("Unable to create event due to organizer. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddEventRepository = self.setEventRepository(aEventRepository)
        if not didAddEventRepository :
            raise RuntimeError ("Unable to create event due to eventRepository. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setEventId(self, aEventId):
        wasSet = False
        self._eventId = aEventId
        wasSet = True
        return wasSet

    def setOrganizerId(self, aOrganizerId):
        wasSet = False
        self._organizerId = aOrganizerId
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

    def setCategoryId(self, aCategoryId):
        wasSet = False
        self._categoryId = aCategoryId
        wasSet = True
        return wasSet

    def setFee(self, aFee):
        wasSet = False
        self._fee = aFee
        wasSet = True
        return wasSet

    def setEventStart(self, aEventStart):
        wasSet = False
        self._eventStart = aEventStart
        wasSet = True
        return wasSet

    def setEventEnd(self, aEventEnd):
        wasSet = False
        self._eventEnd = aEventEnd
        wasSet = True
        return wasSet

    def setCapacity(self, aCapacity):
        wasSet = False
        self._capacity = aCapacity
        wasSet = True
        return wasSet

    def getEventId(self):
        return self._eventId

    def getOrganizerId(self):
        return self._organizerId

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def getCategoryId(self):
        return self._categoryId

    def getFee(self):
        return self._fee

    def getEventStart(self):
        return self._eventStart

    def getEventEnd(self):
        return self._eventEnd

    def getCapacity(self):
        return self._capacity

    # Code from template association_GetOne 
    def getCategory(self):
        return self._category

    # Code from template association_GetMany 
    def getRegistration(self, index):
        aRegistration = self._registrations[index]
        return aRegistration

    def getRegistrations(self):
        newRegistrations = tuple(self._registrations)
        return newRegistrations

    def numberOfRegistrations(self):
        number = len(self._registrations)
        return number

    def hasRegistrations(self):
        has = len(self._registrations) > 0
        return has

    def indexOfRegistration(self, aRegistration):
        index = (-1 if not aRegistration in self._registrations else self._registrations.index(aRegistration))
        return index

    # Code from template association_GetOne 
    def getOrganizer(self):
        return self._organizer

    # Code from template association_GetOne 
    def getEventRepository(self):
        return self._eventRepository

    # Code from template association_SetOneToMany 
    def setCategory(self, aCategory):
        wasSet = False
        if aCategory is None :
            return wasSet
        existingCategory = self._category
        self._category = aCategory
        if not (existingCategory is None) and not existingCategory == aCategory :
            existingCategory.removeEvent(self)
        self._category.addEvent(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfRegistrations():
        return 0

    # Code from template association_AddManyToOne 
    def addRegistration1(self, aRegistrationId, aEventId, aParticipantId, aOrganizerId, aStatus, aTimestamp, aParticipant, aRegistrationRepository):
        from .Registration import Registration
        return Registration(aRegistrationId, aEventId, aParticipantId, aOrganizerId, aStatus, aTimestamp, self, aParticipant, aRegistrationRepository)

    def addRegistration2(self, aRegistration):
        wasAdded = False
        if (aRegistration) in self._registrations :
            return False
        existingEvent = aRegistration.getEvent()
        isNewEvent = not (existingEvent is None) and not self == existingEvent
        if isNewEvent :
            aRegistration.setEvent(self)
        else :
            self._registrations.append(aRegistration)
        wasAdded = True
        return wasAdded

    def removeRegistration(self, aRegistration):
        wasRemoved = False
        #Unable to remove aRegistration, as it must always have a event
        if not self == aRegistration.getEvent() :
            self._registrations.remove(aRegistration)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addRegistrationAt(self, aRegistration, index):
        wasAdded = False
        if self.addRegistration(aRegistration) :
            if index < 0 :
                index = 0
            if index > self.numberOfRegistrations() :
                index = self.numberOfRegistrations() - 1
            self._registrations.remove(aRegistration)
            self._registrations.insert(index, aRegistration)
            wasAdded = True
        return wasAdded

    def addOrMoveRegistrationAt(self, aRegistration, index):
        wasAdded = False
        if (aRegistration) in self._registrations :
            if index < 0 :
                index = 0
            if index > self.numberOfRegistrations() :
                index = self.numberOfRegistrations() - 1
            self._registrations.remove(aRegistration)
            self._registrations.insert(index, aRegistration)
            wasAdded = True
        else :
            wasAdded = self.addRegistrationAt(aRegistration, index)
        return wasAdded

    # Code from template association_SetOneToMany 
    def setOrganizer(self, aOrganizer):
        wasSet = False
        if aOrganizer is None :
            return wasSet
        existingOrganizer = self._organizer
        self._organizer = aOrganizer
        if not (existingOrganizer is None) and not existingOrganizer == aOrganizer :
            existingOrganizer.removeEvent(self)
        self._organizer.addEvent(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany 
    def setEventRepository(self, aEventRepository):
        wasSet = False
        if aEventRepository is None :
            return wasSet
        existingEventRepository = self._eventRepository
        self._eventRepository = aEventRepository
        if not (existingEventRepository is None) and not existingEventRepository == aEventRepository :
            existingEventRepository.removeEvent(self)
        self._eventRepository.addEvent(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderCategory = self._category
        self._category = None
        if not (placeholderCategory is None) :
            placeholderCategory.removeEvent(self)
        i = len(self._registrations)
        while i > 0 :
            aRegistration = self._registrations[i - 1]
            aRegistration.delete()
            i -= 1

        placeholderOrganizer = self._organizer
        self._organizer = None
        if not (placeholderOrganizer is None) :
            placeholderOrganizer.removeEvent(self)
        placeholderEventRepository = self._eventRepository
        self._eventRepository = None
        if not (placeholderEventRepository is None) :
            placeholderEventRepository.removeEvent(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "eventId" + ":" + str(self.getEventId()) + "," + "organizerId" + ":" + str(self.getOrganizerId()) + "," + "name" + ":" + str(self.getName()) + "," + "description" + ":" + str(self.getDescription()) + "," + "categoryId" + ":" + str(self.getCategoryId()) + "," + "fee" + ":" + str(self.getFee()) + "," + "eventStart" + ":" + str(self.getEventStart()) + "," + "eventEnd" + ":" + str(self.getEventEnd()) + "," + "capacity" + ":" + str(self.getCapacity()) + "]" + str(os.linesep) + "  " + "category = " + str(((format(id(self.getCategory()), "x")) if not (self.getCategory() is None) else "null")) + str(os.linesep) + "  " + "organizer = " + str(((format(id(self.getOrganizer()), "x")) if not (self.getOrganizer() is None) else "null")) + str(os.linesep) + "  " + "eventRepository = " + ((format(id(self.getEventRepository()), "x")) if not (self.getEventRepository() is None) else "null")

    def addRegistration(self, *argv):
        from .Registration import Registration
        from .RegistrationRepository import RegistrationRepository
        from .Participant import Participant
        if len(argv) == 8 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], str) and isinstance(argv[4], str) and isinstance(argv[5], int) and isinstance(argv[6], Participant) and isinstance(argv[7], RegistrationRepository) :
            return self.addRegistration1(argv[0], argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7])
        if len(argv) == 1 and isinstance(argv[0], Registration) :
            return self.addRegistration2(argv[0])
        raise TypeError("No method matches provided parameters")
