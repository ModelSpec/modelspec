# %% NEW FILE Registration BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 21 "model.ump"
# line 167 "model.ump"
import os

class Registration():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Registration Attributes
    #Registration Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aRegistrationId, aEventId, aParticipantId, aOrganizerId, aStatus, aTimestamp, aEvent, aParticipant, aRegistrationRepository):
        self._registrationRepository = None
        self._participant = None
        self._event = None
        self._timestamp = None
        self._status = None
        self._organizerId = None
        self._participantId = None
        self._eventId = None
        self._registrationId = None
        self._registrationId = aRegistrationId
        self._eventId = aEventId
        self._participantId = aParticipantId
        self._organizerId = aOrganizerId
        self._status = aStatus
        self._timestamp = aTimestamp
        didAddEvent = self.setEvent(aEvent)
        if not didAddEvent :
            raise RuntimeError ("Unable to create registration due to event. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddParticipant = self.setParticipant(aParticipant)
        if not didAddParticipant :
            raise RuntimeError ("Unable to create registration due to participant. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddRegistrationRepository = self.setRegistrationRepository(aRegistrationRepository)
        if not didAddRegistrationRepository :
            raise RuntimeError ("Unable to create registration due to registrationRepository. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setRegistrationId(self, aRegistrationId):
        wasSet = False
        self._registrationId = aRegistrationId
        wasSet = True
        return wasSet

    def setEventId(self, aEventId):
        wasSet = False
        self._eventId = aEventId
        wasSet = True
        return wasSet

    def setParticipantId(self, aParticipantId):
        wasSet = False
        self._participantId = aParticipantId
        wasSet = True
        return wasSet

    def setOrganizerId(self, aOrganizerId):
        wasSet = False
        self._organizerId = aOrganizerId
        wasSet = True
        return wasSet

    def setStatus(self, aStatus):
        wasSet = False
        self._status = aStatus
        wasSet = True
        return wasSet

    def setTimestamp(self, aTimestamp):
        wasSet = False
        self._timestamp = aTimestamp
        wasSet = True
        return wasSet

    def getRegistrationId(self):
        return self._registrationId

    def getEventId(self):
        return self._eventId

    def getParticipantId(self):
        return self._participantId

    def getOrganizerId(self):
        return self._organizerId

    def getStatus(self):
        return self._status

    def getTimestamp(self):
        return self._timestamp

    # Code from template association_GetOne 
    def getEvent(self):
        return self._event

    # Code from template association_GetOne 
    def getParticipant(self):
        return self._participant

    # Code from template association_GetOne 
    def getRegistrationRepository(self):
        return self._registrationRepository

    # Code from template association_SetOneToMany 
    def setEvent(self, aEvent):
        wasSet = False
        if aEvent is None :
            return wasSet
        existingEvent = self._event
        self._event = aEvent
        if not (existingEvent is None) and not existingEvent == aEvent :
            existingEvent.removeRegistration(self)
        self._event.addRegistration(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany 
    def setParticipant(self, aParticipant):
        wasSet = False
        if aParticipant is None :
            return wasSet
        existingParticipant = self._participant
        self._participant = aParticipant
        if not (existingParticipant is None) and not existingParticipant == aParticipant :
            existingParticipant.removeRegistration(self)
        self._participant.addRegistration(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany 
    def setRegistrationRepository(self, aRegistrationRepository):
        wasSet = False
        if aRegistrationRepository is None :
            return wasSet
        existingRegistrationRepository = self._registrationRepository
        self._registrationRepository = aRegistrationRepository
        if not (existingRegistrationRepository is None) and not existingRegistrationRepository == aRegistrationRepository :
            existingRegistrationRepository.removeRegistration(self)
        self._registrationRepository.addRegistration(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderEvent = self._event
        self._event = None
        if not (placeholderEvent is None) :
            placeholderEvent.removeRegistration(self)
        placeholderParticipant = self._participant
        self._participant = None
        if not (placeholderParticipant is None) :
            placeholderParticipant.removeRegistration(self)
        placeholderRegistrationRepository = self._registrationRepository
        self._registrationRepository = None
        if not (placeholderRegistrationRepository is None) :
            placeholderRegistrationRepository.removeRegistration(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "registrationId" + ":" + str(self.getRegistrationId()) + "," + "eventId" + ":" + str(self.getEventId()) + "," + "participantId" + ":" + str(self.getParticipantId()) + "," + "organizerId" + ":" + str(self.getOrganizerId()) + "," + "status" + ":" + str(self.getStatus()) + "," + "timestamp" + ":" + str(self.getTimestamp()) + "]" + str(os.linesep) + "  " + "event = " + str(((format(id(self.getEvent()), "x")) if not (self.getEvent() is None) else "null")) + str(os.linesep) + "  " + "participant = " + str(((format(id(self.getParticipant()), "x")) if not (self.getParticipant() is None) else "null")) + str(os.linesep) + "  " + "registrationRepository = " + ((format(id(self.getRegistrationRepository()), "x")) if not (self.getRegistrationRepository() is None) else "null")
