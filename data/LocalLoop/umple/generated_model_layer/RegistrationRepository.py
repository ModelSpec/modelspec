# %% NEW FILE RegistrationRepository BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 76 "model.ump"
# line 207 "model.ump"

class RegistrationRepository():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #RegistrationRepository Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._registrationViewModel = None
        self._registrations = None
        self._registrations = []

    #------------------------
    # INTERFACE
    #------------------------
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
    def getRegistrationViewModel(self):
        return self._registrationViewModel

    def hasRegistrationViewModel(self):
        has = not (self._registrationViewModel is None)
        return has

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfRegistrations():
        return 0

    # Code from template association_AddManyToOne 
    def addRegistration1(self, aRegistrationId, aEventId, aParticipantId, aOrganizerId, aStatus, aTimestamp, aEvent, aParticipant):
        from .Registration import Registration
        return Registration(aRegistrationId, aEventId, aParticipantId, aOrganizerId, aStatus, aTimestamp, aEvent, aParticipant, self)

    def addRegistration2(self, aRegistration):
        wasAdded = False
        if (aRegistration) in self._registrations :
            return False
        existingRegistrationRepository = aRegistration.getRegistrationRepository()
        isNewRegistrationRepository = not (existingRegistrationRepository is None) and not self == existingRegistrationRepository
        if isNewRegistrationRepository :
            aRegistration.setRegistrationRepository(self)
        else :
            self._registrations.append(aRegistration)
        wasAdded = True
        return wasAdded

    def removeRegistration(self, aRegistration):
        wasRemoved = False
        #Unable to remove aRegistration, as it must always have a registrationRepository
        if not self == aRegistration.getRegistrationRepository() :
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

    # Code from template association_SetOptionalOneToOne 
    def setRegistrationViewModel(self, aNewRegistrationViewModel):
        wasSet = False
        if not (self._registrationViewModel is None) and not self._registrationViewModel == aNewRegistrationViewModel and self == self._registrationViewModel.getRepository() :
            #Unable to setRegistrationViewModel, as existing registrationViewModel would become an orphan
            return wasSet
        self._registrationViewModel = aNewRegistrationViewModel
        anOldRepository = (aNewRegistrationViewModel.getRepository()) if not (aNewRegistrationViewModel is None) else None
        if not self == anOldRepository :
            if not (anOldRepository is None) :
                anOldRepository.registrationViewModel = None
            if not (self._registrationViewModel is None) :
                self._registrationViewModel.setRepository(self)
        wasSet = True
        return wasSet

    def delete(self):
        i = len(self._registrations)
        while i > 0 :
            aRegistration = self._registrations[i - 1]
            aRegistration.delete()
            i -= 1

        existingRegistrationViewModel = self._registrationViewModel
        self._registrationViewModel = None
        if not (existingRegistrationViewModel is None) :
            existingRegistrationViewModel.delete()

    def addRegistration(self, *argv):
        from .Registration import Registration
        from .Event import Event
        from .Participant import Participant
        if len(argv) == 8 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], str) and isinstance(argv[4], str) and isinstance(argv[5], int) and isinstance(argv[6], Event) and isinstance(argv[7], Participant) :
            return self.addRegistration1(argv[0], argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7])
        if len(argv) == 1 and isinstance(argv[0], Registration) :
            return self.addRegistration2(argv[0])
        raise TypeError("No method matches provided parameters")
